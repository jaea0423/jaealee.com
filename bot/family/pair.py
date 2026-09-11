"""터미널에서 생성한 문구로 본인의 개인채팅만 연결합니다. 토큰은 출력하지 않습니다."""
import argparse
import json
import os
import secrets
import time
from pathlib import Path
from bots import request_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    path = Path(args.config).expanduser().resolve()
    config = json.loads(path.read_text(encoding='utf-8'))
    if config.get('owner_id'):
        raise RuntimeError('이미 개인방 ID가 있습니다. 자동 교체하지 않습니다.')
    token = config['white_token']
    if not token:
        raise RuntimeError('먼저 비공개 설정에 흰둥이 토큰을 입력하세요.')

    def api(method, payload):
        response = request_json(f'https://api.telegram.org/bot{token}/{method}', payload)
        if not response.get('ok'):
            raise RuntimeError('텔레그램 연결 실패')
        return response['result']

    if api('getWebhookInfo', {}).get('url'):
        raise RuntimeError('기존 webhook이 있습니다. 기존 운영 상태를 먼저 확인하세요.')
    phrase = '연결 ' + secrets.token_hex(12)
    print('2분 안에 흰둥이 개인방에 다음 문구를 보내세요:\n' + phrase, flush=True)
    deadline, offset = time.monotonic() + 120, 0
    while time.monotonic() < deadline:
        for update in api('getUpdates', {'offset': offset, 'timeout': 15, 'allowed_updates': ['message']}):
            offset = update['update_id'] + 1
            message = update.get('message', {})
            chat, sender = message.get('chat', {}), message.get('from', {})
            if (message.get('text') != phrase or chat.get('type') != 'private'
                    or chat.get('id') != sender.get('id') or sender.get('is_bot') or chat.get('id', 0) <= 0):
                continue
            config['owner_id'] = chat['id']
            # 설정 전체를 출력하지 않고 원본 파일만 갱신합니다.
            if os.name != 'nt':
                path.chmod(0o600)
            path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print('개인방 ID를 저장했습니다. 가족방에는 아무 메시지도 보내지 않았습니다.')
            return
    raise RuntimeError('시간 초과. 설정은 바꾸지 않았습니다.')


if __name__ == '__main__':
    main()
