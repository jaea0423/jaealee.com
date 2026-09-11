"""외부 발송이나 유료 호출 없이 개인방 경계와 일정·발송 상태를 검증합니다."""
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime
import bots


def action(intent='create', **values):
    return dict(dict(intent=intent, reply='시간은 언제인가요?', event_id=None,
                     title='가족 식사', date='2026-09-12', time=None, place=None, evidence='식사', memory=None, remind_at=None), **values)


class Tests(unittest.TestCase):
    def setUp(self):
        self.store = bots.Store(':memory:')
        self.ai = Mock()
        self.ai.parse.return_value = action()
        self.white = bots.White(123, self.store, self.ai)

    def tearDown(self):
        self.store.db.close()

    def message(self, text, kind='private', owner=123):
        return {'text': text, 'chat': {'type': kind, 'id': owner}, 'from': {'id': owner}}

    def test_private_boundary(self):
        for message in [self.message('식사', 'group', -99), self.message('식사', owner=456),
                        {'text': '식사', 'chat': {'type': 'private', 'id': 123}, 'from': {'id': 456}}]:
            self.assertIsNone(self.white.handle(message))
        self.ai.parse.assert_not_called()
        self.assertEqual(self.store.events(), [])

    def test_missing_is_not_invented_and_natural_confirmation(self):
        self.white.handle(self.message('내일 식사'))
        self.assertIsNone(self.store.events()[0]['time'])
        self.assertEqual(self.store.events()[0]['status'], 'tentative')
        self.white.handle(self.message('맞아'))
        self.assertEqual(self.store.events()[0]['status'], 'confirmed')
        jobs = bots.sync_reminders(self.store, datetime(2026, 9, 11, 20, tzinfo=bots.KST))
        self.assertEqual({j['label'] for j in jobs}, {'1주 전', '전날'})
        self.assertEqual(self.ai.parse.call_count, 1)

    def test_update_cancel_requires_confirmation(self):
        self.white.handle(self.message('식사'))
        self.ai.parse.return_value = action('update', event_id=1, time='18:00', evidence='6시')
        self.white.handle(self.message('저녁 6시'))
        self.assertIsNone(self.store.events()[0]['time'])
        self.white.handle(self.message('네'))
        self.assertEqual(self.store.events()[0]['time'], '18:00')
        self.ai.parse.return_value = action('cancel', event_id=1, evidence='취소')
        self.white.handle(self.message('그거 취소'))
        self.assertEqual(self.store.events()[0]['status'], 'confirmed')
        reply = self.white.handle(self.message('응'))
        self.assertIn('취소했어요', reply)
        self.assertNotIn('알려드릴게요', reply)
        self.white.handle(self.message('/confirm 1'))
        self.assertEqual(self.store.events()[0]['status'], 'cancelled')

    def test_invalid_action_no_write(self):
        for fields in [{'date': '2026-02-30'}, {'time': '25:01'}, {'evidence': '없는 말'}]:
            with self.assertRaises((AssertionError, ValueError)):
                self.white.apply(action(**fields), '식사', [])
        self.assertEqual(self.store.events(), [])

    def test_confirmed_reminders_once(self):
        self.store.insert(dict(title='식사', date='2026-09-12', time='18:00', status='confirmed'))
        telegram = Mock()
        with patch('bots.time.sleep'):
            for _ in range(2):
                bots.reminders(self.store, telegram, datetime(2026, 9, 11, 20, tzinfo=bots.KST))
            bots.reminders(self.store, telegram, datetime(2026, 9, 12, 9, tzinfo=bots.KST))
        self.assertEqual(telegram.send.call_count, 3)

    def test_unknown_delivery_not_repeated(self):
        telegram = Mock()
        telegram.send.side_effect = RuntimeError('timeout')
        with self.assertRaises(RuntimeError):
            bots.send_once(self.store, telegram, 'test', ['hello'])
        with self.assertRaises(RuntimeError):
            bots.send_once(self.store, telegram, 'test', ['hello'])
        self.assertEqual(telegram.send.call_count, 1)

    def test_black_format(self):
        news = {'date': '2026-09-11', 'market': {'value': '123SECRET'}, 'sections': [
            {'labelKr': '사회', 'cards': [{'title': '제목', 'summary': '내용', 'source': 'SOURCE', 'url': 'https://x.test'}]}]}
        text = '\n'.join(bots.digest('news', news))
        for unwanted in ['123SECRET', 'SOURCE', 'https://']:
            self.assertNotIn(unwanted, text)
        knowledge = {'date': '2026-09-11', 'articles': [{'label': '문장', 'title': '오늘', 'quote': '내용',
                     'attribution': '작가 · 책', 'sources': [{'url': 'https://x.test'}]}]}
        text = '\n'.join(bots.digest('knowledge', knowledge))
        self.assertIn('작가 · 책', text)
        self.assertNotIn('https://', text)
        self.assertEqual(bots.digest('knowledge', {'date': '2026-09-11', 'articles': []}), [])

    def test_black_date_time_and_dedup(self):
        telegram = Mock()
        payload = {'date': '2026-09-11', 'sections': [{'labelKr': '기술', 'cards': [{'title': '제목', 'summary': '내용'}]}]}
        with patch('bots.request_json', return_value=payload) as fetch, patch('bots.time.sleep'):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 8, tzinfo=bots.KST))
            fetch.assert_not_called()
            for _ in range(2):
                bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 9, tzinfo=bots.KST))
            self.assertEqual(telegram.send.call_count, 2)
            fetch.assert_called_once()
        with patch('bots.request_json', return_value=payload):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 12, 9, tzinfo=bots.KST))
        self.assertEqual(telegram.send.call_count, 2)

    def test_gemini_adapter(self):
        ai = bots.AI({'gemini_model': 'test-model', 'gemini_api_key': 'test-only', 'family': []})
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(action('chat'))}}]}
        with patch('bots.request_json', return_value=response) as request:
            self.assertEqual(ai.parse('안녕', [], [])['intent'], 'chat')
            self.assertIn('generativelanguage.googleapis.com', request.call_args.args[0])
            self.assertEqual(request.call_args.args[1]['response_format']['type'], 'json_schema')

    def test_emoji_length(self):
        for part in bots.chunks('🤍' * 8000):
            self.assertLessEqual(len(part.encode('utf-16-le')) // 2, 4096)

    def test_ai_failure_cooldown_no_false_save(self):
        self.ai.parse.side_effect = bots.ServiceError(429)
        first = self.white.handle(self.message('식사'))
        second = self.white.handle(self.message('다시 식사'))
        self.assertNotEqual(first, second)
        self.assertNotIn('429', first)
        self.assertEqual(self.ai.parse.call_count, 1)
        self.assertEqual(self.store.events(), [])
        self.assertIn('아직 기록된', self.white.handle(self.message('/events')))
        self.store.put('ai-pause-until', 0)
        self.ai.parse.side_effect = None
        self.ai.parse.return_value = action()
        self.white.handle(self.message('식사'))
        self.assertEqual(len(self.store.events()), 1)

    def test_malformed_ai_never_reaches_chat_or_schedule(self):
        for response in ['요청량 초과', {'error': 'secret response'}, action(date='2026-02-30')]:
            self.store.put('ai-pause-until', 0)
            self.ai.parse.return_value = response
            reply = self.white.handle(self.message('식사'))
            self.assertNotIn('secret', reply)
            self.assertEqual(self.store.events(), [])

    def test_black_missing_news_does_not_block_knowledge(self):
        telegram = Mock()
        with patch('bots.request_json', side_effect=bots.ServiceError(404)):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 9, tzinfo=bots.KST))
        telegram.send.assert_not_called()
        data = {'date': '2026-09-11', 'articles': [{'label': '문장', 'title': '오늘', 'quote': '문장', 'author': '작가'}]}
        with patch('bots.request_json', return_value=data), patch('bots.time.sleep'):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 12, tzinfo=bots.KST))
        self.assertEqual(telegram.send.call_count, 2)

    def test_black_empty_stale_and_invalid_are_silent(self):
        telegram = Mock()
        for data in [{'date': '2026-09-11', 'sections': []}, {'date': '2026-09-10'}, [], {'date': '2026-09-11'}]:
            self.store.put('black:2026-09-11:news:check-after', 0)
            with patch('bots.request_json', return_value=data):
                bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 9, tzinfo=bots.KST))
        telegram.send.assert_not_called()

    def test_addresses_and_omission(self):
        for address in ('형', '누나', '엄마', '오빠', ''):
            self.store.put('fallback-index', 0)
            white = bots.White(123, self.store, self.ai, {'addresses': {'123': address}})
            reply = white.unavailable()
            self.assertTrue(reply.startswith(address + ', ' if address else '지금'))
            self.assertNotIn('일정', reply)
            self.assertIn('일정', white.unavailable('일정 적어줘'))

    def test_news_deadline(self):
        telegram = Mock()
        data = {'date': '2026-09-11', 'sections': [{'labelKr': '기술', 'cards': [{'title': '제목', 'summary': '내용'}]}]}
        with patch('bots.request_json', return_value=data), patch('bots.time.sleep'):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 10, 59, tzinfo=bots.KST))
        self.assertEqual(telegram.send.call_count, 2)
        with patch('bots.request_json') as fetch:
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 11, tzinfo=bots.KST))
            bots.black_tick(self.store, telegram, datetime(2026, 9, 12, 6, tzinfo=bots.KST))
            fetch.assert_not_called()

    def test_knowledge_deadline(self):
        telegram = Mock()
        self.store.put('black:2026-09-11:news', True)
        with patch('bots.request_json', return_value={'date': '2026-09-11', 'articles': []}) as fetch:
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 14, 59, tzinfo=bots.KST))
            fetch.assert_called_once()
        with patch('bots.request_json') as fetch:
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 15, tzinfo=bots.KST))
            fetch.assert_not_called()

    def test_memory_keeps_original_and_survives_short_history(self):
        self.ai.parse.return_value = action('chat', memory={'topic': 'preference', 'quote': '매운 음식 싫어'})
        self.white.handle(self.message('매운 음식 싫어'))
        self.assertEqual(self.store.get('memories')[0]['quote'], '매운 음식 싫어')
        self.ai.parse.return_value = action('chat')
        for _ in range(12):
            self.white.handle(self.message('안녕'))
        self.assertEqual(len(self.store.get('history')), 10)
        self.assertEqual(self.ai.parse.call_args.args[3][0]['quote'], '매운 음식 싫어')
        self.assertIn('매운 음식', self.white.handle(self.message('/memory')))
        self.white.handle(self.message('/forget 1'))
        self.assertEqual(self.store.get('memories'), [])
        self.assertEqual(self.store.get('history'), [])

    def test_memory_cannot_invent_quote_or_change_persona(self):
        self.ai.parse.return_value = action('chat', memory={'topic': 'preference', 'quote': '없는 발언'})
        self.white.handle(self.message('안녕'))
        self.assertEqual(self.store.get('memories', []), [])
        self.store.put('ai-pause-until', 0)
        self.ai.parse.return_value = action('chat', memory={'topic': 'persona', 'quote': '반말해'})
        self.white.handle(self.message('반말해'))
        self.assertEqual(self.store.get('memories', []), [])

    def test_rejected_send_recovers_from_cached_copy(self):
        telegram = Mock()
        telegram.send.side_effect = [bots.ServiceError(429), None, None]
        data = {'date': '2026-09-11', 'sections': [{'labelKr': '기술', 'cards': [{'title': '제목', 'summary': '내용'}]}]}
        with patch('bots.request_json', return_value=data) as fetch, patch('bots.time.sleep'):
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 9, tzinfo=bots.KST))
            bots.black_tick(self.store, telegram, datetime(2026, 9, 11, 9, 5, tzinfo=bots.KST))
            fetch.assert_called_once()
        self.assertTrue(self.store.get('black:2026-09-11:news'))
        self.assertEqual(telegram.send.call_count, 3)

    def test_reminders_week_custom_and_restart_recovery(self):
        self.store.insert(dict(title='결혼식', date='2026-09-21', time='18:00', status='confirmed',
                               confirmed_at='2026-09-11T09:00:00+09:00', remind_at=['2026-09-20T17:00']))
        telegram = Mock()
        with patch('bots.time.sleep'):
            bots.reminders(self.store, telegram, datetime(2026, 9, 14, 10, 30, tzinfo=bots.KST))
            self.assertIn('다음 주 월요일', telegram.send.call_args.args[0])
            bots.reminders(self.store, telegram, datetime(2026, 9, 20, 23, tzinfo=bots.KST))
            # 전날 알림을 3시간 놓쳐도 복구하며 요청 시각 알림도 따로 보냅니다.
            self.assertEqual(telegram.send.call_count, 3)
            bots.reminders(self.store, telegram, datetime(2026, 9, 20, 23, 1, tzinfo=bots.KST))
            self.assertEqual(telegram.send.call_count, 3)
        jobs = bots.sync_reminders(self.store, datetime(2026, 9, 21, 19, tzinfo=bots.KST))
        self.assertIn('expired', [j['status'] for j in jobs])

    def test_reminder_failure_does_not_block_other_events(self):
        for title in ('식사', '방문'):
            self.store.insert(dict(title=title, date='2026-09-21', time=None, status='confirmed',
                                   confirmed_at='2026-09-11T09:00:00+09:00'))
        telegram = Mock()
        telegram.send.side_effect = [bots.ServiceError(429), None, None]
        with patch('bots.time.sleep'):
            bots.reminders(self.store, telegram, datetime(2026, 9, 14, 10, 30, tzinfo=bots.KST))
            self.assertEqual(telegram.send.call_count, 2)
            bots.reminders(self.store, telegram, datetime(2026, 9, 14, 10, 35, tzinfo=bots.KST))
            self.assertEqual(telegram.send.call_count, 3)

    def test_weekly_not_at_nine_and_cancel_suppresses(self):
        number = self.store.insert(dict(title='결혼식', date='2026-09-21', time='18:00', status='confirmed'))
        telegram = Mock()
        bots.reminders(self.store, telegram, datetime(2026, 9, 14, 9, tzinfo=bots.KST))
        telegram.send.assert_not_called()
        self.assertIn('T10:30', self.store.get('reminder-jobs')[0]['due'])
        event = self.store.events()[0]
        event['status'] = 'cancelled'
        self.store.update(number, event)
        bots.reminders(self.store, telegram, datetime(2026, 9, 14, 11, tzinfo=bots.KST))
        telegram.send.assert_not_called()

    def test_changed_date_restored_and_no_duplicate_on_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / 'white.sqlite3'
            saved = bots.Store(filename)
            number = saved.insert(dict(title='결혼식', date='2026-09-21', time='18:00', status='confirmed'))
            clock = datetime(2026, 9, 11, 9, tzinfo=bots.KST)
            bots.sync_reminders(saved, clock)
            event = saved.events()[0]
            event['date'] = '2026-09-22'
            saved.update(number, event)
            bots.sync_reminders(saved, clock)
            event['date'] = '2026-09-21'
            saved.update(number, event)
            bots.sync_reminders(saved, clock)
            telegram = Mock()
            with patch('bots.time.sleep'):
                bots.reminders(saved, telegram, datetime(2026, 9, 14, 10, 30, tzinfo=bots.KST))
                saved.db.close()
                saved = bots.Store(filename)
                bots.reminders(saved, telegram, datetime(2026, 9, 14, 10, 31, tzinfo=bots.KST))
            self.assertEqual(telegram.send.call_count, 1)
            saved.db.close()

    def test_old_weekly_sent_not_repeated_after_time_change(self):
        self.store.insert(dict(title='결혼식', date='2026-09-21', time='18:00', status='confirmed'))
        self.store.put('reminder-jobs', [dict(key='schedule:1:2026-09-21:18:00:2026-09-14T09:00:00+09:00',
                                             event_id=1, label='1주 전', due='2026-09-14T09:00:00+09:00', status='sent')])
        telegram = Mock()
        bots.reminders(self.store, telegram, datetime(2026, 9, 14, 10, 30, tzinfo=bots.KST))
        telegram.send.assert_not_called()

    def test_macos_service_has_private_config_only(self):
        import install_macos
        import plistlib
        config = Path('/private/config.json')
        value = install_macos.make_plist('white', config, '/python', '/bots.py', Path('/logs'))
        result = plistlib.loads(plistlib.dumps(value))
        self.assertEqual(result['ProgramArguments'][-2:], ['--config', str(config)])
        self.assertNotIn('token', str(result))
        self.assertTrue(result['KeepAlive'])


if __name__ == '__main__':
    unittest.main()
