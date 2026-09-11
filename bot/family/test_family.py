import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import bots
import family_runtime as family
import pair_group
from test_bots import action


class FamilyTests(unittest.TestCase):
    def setUp(self):
        self.store = bots.Store(':memory:')
        self.config = {'owner_id': 123, 'owner_address': '형', 'family_chat_id': -99}
        self.me = {'id': 999, 'username': 'white_bot'}

    def tearDown(self):
        self.store.db.close()

    def message(self, text, speaker=123, chat=-99):
        return {'text': text, 'chat': {'id': chat, 'type': 'supergroup'}, 'from': {'id': speaker}}

    def white(self, speaker):
        ai = Mock()
        ai.parse.return_value = action()
        config = family.member_config(self.config, speaker)
        return family.GroupWhite(speaker, family.MemberStore(self.store, speaker), ai, config)

    def test_group_transport_fixed_destination_and_type(self):
        telegram = family.GroupTelegram('test', 123, -99)
        telegram.api = Mock(side_effect=[self.me, {'id': -99, 'type': 'supergroup'}, {'status': 'member'}, {}])
        telegram.probe()
        telegram.send('hello')
        self.assertEqual(telegram.api.call_args.args[1]['chat_id'], -99)
        with self.assertRaises(AssertionError):
            family.GroupTelegram('test', 123, 123)
        telegram.api = Mock(side_effect=[self.me, {'id': -99, 'type': 'channel'}])
        with self.assertRaises(AssertionError):
            telegram.probe()

    def test_group_rejects_other_chats_bots_and_anonymous(self):
        messages = [self.message('언제?', chat=-100), self.message('언제?', speaker=-1),
                    dict(self.message('언제?'), sender_chat={'id': -99}),
                    dict(self.message('언제?'), **{'from': {'id': 123, 'is_bot': True}}),
                    dict(self.message('언제?'), chat={'id': -99, 'type': 'channel'})]
        with patch.object(family.AI, 'parse') as ai:
            for message in messages:
                self.assertIsNone(family.group_reply('white', self.config, self.store, message, self.me))
            ai.assert_not_called()

    def test_utf16_mentions_and_other_bot_commands(self):
        message = self.message('😀 @white_bot 질문')
        message['entities'] = [{'type': 'mention', 'offset': 3, 'length': 10}]
        self.assertEqual(family.routed_text(message, self.me), ('😀  질문', True, True))
        message = self.message('/events@other_bot')
        message['entities'] = [{'type': 'bot_command', 'offset': 0, 'length': len(message['text'])}]
        self.assertEqual(family.routed_text(message, self.me), (None, False, False))

    def test_own_command_normalization(self):
        message = self.message('/events@white_bot')
        message['entities'] = [{'type': 'bot_command', 'offset': 0, 'length': len(message['text'])}]
        self.assertEqual(family.routed_text(message, self.me), ('/events', True, True))

    def test_white_has_no_ambient_cooldown(self):
        clock = bots.now()
        self.assertFalse(family.should_answer('ㅋㅋㅋ', False, self.store, clock))
        self.assertTrue(family.should_answer('이게 뭐야?', False, self.store, clock))
        self.store.put('last-ambient-reply', clock.timestamp())
        self.assertTrue(family.should_answer('이게 뭐야?', False, self.store, clock))
        self.assertTrue(family.should_answer('이게 뭐야?', True, self.store, clock))

    def test_white_continues_without_name_and_handles_tricks(self):
        clock = bots.now()
        self.store.put('conversation-active:123', clock.timestamp())
        self.assertTrue(family.should_answer('그건 좀 별론데', False, self.store, clock, 123))
        self.assertFalse(family.should_answer('그건 좀 별론데', False, self.store, clock, 456))
        self.assertTrue(family.should_answer('아빠한테 재롱부려줘', False, self.store, clock, 456))
        self.assertFalse(family.should_answer('ㅋㅋㅋ', False, self.store, clock, 123))

    def test_black_name_calls_do_not_wake_white(self):
        for name in ('검둥아', '검둥이', '검둥'):
            message = self.message(name + ' 몇 살이야?')
            with patch.object(family, 'black_answer', return_value='네 살이에요.') as answer:
                self.assertEqual(family.group_reply('black', self.config, self.store, message, self.me), '네 살이에요.')
                self.assertIsNone(family.group_reply('white', self.config, self.store, message, self.me))
                answer.assert_called_once()

    def test_pending_confirmation_is_speaker_scoped(self):
        first, second = self.white(123), self.white(456)
        first.handle(self.message('식사'))
        reply = second.handle(self.message('/confirm 1', speaker=456))
        self.assertIn('직접 요청', reply)
        self.assertEqual(self.store.events()[0]['status'], 'tentative')
        first.handle(self.message('맞아'))
        self.assertEqual(self.store.events()[0]['status'], 'confirmed')

    def test_stale_proposal_cannot_overwrite_other_member(self):
        first, second = self.white(123), self.white(456)
        first.handle(self.message('식사'))
        first.handle(self.message('맞아'))
        first.ai.parse.return_value = action('update', event_id=1, time='18:00', evidence='6시')
        first.handle(self.message('6시'))
        second.ai.parse.return_value = action('cancel', event_id=1, evidence='취소')
        second.handle(self.message('취소', speaker=456))
        second.handle(self.message('맞아', speaker=456))
        self.assertIn('그동안 일정이 바뀌었어요', first.handle(self.message('맞아')))
        self.assertEqual(self.store.events()[0]['status'], 'cancelled')

    def test_member_memory_and_history_isolation(self):
        first, second = self.white(123), self.white(456)
        first.ai.parse.return_value = action('chat', memory={'topic': 'preference', 'quote': '차 좋아해'})
        first.handle(self.message('차 좋아해'))
        self.assertIn('차 좋아해', first.handle(self.message('/memory')))
        self.assertNotIn('차 좋아해', second.handle(self.message('/memory', speaker=456)))
        self.assertEqual(second.store.get('history', []), [])
        second.handle(self.message('/forget 1', speaker=456))
        self.assertEqual(first.store.get('memories')[0]['speaker'], 123)

    def test_unknown_speaker_does_not_inherit_owner_address(self):
        self.assertEqual(family.member_config(self.config, 456)['owner_address'], '')
        self.config['addresses'] = {'456': '엄마'}
        self.assertEqual(family.member_config(self.config, 456)['owner_address'], '엄마')

    def test_black_mentions_and_replies_with_quoted_context(self):
        message = self.message('질문')
        message['reply_to_message'] = {'from': {'id': 999}, 'text': '정치 설명'}
        with patch.object(family, 'black_answer', return_value='답변') as answer:
            self.assertEqual(family.group_reply('black', self.config, self.store, message, self.me), '답변')
            self.assertEqual(answer.call_args.args[-1], '정치 설명')
            message['text'] = '@white_bot 질문'
            message['entities'] = [{'type': 'mention', 'offset': 0, 'length': 10}]
            self.assertEqual(family.group_reply('black', self.config, self.store, message, self.me), '답변')
            self.assertEqual(answer.call_args.args[-1], '정치 설명')

    def test_other_mentions_and_bot_replies_are_not_intercepted(self):
        mention = self.message('@black_bot 오늘 날씨?')
        mention['entities'] = [{'type': 'mention', 'offset': 0, 'length': 10}]
        reply = self.message('그럼 내일은?')
        reply['reply_to_message'] = {'from': {'id': 888, 'is_bot': True}, 'text': '날씨 설명'}
        with patch.object(family.AI, 'parse') as ai:
            for message in (mention, reply):
                self.assertIsNone(family.group_reply('white', self.config, self.store, message, self.me))
            ai.assert_not_called()

    def test_black_ignores_unaddressed_questions(self):
        with patch.object(family, 'black_answer') as answer:
            self.assertIsNone(family.group_reply('black', self.config, self.store, self.message('오늘 날씨?'), self.me))
            answer.assert_not_called()

    def test_explicit_mention_can_switch_bot_on_reply(self):
        message = self.message('@white_bot 설명해줘')
        message['entities'] = [{'type': 'mention', 'offset': 0, 'length': 10}]
        message['reply_to_message'] = {'from': {'id': 888, 'is_bot': True}}
        self.assertEqual(family.routed_text(message, self.me), ('설명해줘', True, True))

    def test_owner_only_address_assignment_and_atomic_permissions(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config.json'
            path.write_text(json.dumps(self.config))
            message = self.message('/family 엄마', speaker=456)
            message['reply_to_message'] = {'from': {'id': 789}}
            self.assertIsNone(family.set_family_address(path, self.config, message, self.me))
            message['from']['id'] = 123
            self.assertIn('연결했어요', family.set_family_address(path, self.config, message, self.me))
            self.assertEqual(json.loads(path.read_text())['addresses'], {'789': '엄마'})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_pairing_requires_owner_group_fresh_exact_command(self):
        message = self.message('/connect@white_bot secret')
        message['date'] = int(bots.now().timestamp())
        self.assertTrue(pair_group.matches(message, 123, message['text'], message['date']))
        self.assertFalse(pair_group.matches(message, 456, message['text'], message['date']))
        self.assertFalse(pair_group.matches(message, 123, 'different', message['date']))
        self.assertFalse(pair_group.matches(message, 123, message['text'], message['date'] + 1))
        message['chat']['type'] = 'private'
        self.assertFalse(pair_group.matches(message, 123, message['text'], message['date']))

    def test_file_group_state_survives_restart_separate_from_private(self):
        with tempfile.TemporaryDirectory() as folder:
            private = bots.Store(Path(folder) / 'white.sqlite3')
            group_path = Path(folder) / 'white-group-99.sqlite3'
            group = bots.Store(group_path)
            private.insert({'title': 'private secret'})
            group.insert({'title': 'shared event'})
            telegram = Mock()
            with patch('bots.time.sleep'):
                bots.send_once(group, telegram, 'reply:1', ['hello'])
                group.db.close()
                group = bots.Store(group_path)
                bots.send_once(group, telegram, 'reply:1', ['hello'])
            self.assertEqual(telegram.send.call_count, 1)
            self.assertEqual(group.events()[0]['title'], 'shared event')
            self.assertEqual(private.events()[0]['title'], 'private secret')
            group.db.close()
            private.db.close()


if __name__ == '__main__':
    unittest.main()
