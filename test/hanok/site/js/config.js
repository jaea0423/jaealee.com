/* 홈페이지 ↔ 예약 시스템 연결 정보. anon 키는 공개해도 되는 키입니다(서버 권한표가 막음) —
   홈페이지가 할 수 있는 건 남은 자리 읽기와 접수 한 줄 넣기뿐. service_role 키는 절대 여기 넣지 않습니다.
   지금은 dev 프로젝트. 실서비스로 바꿀 때 url·anonKey 만 교체(v7/supabase.prod.json 값). store 는 매장 키 */
window.SUPA = { url: "https://tequnppstugefkhilaqs.supabase.co", anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlcXVucHBzdHVnZWZraGlsYXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTM3MTIsImV4cCI6MjEwNDg4OTcxMn0.OTzk47tHUYmavOysPJ_vKsTjKkcX3gt7UiAC0kjntqE", store: "hanok" };
