# v4 진행 기록

- 2026-09-13 v4 생성 — v3 복사. 목적은 **Supabase 붙이기 전 데이터 모양 확정**.
  계획은 `../docs/supabase_준비.md`, 순서는 `CLAUDE.md` 1장.
- 2026-09-13 v4 1차 — 문구·UI 정리.
  · 잠금: "PIN 번호를 입력하세요" · "숫자 키보드로도…" · "제작 중이라…" 삭제, 네모 → 동그라미(.pdot)
  · 상단바: 한옥반점 → HANOK(.sn-brand), 날짜 15px. **오늘이 아니면 상단바 색 변경**(.topbar.notoday .past/.future)
  · 상단바: 새로고침 버튼(.b-refresh) + "N분 전"(refreshedAgo). 1분마다 자동 갱신(refreshData → 나중에 reloadFromStore), 30초마다 글자만 갱신
  · 설정: 한 번에 하나만 펼침(toggleFold, s_ 접두 섹션끼리)
  · 마법사: eyebrow(손님께 여쭤 보세요/직원 확인) 삭제, 경로·메뉴 타일 설명 삭제(빈 s-d 안 그림, 세로 중앙),
    "위 인원에 포함됩니다"→"총 인원에 포함", 코스 미정 부연 삭제, 코스 팝업 − 버튼 삭제,
    전화번호·알러지 "필수" 삭제, 요청사항·메모에 "선택", "우리끼리만 봅니다"·"이대로 등록됩니다" 삭제, "예약 하나 더"→"새 예약"
  · 날짜 화면 높이 고정: 달력 항상 42칸 / 시각 칸은 weekHourRange(주 최이른 개점~최늦 마감)로 요일 무관 고정, 밖은 .outside "영업 전/종료"
    / .hcell height:64px / .hn 한 줄 / .wz-warn 60px 고정 / .hours-line 36px 고정. 월·일·다음달 전부 같은 높이 확인
- 2026-09-13 v4 2차 — **DB 전 5개** (`../docs/supabase_준비.md` 1부).
  ① 코스 키 `순서|이름` → `cg_xxx|이름`. 묶음에 id(cg_dinner/cg_wdlunch/cg_welunch, 새 행은 newId), courseGroupById(), migrate 가 옛 키 변환(옛 번호도 fallback)
  ② newId("res") — UUID v4 직접 생성 (구형 TV 에 crypto.randomUUID 없음). 두 곳 교체
  ③ soft delete — delRes 가 deletedAt 찍고 s.trash 로 이동(최대 500). 화면 코드는 reservations 만 보므로 동작 동일. migrate 가 deletedAt 붙은 것 trash 로
  ④ touch(rec) → updatedAt. addChange 안에서 자동, markRes(확정/방문도), smsSend
  ⑤ 예시 데이터 자동 주입 차단 — 저장소 없음(개발)이면 예시, **있는데 실패면 빈 상태 + _readonly + 빨간 띠(.loaderr)**. saveData 가 _readonly 면 안 씀.
    설정→기타에 "예시 데이터 넣기" 버튼(사람이 눌러야만)
  · 확인: migrate 단위 테스트, 삭제→trash, markRes→updatedAt, 코스 팝업 새 키, 실패 흉내→예약 0건·띠 표시. 오류 0
- 2026-09-13 v4 3차 — **글꼴 내장**. 시스템 글꼴(맑은 고딕/바탕) 대체가 "파워포인트 느낌"의 원인.
  Pretendard 400·700 + Noto Serif KR 700·900 을 KS X 1001 한글 2,350자 + ASCII + 기호 + 歡迎光臨韓屋反店飯點 로 부분집합(pyftsubset, woff2)
  → `assets/font-*.b64` 4개, build.py 가 `__FONT_PT_R__ __FONT_PT_B__ __FONT_NS_7__ __FONT_NS_9__` 로 끼움. 파일 1.48MB → 2.19MB. 만드는 법은 `work/fonts.md`
- 2026-09-13 v4 4차 — **인트로 재설계** (`work/p5_intro.py`).
  · 원인: 글자마다 render() 로 innerHTML 을 통째로 다시 써서 CSS 전환이 한 번도 재생되지 않았음(요소가 매번 새로 생김) → 한 번만 그리고 클래스만 바꿈(introStep)
  · 붉은 칠기·금박 歡迎光臨 → 한지(SVG 잡음 결)·먹 어서오세요(Noto Serif KR 900, 최대 104px), 글자는 blur 10px → 0 으로 '스미듯', 양옆 띠살 창호(.intro-sash, 그라디언트만) 슬라이드, 마지막 붉은 낙관 韓屋(.intro-seal) + 한옥반점 소제. 총 2.3초, 아무 데나 누르면 건너뜀
  · 폰(640px 이하)은 창호 숨김. render() 가 도중에 불려도 INTRO.n 기준으로 그대로 그림
- 2026-09-13 v4 5차 — **손님용 화면을 screen/ 폴더로 + 방치용 동작** (`work/p6_screen.py`).
  · build.py 가 같은 파일을 `screen/index.html` 로도 생성. TV 주소 = `jaealee.com/test/hanok/v4/screen/` (로그인 없음, 주소만 열면 디스플레이)
  · readRoute 가 `/screen` `/screen/` `/screen/index.html` `/screen/hanok` 전부 인식. appDir() 하나로 경로 계산 통일(adUrl/screenUrl/setRoute)
  · **광고 영상은 `screen/ad.mp4`** 에 둠(v3 의 v3/ad.mp4 를 옮겨야 함). 설정의 파일 이름만 적으면 screen/ 을 붙임
  · 1분 갱신: 통째로 render() → 날개(.tvl-side)만 갈아 끼움(tvSideHtml). **매분 영상이 처음부터 다시 시작하던 버그** 해결. 갱신 때 refreshData()(→ 나중에 Supabase)
  · 3번 연속 읽기 실패 → 바닥글에 작게 "연결 확인 중"(마지막 데이터 유지). 성공하면 사라짐
  · 주소로 들어온 화면은 새벽 4시에 하루 한 번 location.reload() (오래 켠 TV 브라우저 메모리)
  · 목록형 글자: 시각 명조 900·3.4tvu, 이름 2.5tvu, 좌석/인원 분리(.tvl-seat/.tvl-cnt) 인원 금색, 날짜 자간 .18→.06em
  · 글꼴: CDN link 3개 제거(외부 요청 0). Pretendard 600 추가(600 이 55곳). 명조 700 은 준비만(435KB, 안 넣음). 파일 2.42MB
  · 확인(Playwright, 실제 경로 /test/hanok/v4/screen/): 라우팅 3종, 영상이 갱신 뒤에도 같은 요소·이어서 재생, 실패 3회→띠, 성공→해제, 관리 화면 폰트 4종 로드
- 2026-09-14 v4 6차-A — 색·글자 (지시서 1·3·4·5·11·12, `work/p7_a.py` + 조정 `p7_a2.py`, 스크린샷 `work/shots/6a/`, 도구 `work/shot.py`+`shot.html` 헤드리스 크롬).
  ① 타임라인 '오늘 바뀐 것' = 파란 바탕(--blue)+흰 글자, 원래 상태색은 2px 테두리(확정 검정/잠정 회색/경고 벽돌), past 는 opacity .5. '잠정' 꼬리표(.tt) 삭제
  ③ 흐림 기준 isBlockPast(r,s0,date,nowM) 하나로 — 방문 즉시 / 미처리 시작+60분. 홀·룸·디스플레이 세 곳 공용
  ④ 오늘 아니면 상단바+body 검정(.topbar.notoday / body.notoday, notodayView()), 날짜 옆 '지난 날짜'/'D-n'(.nt-tag), '오늘' 버튼은 오늘이 아닐 때만 그림(.hold 자리 없음, 가운데 맞춤은 ::before 를 notoday 에만)
  ⑤ 영업시간 줄 hoursLineHtml(dh) 세 칸 grid — 대시보드(.tl-hours 대체)·마법사 공용. 좁은 곳(마법사 열 12px, 폰 한 줄+'영업시간' 라벨 생략) 조정
  ⑪ HANOK 로고 Pretendard 700 .18em  ⑫ 디스플레이 목록형 .tvl-mark 삭제
- 2026-09-14 v4 6차-B — 지시서 2·7·9·15 (`work/p7_b.py`, 스크린샷 `work/shots/6b/`, 상태 스크립트 `work/shots_b.py`).
  ② 예약 목록 .rrow 를 grid(12|52|92|72|88|118|1fr)로 — 전화 열 세로 정렬, 인원·룸·전화 같은 무게(--text-2 500), 룸 tag 색 제거(미배정만 벽돌 글자). 꼬리표는 .rr-rest 한 칸(있을 때만). 640px 이하 전화 둘째 줄·꼬리표 셋째 줄
  ⑦ (a) 예약률 시트 전용 커서 view.rateEnd + rateMove(n) — 닫으면 view.date 그대로 (b) saveRes·wzFinish 의 view.date 점프 삭제, 토스트 showToast/toastSaved — 다른 날짜면 '9/21(월) 예약 저장됨 · 보기', 보는 날짜면 '저장됨'. 마법사는 완료 화면 닫을 때(closeWizardDone). gotoRes(설정→예약)는 유지
  ⑨ PIN .pdot 빈 원 테두리 + 글자만(f1 명조900 / f2 Pretendard700 / f3 명조900 italic / f4 Pretendard400), Nanum Myeongjo 제거
  ⑮ delRes 확인창에 resLine(rec) '9/14(월) 12:30 · 노아린 · 6명 · 초선 룸'
  · 확인(브라우저 JS): 시트 주 2번 이동 후 닫기 → 날짜 유지 / 수정 시트에서 +7일로 저장 → 날짜 유지·토스트·'보기'로 이동 / 완료 화면 닫기 토스트. 헤드리스 캡처는 토스트 글자가 안 찍힘(브라우저에선 정상)
- 2026-09-14 v4 6차-C — 인트로 (지시서 10, `work/p7_c.py`, 스크린샷 `work/shots/6c/`, 시점 캡처는 `shot.py` 의 가상 시간 예산 인자).
  · 글자 clamp(36px,6.4vw,72px). 단계 t0=380 gap=260(5글자 1.3초), 마지막 글자 뒤 700ms 에 끝(총 약 2.4초). blur 전환 .55→.7s, 바탕 전환 1.1→.7s
  · 낙관(.intro-seal)·소제(.intro-sub)·introSeal() 삭제 — 마지막 장면은 어서오세요 + 창호
  · 바탕 3단계: 새 레이어 .intro-mid(#3A2A1E 나무색) opacity=min(1,p·2), .intro-ko·창호 opacity=max(0,(p−.5)·2). introBg(n) 한 함수로 introStep/renderIntro 공용
  · 확인: 0.6s 빨강+歡迎光臨 / 1.1s 나무색+어서光臨 / 1.6s 한지+창호+어서오세 / 2.1s 완성. 430 은 브라우저에서 첫 글자 선명 확인(헤드리스 캡처만 blur 잔상)
- 2026-09-14 v4 6차-D — 예약률 좌석 수 스냅샷 (지시서 6, `work/p7_d.py`, 스크린샷 `work/shots/6d/`).
  · `s.snapshots[날짜] = {rooms, hallTables}` — migrate 가 없으면 {}. takeSnapshot(): loadData 끝·1분 타이머에서 날짜 바뀜 감지·applySettings 에서 호출. 빠진 지난 날짜(마지막 스냅샷 다음 날부터, 없으면 30일 전부터)는 오늘 설정으로 채움, 오늘은 매번 덮어씀, 366일 지난 것 삭제
  · dayStat: date<오늘 이고 스냅샷 있으면 그 수치가 분모. 사용 중지(blocks)는 룸·홀 모두 '잠긴 시간(영업시간 안)×좌석 수' 를 분모에서 뺌. 스냅샷 날짜에서 지금은 없는 룸의 예약도 룸 사용으로 셈(isRoomSeat)
  · 단위 테스트(브라우저 콘솔): 룸 '조조' 삭제 → 3일 전 [13%, 룸 25%, 좌석 29] 그대로, 오늘 29→28 좌석·룸 38→40%, 이틀 뒤 19→21%. 어제 룸 하나 하루 종일 잠금 → 룸 29→33%. 2020년 스냅샷 자동 삭제. 스냅샷 31일치 생성 확인
- 2026-09-14 v4 6차-E — 뒤로가기 보호 + 빠른 입력 (지시서 14·13, `work/p7_e.py` + 보강 `p7_e2.py`(delRes histPop) `p7_e3.py`(back 중복 방지), 스크린샷 `work/shots/6e/`).
  ⑭ openWizard/openRes 에서 pushState({wz:1}) 한 칸(histPush), popstate 에서 WZ 또는 res 시트가 열려 있으면 "입력 중인 예약이 있습니다. 나갈까요?" — 취소면 칸 다시, 확인이면 닫기. 정상 닫기(closeWizard/closeWizardDone/closeSheet/saveRes/delRes)는 histPop 으로 칸 회수. back() 비동기 중복은 HIST_PENDING 으로 막음. beforeunload 는 같은 조건에서 returnValue="" (문구는 브라우저 것). 디스플레이·검색 등 다른 시트 제외
  ⑬ 마법사 1단계 아래 '한 화면으로 입력'(.wz-quick) → openQuick(): WZ 닫고 sheetRes 를 빈 예약(마법사 날짜, 시각·인원·경로 비움)으로. 제목 '빠른 입력', 버튼 '등록'. 등록은 마법사와 공유 함수 confirmNewRes(같은 번호·노쇼 확인) → createReservation(등록 기록·문자 흉내·push·로그·잠정 배정). saveRes 의 새 예약 분기는 4줄
  · 확인(브라우저): 마법사/빠른 입력으로 만든 예약 키 목록 동일(26개), changes/updatedAt/source/allergyChecked/seatPref 동일. 뒤로가기 6단계 시나리오 전부 통과, 주소 유지
- 2026-09-14 v4 6차-F — 재아 검토 뒤 손질 (`work/p7_f.py`, 스크린샷 `work/shots/6f/`).
  · 타임라인 범례에 '오늘 변동'(.lgsw.chg) 추가 · 변동 블록 테두리 2→4px, 잠정은 점선(잠정+경고 = 점선 벽돌)
  · 코스 선택 − 버튼(.cminus, dropCourse) 부활 · PIN 글자 40px 로 원을 대체(f1 명조900 / f2 고딕 이탤릭 / f3 외곽선 명조 / f4 가는 고딕 -10°)
  · '오늘' 버튼·goToday·'지난 날짜'/'D-n'(.nt-tag) 삭제 — 날짜를 눌러 달력에서 고름 · 인트로 t0 160·gap 200·끝 +600 (총 약 1.8초), 전환 .55s
  · **광고 영상**: v4/ad.mp4 → v4/screen/ad.mp4 로 이동(adUrl 이 screen/ 을 붙이므로 여기 있어야 재생됨). 로컬 서버에서 목록형 재생 확인. ※ 134MB — GitHub 100MB 한도 초과라 배포 전 재인코딩 필요(ffmpeg 없음)
- 2026-09-14 v4 6차-G — 재아 검토 2 (`work/p7_g.py`, 스크린샷 `work/shots/6g/`).
  · 변동 표시를 '블록 전체 파랑 + 상태색 테두리' → **글자 영역만 파란 칩(.chg-chip)** 으로. 블록 바탕·테두리는 원래 상태 그대로(확정 먹색 / 잠정 점선 회색 / 경고 벽돌 / 잠정+경고 점선 벽돌) → 변동이 상태를 덮지 않아 세 가지가 한 블록에서 다 읽힘. 범례 견본은 파랑만
  · PIN 글자 40 → 30px
- 2026-09-14 v4 6차-H — 재아 검토 3 (`work/p7_h.py`, 스크린샷 `work/shots/6h/`).
  · 잠정 = 색 대신 **빗금 무늬 + 점선 테두리**(background-image, 흰 34%). 바탕색은 상태 그대로 → 먹색+빗금 = 잠정 확정, 벽돌+빗금 = 잠정 경고, 지난 것은 밝은 회색에 검은 빗금. 모든 블록 background 를 background-color 로(단축 속성이 빗금을 지움). 범례 견본도 먹색+빗금
  · 영업시간 줄을 그래프 카드에서 빼서 바로 아래 별도 카드(.hours-card)로
- 2026-09-14 v4 6차-H 보강 — 변동 칩 높이 15→12px·글자 10px (블록을 거의 채워 어색하다는 평)
- 2026-09-14 v4 6차-I — 수정 시트 저장 전 확인(saveIssues)에 resWarn 의 '성인 없음·유아의자 초과·룸·코스 아님·코스 미확정·코스 인원 부족' 추가 (`work/p7_i.py`). 유아=총 인원으로 저장 시 확인창 없이 경고 예약이 되던 것
- 2026-09-14 v4 6차-J — 예약률 시트 제목 기간 14일 → 21일(그래프와 일치) (`work/p7_j.py`)
