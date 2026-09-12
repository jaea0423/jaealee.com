"""Website screenshots and album delivery; no AI calls or text fallback."""
import hashlib
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from bots import ServiceError, digest, request_json


def image_folder(config):
    folder = Path(config['state_dir']).expanduser() / 'digest-images'
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    folder.chmod(0o700)
    return folder


def cleanup_images(config, timestamp=None):
    timestamp = time.time() if timestamp is None else timestamp
    removed = 0
    for path in image_folder(config).iterdir():
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}-(news|knowledge)-[1-6]\.png', path.name):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        stat = path.stat()
        if timestamp - max(stat.st_mtime, getattr(stat, 'st_birthtime', stat.st_mtime)) < 72 * 3600:
            continue
        with path.open('rb') as source:
            if source.read(8) != b'\x89PNG\r\n\x1a\n':
                continue
        path.unlink()
        removed += 1
    return removed


def render(config, kind, day, data):
    from PIL import Image, ImageStat
    settings = config['image_renderer']
    folder = image_folder(config)
    payload = dict(kind=kind, day=day, data=data, folder=str(folder),
                   playwright=settings['playwright'], chrome=settings['chrome'])
    try:
        result = subprocess.run([settings['node'], str(Path(__file__).with_name('capture_digest.cjs'))],
                                input=json.dumps(payload), text=True, capture_output=True, timeout=180)
        if result.returncode:
            raise RuntimeError('Screenshot rendering failed')
        expected_count = 6 if kind == 'news' else 3
        if json.loads(result.stdout)['count'] != expected_count:
            raise RuntimeError('Unexpected screenshot count')
        images = []
        for index in range(1, expected_count + 1):
            path = folder / f'{day}-{kind}-{index}.png'
            with Image.open(path) as source:
                image = source.convert('RGB')
            if min(ImageStat.Stat(image).stddev) < 10:
                raise RuntimeError('Blank screenshot')
            # Keep the tested photo size, avoiding Telegram's tall-image downscaling.
            image.thumbnail((2560, 2560), Image.Resampling.LANCZOS)
            if max(image.size) / min(image.size) > 20:
                raise RuntimeError('Photo aspect ratio exceeds limit')
            image.save(path)
            path.chmod(0o600)
            blob = path.read_bytes()
            if len(blob) >= 10_000_000:
                raise RuntimeError('Photo exceeds upload limit')
            images.append({'name': path.name, 'sha256': hashlib.sha256(blob).hexdigest(),
                           'width': image.width, 'height': image.height, 'bytes': len(blob)})
        return images
    except Exception:
        raise RuntimeError('Digest image preparation failed') from None


def send_album(telegram, images, caption):
    target = getattr(telegram, 'chat_id', telegram.owner)
    boundary = uuid.uuid4().hex
    media = [{'type': 'photo', 'media': f'attach://image{i}'} for i in range(len(images))]
    media[0]['caption'] = caption
    pieces = []
    for field, value in {'chat_id': str(target), 'media': json.dumps(media, ensure_ascii=False)}.items():
        pieces.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"\r\n\r\n{value}\r\n'.encode())
    for index, path in enumerate(images):
        pieces.append((f'--{boundary}\r\nContent-Disposition: form-data; name="image{index}"; '
                       f'filename="{path.name}"\r\nContent-Type: image/png\r\n\r\n').encode()
                      + path.read_bytes() + b'\r\n')
    pieces.append(f'--{boundary}--\r\n'.encode())
    req = urllib.request.Request(f'https://api.telegram.org/bot{telegram.token}/sendMediaGroup',
                                 data=b''.join(pieces), headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        raise ServiceError(exc.code) from None
    except Exception:
        raise ServiceError() from None
    if not result.get('ok'):
        raise ServiceError(result.get('error_code'))
    messages = result['result']
    if (len(messages) != len(images) or any(m['chat']['id'] != target for m in messages)
            or len({m.get('media_group_id') for m in messages}) != 1
            or not messages[0].get('media_group_id')):
        raise ServiceError()
    return {'message_ids': [m['message_id'] for m in messages],
            'media_group_id': messages[0]['media_group_id'],
            'sizes': [{k: p[k] for k in ('width', 'height', 'file_size') if k in p}
                      for m in messages for p in [max(m['photo'], key=lambda p: p['width'] * p['height'])]]}


def deliver(config, store, telegram, kind, day, key):
    if kind not in ('news', 'knowledge') or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
        raise ValueError('Invalid edition')
    state_key = 'delivery:' + key + ':album-v1'
    state = store.get(state_key)
    if state == 'sent':
        return True
    if state == 'sending':
        raise RuntimeError('Album outcome uncertain; manual verification required')
    # Never overlap a partly sent legacy text digest during migration.
    if store.get('delivery:' + key + ':0') in ('sent', 'sending'):
        raise RuntimeError('Legacy digest already started')
    data = store.get(key + ':source')
    if data is None:
        data = request_json(f'https://jaealee.com/{kind}/data/{day}.json')
        if not isinstance(data, dict) or data.get('date') != day or not digest(kind, data):
            return False
        store.put(key + ':source', data)
    images = store.get(key + ':images')
    folder = image_folder(config)
    if not images or any(not (folder / i['name']).is_file() or
                         hashlib.sha256((folder / i['name']).read_bytes()).hexdigest() != i['sha256'] for i in images):
        images = render(config, kind, day, data)
        store.put(key + ':images', images)
    caption = digest(kind, data)[0]
    store.put(state_key, 'sending')
    try:
        receipt = send_album(telegram, [folder / i['name'] for i in images], caption)
    except ServiceError as exc:
        if exc.status in (400, 401, 403, 404, 429):
            store.put(state_key, 'retry')
        raise
    store.put(key + ':album-receipt', receipt)
    store.put(state_key, 'sent')
    return True
