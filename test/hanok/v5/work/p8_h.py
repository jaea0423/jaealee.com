# -*- coding: utf-8 -*-
"""v5 7차-H (2026-09-14)
   1 정해진 비밀번호로만: 서버 설정이 없는 빌드는 잠금 화면에서 들어갈 수 없음(아무 PIN 통과 경로 삭제). build.py 는 prod 설정이 없으면 사이트 빌드에 dev 설정을 씀
   2 TV 광고 영상이 뜨기 전 로딩 표시(빙글) — 영상이 재생되면(playing) 사라짐. 영상 없음·오류·15초 넘으면도 사라짐
   3 '오늘로' → '오늘', 새로고침 왼쪽으로"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- 1. 설정 없는 빌드는 못 들어감 ----------
rep("""async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  /* 서버 미연결 — 개발용. 아무 번호나 통과 */
  logEvent("로그인 성공", "서버 미연결 · PIN 확인 안 함");
  AUTHED = true; PIN_BUF=""; PIN_ERR="";
  DATA._session = {authed:true, since:new Date().toISOString()};
  saveData();
  startIntro();
  render();
}""",
"""async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  /* 서버 설정이 없는 빌드 — PIN 을 확인할 곳이 없으므로 들어갈 수 없습니다 (재아 결정: 정해진 비밀번호로만).
     화면 확인용 스크린샷은 AUTHED 를 직접 켜서 찍습니다(work/shot.py) */
  PIN_BUF = ""; PIN_ERR = "서버 설정이 없는 빌드입니다. 들어갈 수 없습니다.";
  render();
}""")
rep("""        ${supaOn() ? "" : `<div class="lk-open"><b>서버 미연결 빌드</b> — 확인용이라 아무 번호나 통과합니다</div>`}""",
    """        ${supaOn() ? "" : `<div class="lk-open"><b>서버 설정이 없는 빌드</b> — supabase.dev.json 또는 supabase.prod.json 을 넣고 다시 빌드하세요</div>`}""")
rep("""   서버 미연결(설정 파일 없는 빌드): 개발·확인용이라 아무 번호나 통과시키고, 잠금 화면에 그렇다고 표시합니다.
   ★ 실서비스는 반드시 supabase.prod.json 을 넣고 빌드합니다 — 그러면 이 통과 경로는 코드상 닿지 않습니다. ★""",
"""   서버 설정이 없는 빌드: 들어갈 수 없습니다(7차-H). build.py 가 prod 설정이 없으면 dev 설정을 쓰므로 사이트에 설정 없는 빌드가 올라갈 일은 없습니다.""")
rep("""/* 서버 미연결 빌드에서만 뜹니다. 잠금이 풀려 있다는 사실이 눈에 보여야""",
    """/* 서버 설정이 없는 빌드에서만 뜹니다. 들어갈 수 없다는 사실이 눈에 보여야""")

# ---------- 2. TV 로딩 표시 ----------
rep("""                  onerror="this.parentNode.removeChild(this)"></video>` : ""}""",
    """                  onplaying="tvVideoReady(this)" onerror="tvVideoReady(this); this.parentNode.removeChild(this)"></video>
        <div class="tv-loading" aria-hidden="true"><i></i></div>` : ""}""", 2)
rep("""/* 오늘 남은 예약이 없고 설정(tvIdleFull, 기본 켬)이 켜져 있으면 목록/좌석표 대신 광고만 전체 화면 */""",
"""/* 광고 영상이 뜨기 전 빙글이 — 파일이 커서(29MB) 첫 프레임까지 몇 초 걸립니다. 재생이 시작되면(playing) 지웁니다.
   오류로 영상이 빠지면 사진이 드러나므로 그때도 지우고, 혹시 이벤트가 안 오면 15초 뒤에 지웁니다 */
function tvVideoReady(v){
  var box = v && v.parentNode, sp = box && box.querySelector(".tv-loading");
  if(sp && sp.parentNode) sp.parentNode.removeChild(sp);
}
setInterval(function(){
  document.querySelectorAll(".tv-loading").forEach(function(sp){
    var t = Number(sp.getAttribute("data-t") || 0) + 1; sp.setAttribute("data-t", t);
    if(t >= 15 && sp.parentNode) sp.parentNode.removeChild(sp);
  });
}, 1000);
/* 오늘 남은 예약이 없고 설정(tvIdleFull, 기본 켬)이 켜져 있으면 목록/좌석표 대신 광고만 전체 화면 */""")
rep("""/* 예약이 없을 때 광고만 — 날개 없이 영상이 화면 전체. 사진 위 어둡게 하는 막(veil)도 없음 */""",
"""/* 영상 로딩 표시 — 영상(z-index 2) 위, 가운데 빙글이. 회전은 transform 이지만 배율(zoom 규칙)과 무관합니다 */
.tv-loading{position:absolute; top:0; right:0; bottom:0; left:0; z-index:3; display:flex; align-items:center; justify-content:center; pointer-events:none}
.tv-loading i{display:block; width:calc(var(--tvu)*5); height:calc(var(--tvu)*5); border-radius:50%;
  border:calc(var(--tvu)*.45) solid rgba(246,238,221,.25); border-top-color:rgba(246,238,221,.9); animation:tvspin .9s linear infinite}
@keyframes tvspin{to{transform:rotate(360deg)}}
/* 예약이 없을 때 광고만 — 날개 없이 영상이 화면 전체. 사진 위 어둡게 하는 막(veil)도 없음 */""")

# ---------- 3. 오늘 버튼 ----------
rep("""          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘로</button>`}""",
"""          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>""")
rep("""  .b-today{order:4; flex:0 1 auto}
  .b-search{order:5; flex:0 1 auto}
  .b-add{order:6; flex:0 1 auto}""",
"""  .b-today{order:0; flex:0 1 auto}
  .b-search{order:5; flex:0 1 auto}
  .b-add{order:6; flex:0 1 auto}""")
rep("""/* '오늘로' 버튼 — 오늘이 아닐 때만 상단바 오른쪽(새로고침과 예약 검색 사이)에. 6차-F 에서 뺐다가 6차-K 에서 되살림 */""",
    """/* '오늘' 버튼 — 오늘이 아닐 때만 상단바 오른쪽(새로고침 왼쪽)에. 6차-F 에서 뺐다가 6차-K 에서 되살림, 7차-H 에서 자리·글자 조정 */""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_h 적용 완료")
