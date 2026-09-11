import unittest
from unittest.mock import Mock, patch

import bots
import live_answers
from test_bots import action


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.config = {'ai_provider': 'gemini', 'gemini_api_key': 'test', 'gemini_model': 'gemini-2.5-flash'}

    def response(self, text, grounded=True):
        result = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': text}]}}]}
        if grounded:
            result['candidates'][0]['groundingMetadata'] = {'groundingChunks': [
                {'web': {'title': 'Weather source', 'uri': 'https://example.org/weather'}}]}
        return result

    def test_search_tool_and_timestamp_are_sent_and_source_is_shown(self):
        with patch('live_answers.request_json', return_value=self.response('서울은 맑아요.')) as request:
            text = live_answers.answer(self.config, '오늘 서울 날씨')
            payload = request.call_args.args[1]
            self.assertEqual(payload['tools'], [{'google_search': {}}])
            self.assertIn('now', payload['systemInstruction']['parts'][0]['text'])
            self.assertIn('Weather source', text)
            self.assertIn('KST', text)

    def test_ungrounded_current_facts_are_not_presented_as_verified(self):
        with patch('live_answers.request_json', return_value=self.response('서울은 99도예요.', False)):
            reply = live_answers.answer(self.config, '오늘 서울 날씨')
            self.assertNotIn('99도', reply)
            self.assertIn('최신 자료를 확인하지 못했어요', reply)

    def test_missing_weather_location_can_be_clarified(self):
        with patch('live_answers.request_json', return_value=self.response('어느 지역 날씨가 궁금하세요?', False)):
            self.assertIn('어느 지역', live_answers.answer(self.config, '날씨 알려줘'))

    def test_weather_followup_inherits_live_requirement(self):
        self.assertTrue(live_answers.needs_live('서울', [{'user': '오늘 날씨 알려줘'}]))

    def test_incomplete_native_output_is_rejected(self):
        result = self.response('중간 답변')
        result['candidates'][0]['finishReason'] = 'MAX_TOKENS'
        with patch('live_answers.request_json', return_value=result), self.assertRaises(AssertionError):
            live_answers.answer(self.config, '설명해줘')

    def test_white_weather_uses_search_but_schedule_keeps_structured_flow(self):
        store = bots.Store(':memory:')
        ai = Mock()
        white = bots.White(123, store, ai, self.config)
        message = {'chat': {'id': 123, 'type': 'private'}, 'from': {'id': 123}, 'text': '오늘 날씨?'}
        ai.parse.return_value = action('chat')
        with patch('live_answers.answer', return_value='검색한 날씨예요.') as search:
            self.assertEqual(white.handle(message), '검색한 날씨예요.')
            search.assert_called_once()
            ai.parse.return_value = action('create', evidence='식사')
            white.handle(dict(message, text='내일 식사 일정'))
            self.assertEqual(search.call_count, 1)
        self.assertEqual(store.events()[0]['status'], 'tentative')
        store.db.close()
