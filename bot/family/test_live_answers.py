import unittest
from unittest.mock import Mock, patch

import bots
import live_answers
from test_bots import action


class LiveTests(unittest.TestCase):
    def test_family_conversation_does_not_search_or_require_grounding(self):
        history = [{'user': '오늘 날씨', 'assistant': '어느 지역인가요?'}]
        for text in ('흰둥아 누나 뭐해', '요즘 누나 뭐해', '엄마 지금 어디 있어', '누나 불러줘', '멍청하네', '바보'):
            self.assertFalse(live_answers.needs_live(text, history), text)
            with patch('live_answers.request_json', return_value=self.response('누나, 잠깐 와 주세요!', False)) as request:
                reply = live_answers.answer(self.config, text, history)
                self.assertNotIn('최신 자료', reply)
                self.assertNotIn('tools', request.call_args.args[1])
        self.assertTrue(live_answers.needs_live('누나가 서울 날씨 알려달래'))
        self.assertTrue(live_answers.needs_live('최근 인공지능 모델 유형'))

    def test_family_group_context_reaches_both_answer_paths(self):
        config = dict(self.config, conversation_scope='family_group', owner_address='엄마',
                      recent_group=[{'speaker': '누나', 'text': '도서관 가요', 'at': 123}])
        with patch('live_answers.request_json', return_value=self.response('누나, 엄마가 불러요!', False)) as request:
            live_answers.answer(config, '누나 불러줘')
            prompt = request.call_args.args[1]['systemInstruction']['parts'][0]['text']
            self.assertIn('도서관 가요', prompt)
            self.assertIn('family_group', prompt)
        with patch('bots.request_json', return_value={'choices': [{'finish_reason': 'stop', 'message': {'content': __import__('json').dumps(action('chat'))}}]}) as request:
            bots.AI(config).parse('누나 불러줘', [], [], [])
            prompt = request.call_args.args[1]['messages'][0]['content']
            self.assertIn('도서관 가요', prompt)
            self.assertIn('family_group', prompt)

    def setUp(self):
        self.config = {'ai_provider': 'gemini', 'gemini_api_key': 'test', 'gemini_model': 'gemini-2.5-flash'}

    def response(self, text, grounded=True):
        result = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': text}]}}]}
        if grounded:
            result['candidates'][0]['groundingMetadata'] = {'groundingChunks': [
                {'web': {'title': 'Weather source', 'uri': 'https://example.org/weather'}}]}
        return result

    def test_search_tool_and_timestamp_are_internal_without_footer(self):
        with patch('live_answers.request_json', return_value=self.response('서울은 맑아요.')) as request:
            text = live_answers.answer(self.config, '오늘 서울 날씨')
            payload = request.call_args.args[1]
            self.assertEqual(payload['tools'], [{'google_search': {}}])
            self.assertIn('now', payload['systemInstruction']['parts'][0]['text'])
            self.assertEqual(text, '서울은 맑아요.')

    def test_ungrounded_current_facts_are_not_presented_as_verified(self):
        with patch('live_answers.request_json', return_value=self.response('서울은 99도예요.', False)):
            reply = live_answers.answer(self.config, '오늘 서울 날씨')
            self.assertNotIn('99도', reply)
            self.assertIn('최신 자료를 확인하지 못했어요', reply)

    def test_missing_weather_location_can_be_clarified(self):
        with patch('live_answers.request_json', return_value=self.response('어느 지역 날씨가 궁금하세요?', False)):
            self.assertIn('어느 지역', live_answers.answer(self.config, '날씨 알려줘'))

    def test_weather_followup_inherits_live_requirement(self):
        self.assertTrue(live_answers.needs_live('서울', [{'user': '오늘 날씨 알려줘', 'assistant': '어느 지역인가요?'}]))

    def test_weather_reaction_and_topic_change_do_not_search(self):
        history = [{'user': '서울 날씨', 'assistant': '쌀쌀해요.'}]
        for text in ('와 진짜 춥다', '추워', '아빠', '그러게'):
            self.assertFalse(live_answers.needs_live(text, history))

    def test_capability_and_character_questions_do_not_require_sources(self):
        for text in ('실시간 정보는 모르는건가?', '너 몇 살이야?', '언제 자냐?', '아빠한테 재롱부려줘'):
            self.assertFalse(live_answers.needs_live(text, [{'user': '오늘 날씨 알려줘'}]))
        with patch('live_answers.request_json', return_value=self.response('검색해서 알아볼 수 있어요.', False)):
            self.assertEqual(live_answers.answer(self.config, '실시간 정보는 모르는건가?'), '검색해서 알아볼 수 있어요.')

    def test_fixed_character_facts_in_both_prompts(self):
        from personas import CHARACTERS
        self.assertEqual(CHARACTERS['white']['age'], 3)
        self.assertIn('방석', CHARACTERS['white']['sleep'])
        self.assertIn('고구마', bots.PERSONA)
        with patch('live_answers.request_json', return_value=self.response('네 살이에요.', False)) as request:
            live_answers.answer(self.config, '몇 살이야?')
            self.assertIn('"age": 4', request.call_args.args[1]['systemInstruction']['parts'][0]['text'])

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
