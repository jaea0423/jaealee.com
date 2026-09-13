# v5 진행 기록

- 2026-09-14 v5 생성 — v4(6차-K 까지) 복사. 목적은 **Supabase 연동**(`work/7차_작업지시.md`). v4 는 그대로 둠.
  글꼴·이미지는 복사하지 않고 `../v4/assets` `../assets` 를 참조. 광고 영상은 `screen/ad.mp4`(29MB) 복사.
- 2026-09-14 v5 7차-A — 파일만 (코드 수정 없음. dist 가 v4 빌드와 바이트 단위 동일 확인).
  · `supabase/schema.sql`: stores(jsonb settings·snapshots) / reservations(행, data jsonb, deleted_at) / logs, updated_at 서버 트리거, RLS(authenticated 전체·anon 차단), mask_name + public_today·public_screen 뷰(anon select), stores 두 행. 델타 갱신용 (store, updated_at) 색인 추가
  · `supabase/checklist.md`: 재아가 할 일 1~8 + 복구 절차
  · `build.py`: `python build.py [dev]` — prod 는 지금 위치, dev 는 dev/·dev/screen/. `__SUPA_CFG__` ← supabase.{mode}.json(없으면 null). service_role 키가 들어오면 빌드 중단. demo 는 dev 에서만 true. 글꼴은 ../v4/assets 참조
  · `supabase.dev.json.example`
- 2026-09-14 v5 7차-B — 읽기 (`work/p8_b.py`). 파일 2,453 → 2,470KB(+17KB).
  · `var SUPA_CFG = __SUPA_CFG__` · sb(path,{method,body,prefer,anon}) — 실패는 e.network / e.status 로 · 세션: sbLogin/sbRefresh, 메모리+sessionStorage(hanok.session.v1), 1분 타이머에서 만료 5분 전 갱신(sessionTick)
  · **PIN 은 4자리 그대로, 서버 비밀번호 = PIN+"00"**(pinToPassword — 재아 결정, 지시서 '6자리 확정' 대체). pinCheckServer: 400 → 'PIN 번호가 맞지 않습니다' / 연결 없음 → 캐시+PIN 해시(djb2, localStorage) 맞으면 오프라인 읽기 전용 진입 / 그 외 '로그인 실패: …'. 확인 중엔 '서버 확인 중…'(회색)
  · loadFromServer: stores → reservations(365일, deleted_at 30일은 trash) → logs(300, who→ip 칸) → migrate → assembleData(_ui 는 localStorage hanok.ui.v1) → syncMark(SYNC.res/settings/snapshots/lastUpd — C 의 flush 기준) → cacheSave(hanok.cache.v1, 로그 제외)
  · rowToRes/resToRow — 왕복 diff 0 확인. phone 은 서버 숫자만/화면 하이픈, people=pplOf, 나머지 data
  · 오프라인: enterOffline(캐시)→ 갈색 띠 '오프라인 · 마지막 갱신 HH:MM · 볼 수만' + 다시 연결, 30초 재시도(reconnect). 보던 중 끊기면(refreshData e.network) 자동으로 캐시 모드
  · 읽기 전용 안내 readonlyBlock(): openWizard/openRes/markRes/delRes/applySettings/setTvType/addDemo/clearDemo. B 단계는 호박색 띠 '읽기 전용 — 저장은 C 에서'
  · tvType → settings.tvType(migrate 가 _ui 것 이전, setTvType 은 draft+실제 둘 다) · 예시 데이터 버튼은 !supaOn || demo 일 때만 · maskName 은 이미 가린 이름(*) 통과
  · 공개 뷰 loadPublic(): 매장 선택 '오늘 예약 N건' 과 TV(#/screen) — 로그인 없이. 뷰의 null 키는 버림(기본값 보존)
  · curl: anon reservations → 42501 permission denied ✓ / public_today → [] ✓ / public_screen → 두 매장 ✓ / 틀린 비번 → 400 invalid_credentials ✓
  · 브라우저: 틀린 PIN → 문구 / 키 틀림 → '로그인 실패: Invalid API key' / fetch 차단 → '서버에 연결할 수 없습니다' / TV 경로 공개 뷰로 렌더, #app 에 전화번호 없음. 실제 PIN(1018) 로그인 ✓ 세션 sessionStorage ✓ 같은 탭 새로고침 → PIN 없이 설정 화면 복구 ✓ 보던 중 연결 끊김 → 갈색 띠(한국 시각) ✓ 다시 연결 ✓ 오프라인에서 맞는 PIN → 캐시 진입 ✓ 틀린 PIN → 거부 ✓ 쓰기 차단 안내 ✓
- 2026-09-14 v5 7차-C — 쓰기 (`work/p8_c.py`). 파일 2,470 → 2,481KB.
  · saveData → flush(): SYNC 와 JSON 비교해 바뀐 것만 — 새 예약 POST / 바뀐 예약·휴지통 PATCH(`id=eq.&updated_at=eq.내가 본 값`, 0행이면 충돌) / 설정·스냅샷은 조건 없이 PATCH. 응답 updated_at 을 rec.updatedAt 에(문자열 그대로). 첫 로그인 때 서버 settings 가 {} 이면 기본값 전체가 올라감(SYNC 기준을 서버 원본으로)
  · 충돌: 서버 행 다시 읽어 확인창 '다른 기기에서 먼저 수정됐습니다'(삭제됐으면 '이미 삭제된 예약') + 다른 항목만 '18:00 → 19:00' 요약. '상대 내용으로 보기'(기본, 내 변경 버림) / '내 변경으로 덮어쓰기'(조건 없이 PATCH)
  · 저장 실패 → 빨간 띠(#savefail, body 에 직접 — 입력 중 시트를 안 다시 그림) '저장 안 됨 · … · 탭을 닫으면 사라집니다' + 다시 시도. 1분 타이머도 재시도
  · logEvent → logs INSERT(who=SESSION.who, 실패 무시) · reloadFromStore = 델타(`updated_at=gt.` URL 인코딩) + stores.updated_at 로 설정 변경 감지. 로컬 dirty 예약은 덮지 않음
  · enterStore 뒤 autoCloseDays·takeSnapshot(→ flush) · B 의 '읽기 전용 단계' 해제
  · **schema.sql: reservations.id uuid → text** (newId 가 'res_' 접두어를 붙임. 재아가 dev 에서 alter 실행)
  · 확인(탭 두 개, dev): 등록 → 서버 행(phone 숫자만, data 16키) + logs ✓ / 실패(uuid 오류) → 빨간 띠 → 다시 시도 → 올라감 ✓ / 탭 B 수정 → 탭 A 가 안 본 채 수정 → 충돌창 → 상대 내용 ✓ / 덮어쓰기 ✓ / 1분 델타(타이머·수동) ✓ / 탭 A 삭제 → 탭 B 델타로 사라짐(trash) ✓ / 삭제된 것 수정 → '이미 삭제' 창 ✓ / 새 탭은 PIN 다시 ✓ / 첫 로그인 뒤 서버 settings rooms 10 ✓
- 2026-09-14 v5 7차-C 보강 — 재아의 동시 작업 걱정에 코드를 다시 보고 둘 고침.
  ① 보내는 사이에 객체가 또 바뀌면(등록 직후 reflowTentatives 가 잠정 배정을 바꾸는 실제 사례) 서버엔 옛값·SYNC 엔 새값이 남던 것 → markSynced 가 '보낸 JSON' 기준으로 적고 다시 보냄(FLUSH_AGAIN). 등록 직후 서버 tentativeRoomId r1 ✓
  ② 충돌인데 내용이 같으면(두 기기가 같은 결론 — 아침 autoCloseDays, 같은 잠정 배정) 묻지 않고 받음. canon()(키 순서 무관 JSON)으로 비교. 진짜 다른 변경(인원·메모)은 여전히 확인창 ✓
  · 서로 다른 예약 두 건 동시 등록(POST 둘 겹침) → 둘 다 서버·동기화 ✓
- 2026-09-14 v5 더미 데이터 — `work/seed_dev.py`(dev 전용, demo:true 설정에서만). 2026-08-01~10-31 762건(10/10 이후는 드문드문). data.demo=true 라 앱의 '예시 데이터 지우기' 와 같은 기준으로 `python work/seed_dev.py clear` 가 지움.
  이름: 한국 연예인 80% / 외국인(영어·한글 표기) 12% / 기업·단체 7% / 아주 긴 이름 1%. 알러지 12%·요청 22%·메모 15%. 케이스: 노쇼·취소·변경 이력, 같은 번호 여러 날(단골·노쇼 이력), 같은 날 같은 번호 두 건(9/20), 미배정+잠정, 라스트오더 이후·브레이크 시간·정원 초과·성인 1명+유아 다수(경고), 코스 미정·코스 2종, 전화 없음.
  확인: 앱에서 762건 로드, 오늘 10건 타임라인 렌더, 예약률·확인 필요·노쇼 이력 정상, 오류 없음.
- 2026-09-14 v5 7차-D — 손님용 TV (`work/p8_d.py`). 공개 뷰 읽기는 B 의 loadPublic. 추가: loadPublicOrCache — 켤 때 서버 실패면 화면 캐시(hanok.screen.v1)로 시작(캐시가 오늘 것이 아니면 좌석 설정만 쓰고 예약은 비움), 캐시도 없으면 던져 빈 화면+띠
  · 확인(dev/screen/, 로그인 없음): 목록형 렌더·가린 이름 ✓ / #app 에 전화·메모·실명 없음 ✓ / anon 응답 본문 검사: public_today 키 store,time,name,people,room_id,status 만·전화 숫자 없음, public_screen 키 tvAd,rooms,tvType,displayRows 만 ✓ / 갱신 3회 실패 → '연결 확인 중' + 마지막 데이터 유지, 복구 시 해제 ✓ / 캐시로 시작·어제 캐시는 예약 비움·캐시 없음은 예외 ✓
- 2026-09-14 v5 7차-E — 계정 (`work/p8_e.py`).
  · PIN 변경 시트 4칸(관리자 비밀번호 · 현재 PIN · 새 PIN · 확인): admin 로그인으로 권한 확인 → 현재 PIN 으로 staff 임시 토큰 → PUT /auth/v1/user(newPIN+"00"). 지금 세션은 안 건드림. 관리자 비밀번호 변경 시트(apw) 추가(6자 이상). 보안 폴드에 버튼
  · PIN 틀림 5회 → 60초 잠금(PIN_LOCK_UNTIL, 남은 초 표시, 입력 차단). 429 는 별도 문구
  · PIN_ANY · DEFAULT_AUTH · DATA._auth 삭제, migrate 가 옛 _auth 를 지움. 서버 미연결 빌드는 아무 PIN 통과 + 잠금 화면에 '서버 미연결 빌드' 표시(.lk-open 부활)
  · 확인(dev): 5회 틀림 → '60초 뒤에…' + 입력 차단 ✓ / 관리자 비밀번호 틀림·현재 PIN 틀림 문구 ✓ / staff 비밀번호 실제 변경(101900) → 새 값으로 로그인 → 되돌림(101800) ✓ (Secure password change 꺼짐 확인) / 관리자 시트 틀린 현재 비밀번호 ✓ / 기존 세션 유지 ✓. **관리자 비밀번호 성공 경로는 재아 비밀번호라 미확인**
- 2026-09-14 v5 7차-F — 백업. `backup/hanok-backup.yml`(비공개 저장소 hanok-backup 의 .github/workflows/ 로) + `backup/fetch.py`(표준 라이브러리, Range 헤더로 1,000행씩 이어받기, 예약 전체(삭제 포함)·stores·로그 30일 → data/*.json 정렬·들여쓰기, 바뀐 것만 커밋). 매일 19:30 UTC(04:30 KST) + 수동 실행. service_role 은 GitHub Secrets 에만. 복구 단락은 checklist.md 끝(A 에서 작성)
  · 확인: anon 키로는 401(테이블 막힘) ✓ / staff 토큰·페이지 200 으로 dev 762+7 행 이어받기, 중복 0, 삭제 행 포함 ✓. 실제 Actions 실행은 재아가 저장소·Secrets 만든 뒤 workflow_dispatch 로
- 2026-09-14 v5 7차 마무리 — 재아 확인: PIN 변경(관리자 비밀번호 경로) 실제 동작 ✓ / hanok-backup 비공개 저장소 + Secrets + Actions 수동 실행 → data/*.json 생성 ✓ (checkout@v5 로 올려 경고 제거). 남은 것: 실서비스 프로젝트 `hanok` 셋업(checklist 2~5) → supabase.prod.json → `python build.py` → 배포, 백업 Secrets 를 prod 값으로. 결정(재아): 설정 변경에 관리자 확인 **안 걸음**(PIN 으로 들어온 사람이 설정 변경 가능). 커밋은 재아가 직접. 실서비스 전환은 수정 더 한 뒤 별도 논의.
- 2026-09-14 v5 7차-G — 재아 검토 (`work/p8_g.py`).
  ① 충돌은 선택지 없이 알림 '작성 도중 다른 기기에서 수정된 내용입니다' + 화면을 서버 내용으로(내 변경 버림). 다시 하면 충돌 없음 ✓(dev 확인)
  ② 잠정 배정 재계산 reflowFuture(): 서버 읽은 뒤(첫 로드·델타 변경 시) 오늘 이후 날짜의 룸 미정 예약을 겹침 기준으로 다시 배정(view.storeKey 없어도 동작). suggestSeat 는 '아무것도 없는 방' 을 1순위로(잠정 둘이 같은 방 잡던 것). 9/14 토스 결제팀 r7→r8 ✓ 서버 반영 ✓. 시드는 tentative 를 비워 앱이 계산
  ③ TV '오늘 예약이 없습니다'/'예약 없음' 문구 삭제 ④ TV 예약 없으면 광고만 전체 화면(settings.tvIdleFull 기본 켬, 설정 → 디스플레이 배치 '예약이 없을 때'). 목록/좌석표 무관. 바뀌는 순간에만 통째로 다시 그림(TV_IDLE_SHOWN). **schema.sql public_screen 뷰에 tvIdleFull 추가 → 재아가 뷰 재실행 필요**
  ⑤ 영업시간 세 칸 가운데 ⑥ 상단 날짜 페이지 기준 가운데(901px↑ grid 1fr auto 1fr) ⑦ 날짜 선택 달력 항상 42칸 ⑧ 새로고침 'N분 전' 삭제(refreshedAgo 제거), 1분 자동 갱신은 바뀐 것 있을 때만 다시 그림(입력 중엔 원래 안 그림) ⑨ 범례 '변동'
