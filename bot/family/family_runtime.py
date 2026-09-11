"""An explicitly paired group, with separate private and group state."""
import json
import os
import re
import time
from pathlib import Path

from bots import (AI, Store, Telegram, White, chunks,
                  now, process_lock, reminders, request_json, send_once)


class GroupTelegram(Telegram):
    def __init__(self, token, owner, chat_id):
        super().__init__(token, owner)
        assert type(chat_id) is int and chat_id < 0
        self.chat_id = chat_id

    def probe(self):
        me = self.api('getMe', {})
        chat = self.api('getChat', {'chat_id': self.chat_id})
        assert chat['id'] == self.chat_id and chat['type'] in ('group', 'supergroup')
        member = self.api('getChatMember', {'chat_id': self.chat_id, 'user_id': me['id']})
        assert member['status'] in ('member', 'administrator', 'creator')
        return me

    def send(self, text):
        return self.api('sendMessage', {'chat_id': self.chat_id, 'text': text,
                                       'link_preview_options': {'is_disabled': True}})


class MemberStore:
    # Shared events and delivery state, but each speaker owns their conversation.
    scoped = {'history', 'pending', 'memories', 'memory-sequence'}

    def __init__(self, store, speaker):
        self.store, self.speaker = store, speaker

    def key(self, key):
        return f'member:{self.speaker}:{key}' if key in self.scoped else key

    def get(self, key, default=None):
        return self.store.get(self.key(key), default)

    def put(self, key, value):
        self.store.put(self.key(key), value)

    def events(self):
        return self.store.events()

    def insert(self, data):
        return self.store.insert(dict(data, created_by=self.speaker))

    def update(self, event_id, data):
        return self.store.update(event_id, data)


class GroupWhite(White):
    def accepts(self, message):
        return (message.get('chat', {}).get('type') in ('group', 'supergroup')
                and message.get('chat', {}).get('id') == self.config['family_chat_id']
                and message.get('from', {}).get('id') == self.owner
                and type(self.owner) is int and self.owner > 0
                and not message.get('from', {}).get('is_bot')
                and not message.get('sender_chat'))

    def handle(self, message):
        if not self.accepts(message):
            return None
        text = message.get('text', '').strip()
        if text in ('/start', '/help'):
            return ('흰둥이 왔어요. 질문이나 일정을 알려주세요. '
                    '/events 일정 · /reminders 알림 · /memory 내 기억 · /forget 번호 삭제')
        pending = self.store.get('pending')
        confirm = re.fullmatch(r'/confirm (\d+)', text)
        natural = re.fullmatch(r'(응|네|넵|맞아|맞아요|확정해|확정해줘|그래)[.! ]*', text)
        if confirm or (natural and pending):
            if not pending or (confirm and int(confirm[1]) != pending['event_id']):
                return '직접 요청하신 제안만 확정할 수 있어요. 바꾸실 내용을 먼저 알려주세요.'
            event = next((e for e in self.store.events() if e['id'] == pending['event_id']), None)
            if not event or event.get('revision', 0) != pending.get('base_revision'):
                self.store.put('pending', None)
                return '그동안 일정이 바뀌었어요. /events로 확인하고 다시 요청해 주세요.'
        return super().handle(message)

    def apply(self, action, original, events):
        reply = super().apply(action, original, events)
        pending = self.store.get('pending')
        if pending:
            event = next(e for e in self.store.events() if e['id'] == pending['event_id'])
            self.store.put('pending', dict(pending, base_revision=event.get('revision', 0),
                                           proposed_at=now().timestamp()))
        return reply


def member_config(config, speaker):
    address = config.get('addresses', {}).get(str(speaker), '')
    if speaker == config['owner_id']:
        address = config.get('owner_address', '')
    return dict(config, owner_id=speaker, owner_address=address)


def routed_text(message, me, role=None):
    """Telegram entity offsets are UTF-16 units, not Python character offsets."""
    text = message.get('text', '')
    encoded = text.encode('utf-16-le')
    username = me['username'].lower()
    direct = False
    other_target = False
    ranges = []
    for entity in message.get('entities', []):
        start, length = entity.get('offset', 0), entity.get('length', 0)
        value = encoded[start * 2:(start + length) * 2].decode('utf-16-le', errors='replace')
        if entity['type'] == 'bot_command' and '@' in value:
            command, target = value.rsplit('@', 1)
            if target.lower() != username:
                return None, False, False
            direct = True
            ranges.append((start, length, command))
        if ((entity['type'] == 'mention' and value.lower() == '@' + username)
                or (entity['type'] == 'text_mention' and entity.get('user', {}).get('id') == me['id'])):
            direct = True
            ranges.append((start, length, ''))
        elif entity['type'] in ('mention', 'text_mention'):
            other_target = True
    mentioned = direct
    names = {'white': r'흰둥(?:이|아)?', 'black': r'검둥(?:이|아)?'}
    if role:
        called = {name for name, pattern in names.items()
                  if re.search(r'(?<![가-힣A-Za-z])' + pattern + r'(?=[\s,.!?~]|$)', text)}
        if role in called:
            direct = True
        elif called and not direct:
            return None, False, False
    reply_author = message.get('reply_to_message', {}).get('from', {})
    reply_to = reply_author.get('id') == me['id']
    if not direct and (other_target or (reply_author.get('is_bot') and not reply_to)):
        return None, False, False
    for start, length, replacement in sorted(ranges, reverse=True):
        encoded = encoded[:start * 2] + replacement.encode('utf-16-le') + encoded[(start + length) * 2:]
    return encoded.decode('utf-16-le').strip(), direct or reply_to, mentioned


def should_answer(text, direct, store, clock, speaker=None):
    if text is None:
        return False
    if direct or text.startswith('/') or text.startswith('흰둥'):
        return True
    if not text or re.fullmatch(r'[ㅋㅎㅠㅜ\s.!]+|(?:응|네|넵|ㅇㅇ|오케이|고마워)[.! ]*', text):
        return False
    if speaker and clock.timestamp() - store.get('conversation-active:' + str(speaker), 0) < 900:
        return True
    # Do not call AI for acknowledgements or every line of ordinary conversation.
    return bool(re.search(r'[?？]|알려줘|알려주|뭐야|뭘까|어때|어떻게|왜 |언제|어디|'
                          r'일정|예약|알림|기억해|적어줘|등록해|취소해|변경해|해줄래|줄까요|'
                          r'재롱|애교|해\s*줘|보여\s*줘|몇\s*살|나이|자냐|안녕|모르는건가', text))


def black_answer(config, store, speaker, text, context=''):
    if not text:
        return '검둥이에요. 궁금한 내용을 같이 적어주세요.'
    if len(text) > 6000:
        return '6,000자 이내로 나눠서 보내주세요.'
    key = 'ai-calls:' + now().date().isoformat()
    if store.get(key, 0) >= 100:
        return '오늘의 AI 대화 한도에 도달했어요.'
    if now().timestamp() < store.get('ai-pause-until', 0):
        return '잠깐 연결이 원활하지 않아요. 조금 뒤에 다시 불러주세요.'
    store.put(key, store.get(key, 0) + 1)
    try:
        from live_answers import answer
        scoped = MemberStore(store, speaker)
        value = answer(member_config(config, speaker), text, scoped.get('history', []), context)
        scoped.put('history', (scoped.get('history', []) + [{'user': text, 'assistant': value[:700]}])[-10:])
        return value[:700]
    except Exception:
        store.put('ai-pause-until', now().timestamp() + 60)
        return '지금 답을 받아오지 못했어요. 조금 뒤에 다시 불러주세요.'


def group_reply(role, config, store, message, me):
    sender, chat = message.get('from', {}), message.get('chat', {})
    if (chat.get('id') != config['family_chat_id'] or chat.get('type') not in ('group', 'supergroup')
            or type(sender.get('id')) is not int or sender['id'] <= 0
            or sender.get('is_bot') or message.get('sender_chat')):
        return None
    text, direct, mentioned = routed_text(message, me, role)
    if text is None:
        return None
    if role == 'black':
        context = message.get('reply_to_message', {}).get('text', '')
        return black_answer(config, store, sender['id'], text, context) if direct else None
    local = member_config(config, sender['id'])
    scoped = MemberStore(store, sender['id'])
    if text.startswith('/family') or text.startswith('/connect'):
        return None
    pending = scoped.get('pending')
    continuation = bool(pending and now().timestamp() - pending.get('proposed_at', 0) < 180
                        and re.fullmatch(r'(응|네|넵|맞아|맞아요|확정해|확정해줘|그래)[.! ]*|'
                                         r'(오전|오후|아침|저녁)?\s*\d{1,2}(시.*|:\d{2})', text))
    if not continuation and not should_answer(text, direct, store, now(), sender['id']):
        return None
    white = GroupWhite(sender['id'], scoped, AI(local), local)
    try:
        reply = white.handle(dict(message, text=text))
    except Exception:
        reply = '처리 결과를 확인하지 못했어요. /events에서 확인해 주세요.'
    if reply:
        store.put('conversation-active:' + str(sender['id']), now().timestamp())
    return reply


def set_family_address(config_path, config, message, me):
    if (message.get('chat', {}).get('id') != config['family_chat_id']
            or message.get('chat', {}).get('type') not in ('group', 'supergroup')
            or message.get('from', {}).get('id') != config['owner_id']
            or message.get('from', {}).get('is_bot') or message.get('sender_chat')):
        return None
    text, _, _ = routed_text(message, me)
    match = re.fullmatch(r'/family (엄마|아빠|누나|형)', text or '')
    if not match:
        return None
    target = message.get('reply_to_message', {})
    speaker = target.get('from', {})
    if type(speaker.get('id')) is not int or speaker['id'] <= 0 or speaker.get('is_bot') or target.get('sender_chat'):
        return '연결할 가족이 보낸 메시지에 답장으로 이 명령을 보내주세요.'
    fresh = json.loads(config_path.read_text(encoding='utf-8'))
    assert fresh['family_chat_id'] == config['family_chat_id']
    addresses = fresh.setdefault('addresses', {})
    addresses[str(speaker['id'])] = match[1]
    save_config(config_path, fresh)
    config.update(fresh)
    return match[1] + ' 호칭을 두 봇에 연결했어요.'


def save_config(path, config):
    temporary = path.with_suffix('.tmp')
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w', encoding='utf-8') as output:
        json.dump(config, output, ensure_ascii=False, indent=2)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def run(args, config):
    owner, role = config['owner_id'], args.role
    group = GroupTelegram(config[role + '_token'], owner, config['family_chat_id'])
    me = group.probe()
    if args.probe:
        print('Configured family group and bot membership verified; no message sent.')
        return
    if args.send_test:
        group.send('흰둥이 연결됐어요. 가족방에서도 함께할게요.' if role == 'white'
                   else '검둥이 연결됐어요. 멘션으로 불러주시면 답할게요.')
        return
    assert not group.api('getWebhookInfo', {}).get('url'), 'Existing webhook; no changes made.'
    folder = Path(config['state_dir']).expanduser()
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    folder.chmod(0o700)
    lock = process_lock(folder, role)
    private = Store(folder / (role + '.sqlite3'))
    (folder / (role + '.sqlite3')).chmod(0o600)
    group_path = folder / f'{role}-group-{abs(config["family_chat_id"])}.sqlite3'
    shared = Store(group_path)
    group_path.chmod(0o600)
    private_transport = Telegram(config[role + '_token'], owner)
    white = White(owner, private, AI(config), config)
    print(role + ' family runtime started; scheduled black broadcasts disabled.', flush=True)
    while True:
        try:
            if role == 'white':
                reminders(private, private_transport, now())
                reminders(shared, group, now())
            updates = group.api('getUpdates', {'offset': private.get('offset', 0),
                                               'timeout': 20, 'allowed_updates': ['message']})
            for update in updates:
                private.put('offset', update['update_id'] + 1)
                message = update.get('message', {})
                age = now().timestamp() - message.get('date', 0)
                if age > 600 or age < -60:
                    continue
                chat = message.get('chat', {})
                if role == 'white' and white.accepts(message):
                    try:
                        reply = white.handle(message)
                    except Exception:
                        reply = '처리 결과를 확인하지 못했어요. /events에서 확인해 주세요.'
                    if reply:
                        send_once(private, private_transport, 'reply:' + str(update['update_id']), chunks(reply))
                elif chat.get('id') == config['family_chat_id']:
                    # Only address assignments are live-reloaded; destination changes require restart.
                    config_path = Path(args.config).expanduser()
                    fresh = json.loads(config_path.read_text(encoding='utf-8'))
                    config['addresses'] = fresh.get('addresses', {})
                    reply = set_family_address(config_path, config, message, me) if role == 'white' else None
                    if reply is None:
                        reply = group_reply(role, config, shared, message, me)
                    if reply:
                        send_once(shared, group, 'reply:' + str(update['update_id']), chunks(reply))
        except Exception as error:
            print('Runtime failure:', type(error).__name__, flush=True)
            time.sleep(30)
