"""Bind only an owner's fresh one-time command in a group containing both bots."""
import argparse
import json
import secrets
import time
from pathlib import Path

from bots import Store, Telegram, process_lock
from family_runtime import GroupTelegram, save_config


def matches(message, owner, command, started):
    return (message.get('text', '').strip() == command
            and message.get('from', {}).get('id') == owner
            and not message.get('from', {}).get('is_bot') and not message.get('sender_chat')
            and message.get('chat', {}).get('type') in ('group', 'supergroup')
            and type(message.get('chat', {}).get('id')) is int
            and message['chat']['id'] < 0
            and started <= message.get('date', 0) <= time.time() + 30)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    path = Path(args.config).expanduser()
    config = json.loads(path.read_text(encoding='utf-8'))
    if config.get('family_chat_id'):
        raise SystemExit('Group already paired; no automatic replacement.')
    folder = Path(config['state_dir']).expanduser()
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = process_lock(folder, 'white')
    telegram = Telegram(config['white_token'], config['owner_id'])
    assert not telegram.api('getWebhookInfo', {}).get('url'), 'Existing webhook; unchanged.'
    me = telegram.api('getMe', {})
    command = '/connect@' + me['username'] + ' ' + secrets.token_hex(12)
    started = int(time.time())
    print('Send this command yourself in the family group within 5 minutes:\n' + command, flush=True)
    store = Store(folder / 'white.sqlite3')
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        updates = telegram.api('getUpdates', {'offset': store.get('offset', 0), 'timeout': 15,
                                               'allowed_updates': ['message']})
        for update in updates:
            store.put('offset', update['update_id'] + 1)
            message = update.get('message', {})
            if not matches(message, config['owner_id'], command, started):
                continue
            chat_id = message['chat']['id']
            for role in ('white', 'black'):
                GroupTelegram(config[role + '_token'], config['owner_id'], chat_id).probe()
            config['family_chat_id'] = chat_id
            config.setdefault('addresses', {})[str(config['owner_id'])] = config.get('owner_address', '형')
            save_config(path, config)
            print('Family group paired. No messages sent.', flush=True)
            return
    raise SystemExit('Pairing expired; configuration unchanged.')


if __name__ == '__main__':
    main()
