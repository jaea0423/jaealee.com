-- DineONE DB 변경 0004 (2026-11-12) — 손님 알림을 카카오 알림톡만으로 (구조 정리 15·21장)
-- 0003 다음. dev 에 한 번만 실행. 표 이름 sms_* 는 그대로 둡니다(이름은 바꾸지 않는 원칙, 5장) — 뜻은 '보낸 알림'

-- 1. 보낸 알림에 알림톡 종류와 템플릿 코드
alter table sms_messages drop constraint sms_messages_msg_type_check;
alter table sms_messages add constraint sms_messages_msg_type_check check (msg_type in ('sms','lms','alimtalk'));
alter table sms_messages add column template_code text;   -- 카카오 검수를 받은 템플릿 코드

-- 2. 웨이팅 호출 알림이 갔는지 — 못 갔으면 매장 화면에 '알림 못 감 · 직접 불러 주세요'
alter table waitlist add column notify_status text check (notify_status in ('sent','failed'));
