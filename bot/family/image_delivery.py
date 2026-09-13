"""Website screenshots and album delivery; no AI calls or text fallback."""
import hashlib
import errno
import json
import re
import subprocess
import socket
import ssl
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from bots import ServiceError, digest, request_json


class AlbumError(ServiceError):
    def __init__(self, stage, error_type, status=None, retryable=False):
        super().__init__(status)
        self.stage, self.error_type, self.retryable = stage, error_type, retryable


def send_album(telegram, images, caption):
    try:
        return _send_album(telegram, images, caption)
    except AlbumError:
        raise
    except Exception as exc:
        raise AlbumError('prepare', type(exc).__name__, retryable=True) from None


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


def _send_album(telegram, images, caption):
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
        raise AlbumError('http', 'HTTPError', exc.code,
                         exc.code in (400, 401, 403, 404, 429)) from None
    except urllib.error.URLError as exc:
        reason = exc.reason
        safe = isinstance(reason, (socket.gaierror, ssl.SSLCertVerificationError)) or getattr(reason, 'errno', None) in (errno.ECONNREFUSED, errno.ENETUNREACH, errno.EHOSTUNREACH)
        raise AlbumError('connect' if safe else 'transport', type(reason).__name__, retryable=safe) from None
    except Exception as exc:
        raise AlbumError('transport', type(exc).__name__) from None
    try:
        if not result.get('ok'):
            status = result.get('error_code')
            raise AlbumError('api', 'APIError', status, status in (400, 401, 403, 404, 429))
        messages = result['result']
        if (len(messages) != len(images) or any(m['chat']['id'] != target for m in messages)
                or len({m.get('media_group_id') for m in messages}) != 1
                or not messages[0].get('media_group_id')):
            raise ValueError('Invalid album receipt')
        return {'message_ids': [m['message_id'] for m in messages],
            'media_group_id': messages[0]['media_group_id'],
            'sizes': [{k: p[k] for k in ('width', 'height', 'file_size') if k in p}
                      for m in messages for p in [max(m['photo'], key=lambda p: p['width'] * p['height'])]]}
    except AlbumError:
        raise
    except Exception as exc:
        raise AlbumError('response', type(exc).__name__) from None


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
    attempt = {'started_at': time.time(), 'status': 'sending', 'photo_count': len(images),
               'bytes': sum((folder / i['name']).stat().st_size for i in images)}
    attempts = store.get(key + ':album-attempts', [])
    attempts.append(attempt)
    store.put(key + ':album-attempts', attempts)
    store.put(state_key, 'sending')
    try:
        receipt = send_album(telegram, [folder / i['name'] for i in images], caption)
    except ServiceError as exc:
        retryable = getattr(exc, 'retryable', exc.status in (400, 401, 403, 404, 429))
        if retryable:
            store.put(state_key, 'retry')
        attempt.update(status='retry' if retryable else 'uncertain', ended_at=time.time(),
                       stage=getattr(exc, 'stage', 'transport'), error_type=getattr(exc, 'error_type', type(exc).__name__),
                       http_status=exc.status)
        store.put(key + ':album-attempts', attempts)
        print('Album failure:', kind, day, attempt['stage'], attempt['error_type'],
              'status=' + str(exc.status), attempt['status'], flush=True)
        raise
    store.put(key + ':album-receipt', receipt)
    store.put(state_key, 'sent')
    attempt.update(status='sent', ended_at=time.time())
    store.put(key + ':album-attempts', attempts)
    return True
