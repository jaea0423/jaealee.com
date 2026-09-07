/* 앱 안에서 실행되는 화면 상태 스크립트 (shot.html 이 iframe 문서에 <script> 로 넣습니다)
   DATA / view / WZ 같은 전역이 let 으로 선언돼 있어 바깥(window.X)에서는 안 보이므로,
   이 파일처럼 앱과 같은 스코프에서 돌려야 합니다. */
(function(){
  /* 시각·IP 고정 — 언제 찍어도 같은 화면 */
  window.nowHM = function(){ return "13:20"; };
  CLIENT_IP = "unknown";

  function reset(){
    var today = todayStr();
    MODAL = null; WZ = null; INTRO = null; tmpRes = null;
    view.storeKey = "hanok"; view.tab = "dash"; view.date = today; view.form = null; view.calOpen = false;
    view.display = false; view.fromRoute = false; view.open = {list:false, rate:false}; view.bgIndex = 1;
    view.pickSeat = null; view.blkDraft = null; view.schedDraft = null;
    AUTHED = true; PIN_BUF = ""; PIN_ERR = "";
    DATA._ui.theme = "hanok"; DATA._ui.zoom = 110;
    DATA.hanok.settings.tempClosed = false;
    try { clearInterval(bgTimer); clearInterval(dispTimer); } catch (e) {}
    var cb = document.getElementById("crashbar"); if (cb) cb.parentNode.removeChild(cb);
    scrollMemo = null;
  }
  function firstId(){
    var today = todayStr();
    var l = DATA.hanok.reservations.filter(function(r){ return r.date === today && r.status === "확정" && r.roomId; });
    return l.length ? l[0].id : DATA.hanok.reservations[0].id;
  }
  var SKEYS = ["s_course","s_disp","s_etc","s_hours","s_policy","s_rules","s_seats","s_security","s_sms","s_source","s_zoom"];
  function wz(step, extra){
    openWizard(todayStr());
    WZ.step = step; WZ.source = "전화"; WZ.time = "18:00"; WZ.people = 4; WZ.seat = "r4";
    WZ.menuType = "코스"; WZ.courses = {"0|오":4}; WZ.name = "홍길동"; WZ.phone = "010-1234-5678";
    if (extra) Object.keys(extra).forEach(function(k){ WZ[k] = extra[k]; });
  }
  /* 스크린샷 4장: 대시보드(접이식 모두 펼침) · 마법사 3단계(좌석) · 설정(폴드 모두 펼침) · 예약 상세 시트 */
  var STATES = {
    dash:     function(){ view.open = {list:true, rate:true}; },
    wizard:   function(){ wz(3); },
    settings: function(){ view.tab = "settings"; SKEYS.forEach(function(k){ view.open[k] = true; }); },
    detail:   function(){ view.form = {type:"res", id:firstId()}; },
    /* 아래는 클래스 조합 수집에만 씁니다 */
    select:   function(){ view.storeKey = null; AUTHED = false; },
    lock:     function(){ AUTHED = false; PIN_BUF = "12"; },
    intro:    function(){ INTRO = {from:"歡迎光臨", to:"어서오세요", n:2}; },
    dash_basic: function(){ DATA._ui.theme = "basic"; view.open = {list:true, rate:true}; },
    dash_crash: function(){ showCrash(new Error("테스트")); },
    cal:      function(){ view.calOpen = true; },
    modal:    function(){ MODAL = {mode:"confirm", title:"제목", msg:"본문\n---\n둘째", tone:"warn", ok:"계속", cancel:"취소", res:function(){}}; },
    wiz0: function(){ wz(0); }, wiz1: function(){ wz(1,{time:"21:20"}); }, wiz2: function(){ wz(2,{customPeople:true, people:12, infants:1}); },
    wiz4: function(){ wz(4,{courseOpen:true}); }, wiz5: function(){ wz(5,{phone:"", phoneNone:true}); }, wiz6: function(){ wz(6); },
    wiz_done: function(){ wz(6); WZ.done = DATA.hanok.reservations.filter(function(r){ return r.roomId; })[0]; },
    sheet_mark: function(){ view.form = {type:"mark", id:firstId()}; },
    sheet_course: function(){ view.form = {type:"res", id:firstId()}; render(); tmpRes.courseOpen = true; tmpRes.menuType = "코스"; },
    sheet_unassigned: function(){ view.form = {type:"unassigned"}; },
    sheet_pick: function(){ view.form = {type:"pick", kind:"warn"}; },
    sheet_check: function(){ view.form = {type:"check"}; },
    sheet_search: function(){ view.form = {type:"search"}; },
    sheet_tables: function(){ view.form = {type:"tables", id:"h1"}; },
    sheet_num: function(){ view.form = {type:"num", key:"stayHours", title:"체류", min:1, max:6, ctx:{step:.5}, val:null}; },
    sheet_noshow: function(){ view.form = {type:"noshow"}; },
    sheet_pin: function(){ view.form = {type:"pin"}; },
    sheet_logs: function(){ view.form = {type:"logs"}; },
    sheet_smslog: function(){ view.form = {type:"smslog"}; },
    sheet_rate: function(){ view.form = {type:"rate"}; },
    sheet_sched: function(){ openSchedule(null); },
    sheet_ovr: function(){ view.form = {type:"ovr"}; },
    sheet_blocks: function(){ view.form = {type:"blocks", id:"r1"}; },
    display:  function(){ view.display = true; },
    display_lock: function(){ view.display = true; AUTHED = false; }
  };
  window.__states = Object.keys(STATES);
  window.__ready = function(){ return !!DATA; };
  window.__apply = function(name){ reset(); STATES[name](); render(); window.scrollTo(0, 0); };
  /* 요소마다 "자기 (태그.클래스들) | 조상 클래스들 | 조상 태그들" 을 남깁니다.
     CSS 순서 검사에서 ".tk b" 와 ".mockbar b" 처럼 조상이 다른 규칙이 같은 요소에 걸릴 수 없다는 것을 가리려면 조상 정보가 필요합니다 */
  window.__combos = function(){
    var els = document.querySelectorAll("body, body *"), out = {};
    for (var i = 0; i < els.length; i++) {
      var e = els[i]; if (e.tagName === "SCRIPT" || e.tagName === "STYLE") continue;
      var cls = (typeof e.className === "string" ? e.className : "").trim().split(/\s+/).filter(Boolean).sort();
      var anc = {}, ancTag = {}, p = e.parentNode;
      while (p && p.nodeType === 1) {
        ancTag[p.tagName.toLowerCase()] = 1;
        (typeof p.className === "string" ? p.className : "").trim().split(/\s+/).filter(Boolean).forEach(function(c){ anc[c] = 1; });
        p = p.parentNode;
      }
      out[e.tagName.toLowerCase() + "." + cls.join(".") + "|" + Object.keys(anc).sort().join(".") + "|" + Object.keys(ancTag).sort().join(".")] = 1;
    }
    return out;
  };
})();
