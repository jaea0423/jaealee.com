/* ============================================================
   대경빌 주차 관리자 화면 로직
   config.js 와 supabase-js, qrcode.js 가 먼저 로드되어 있어야 합니다.
   ============================================================ */
(function () {
  "use strict";

  var db = null;
  var cache = [];            // 차량 전체 목록
  var curTab = "active";
  var soonOnly = false;      // 만료 임박만 보기
  var editRow = null;
  var authMode = "pin";

  var $ = function (id) { return document.getElementById(id); };
  var B = CONFIG.BUILDING || "대경빌";

  $("bldg").textContent = B;
  document.title = B + " 주차 관리자";
  (function () {
    var d = new Date(), days = ["일","월","화","수","목","금","토"];
    $("today").innerHTML = fmt(d) + "<br>" + days[d.getDay()] + "요일";
  })();

  var VIEWS = ["login", "menu", "reg", "manage", "edit", "qr", "logs", "pin"];
  function show(name) {
    VIEWS.forEach(function (v) { $("view-" + v).classList.toggle("hidden", v !== name); });
    window.scrollTo(0, 0);
  }

  function say(boxId, text, kind) {
    var box = $(boxId);
    box.innerHTML = "";
    if (!text) { return; }
    var d = document.createElement("div");
    d.className = "msg " + (kind === "ok" ? "ok" : "err");
    d.textContent = text;
    box.appendChild(d);
  }

  /* =========================================================
     변경 기록 남기기 (실패해도 본 작업은 진행)
     ========================================================= */
  function logIt(action, v, detail) {
    if (!db) { return; }
    db.from("logs").insert({
      action: action,
      room:   v ? v.room : null,
      plate:  v ? v.plate : null,
      detail: detail || null
    }).then(function (r) { if (r.error) { console.warn("[log]", r.error); } });
  }

  /* =========================================================
     입력칸 도우미
     ========================================================= */
  function bindRoom(input) {
    input.addEventListener("blur", function () { input.value = normRoom(input.value); });
  }

  function bindPlate(input, preview, onChange) {
    function sync() {
      var cleaned = input.value.replace(/\s+/g, "");
      if (cleaned !== input.value) {
        var caret = input.selectionStart;
        input.value = cleaned;
        try { input.setSelectionRange(caret - 1, caret - 1); } catch (e) {}
      }
      preview.textContent = cleaned
        ? "저장될 형태: " + formatPlate(cleaned)
        : "띄어쓰기 없이 붙여서 입력하세요.";
      if (onChange) { onChange(cleaned); }
    }
    input.addEventListener("input", sync);
    input.sync = sync;
  }

  function bindChips(containerId, startId, endId, mode) {
    var chips = document.querySelectorAll("#" + containerId + " .chip");
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.classList.remove("on"); });
        c.classList.add("on");

        if (c.getAttribute("data-none")) { $(endId).value = ""; return; }

        var months = Number(c.getAttribute("data-m") || 0);
        var days   = Number(c.getAttribute("data-d") || 0);
        var from;

        if (mode === "extend" && $(endId).value) {
          var a = $(endId).value.split("-").map(Number);
          var d = new Date(a[0], a[1] - 1, a[2]);
          d.setDate(d.getDate() + 1);
          from = fmt(d);
        } else {
          from = $(startId).value || todayStr();
          $(startId).value = from;
        }
        $(endId).value = months ? addMonths(from, months) : addDays(from, days);
      });
    });
  }

  function bindToggle(btn, input) {
    btn.addEventListener("click", function () {
      var showing = input.type === "text";
      input.type = showing ? "password" : "text";
      btn.textContent = showing ? "보기" : "숨김";
      input.focus();
    });
  }

  bindToggle($("pw-toggle"), $("pw"));
  document.querySelectorAll(".pw-toggle-2").forEach(function (b) {
    bindToggle(b, $(b.getAttribute("data-for")));
  });
  bindRoom($("r-room")); bindRoom($("e-room"));
  bindPlate($("r-plate"), $("r-plate-preview"), checkDup);
  bindPlate($("e-plate"), $("e-plate-preview"));
  bindChips("r-chips", "r-start", "r-end", "set");
  bindChips("e-chips", "e-start", "e-end", "extend");

  document.querySelectorAll("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      var to = b.getAttribute("data-back");
      if (to === "manage") { loadAll().then(function () { show("manage"); }); }
      else { show(to); }
    });
  });

  /* =========================================================
     로그인 잠금 (이 기기에서만 - localStorage 기준)
     5회 실패마다 대기 시간이 늘고, 35회에서 잠깁니다.
     ========================================================= */
  var LOCK_KEY = "dgparking_lock";
  var PENALTY  = { 5: 30, 10: 60, 15: 180, 20: 600, 25: 3600, 30: 86400 };  // 초
  var LOCK_AT  = 35;
  var lockTimer = null;

  function getLock() {
    try {
      return JSON.parse(localStorage.getItem(LOCK_KEY)) || { fails: 0, until: 0, locked: false };
    } catch (e) { return { fails: 0, until: 0, locked: false }; }
  }
  function setLock(s) {
    try { localStorage.setItem(LOCK_KEY, JSON.stringify(s)); } catch (e) {}
  }
  function clearLock() {
    try { localStorage.removeItem(LOCK_KEY); } catch (e) {}
  }

  function noteFail() {
    var s = getLock();
    s.fails += 1;
    if (s.fails >= LOCK_AT) { s.locked = true; }
    else if (PENALTY[s.fails]) { s.until = Date.now() + PENALTY[s.fails] * 1000; }
    setLock(s);
    paintLock();
  }

  function secText(sec) {
    if (sec >= 3600) {
      var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60);
      return h + "시간" + (m ? " " + m + "분" : "");
    }
    if (sec >= 60) {
      var mm = Math.floor(sec / 60), ss = sec % 60;
      return mm + "분" + (ss ? " " + ss + "초" : "");
    }
    return sec + "초";
  }

  // 잠금 상태에 맞춰 화면을 그립니다. 잠겨 있으면 true 를 돌려줍니다.
  function paintLock() {
    var s = getLock();
    var blocked = s.locked || s.until > Date.now();

    $("login-lock").classList.toggle("hidden", !blocked);
    $("login-pin").classList.toggle("hidden", blocked || authMode !== "pin");
    $("login-pwd").classList.toggle("hidden", blocked || authMode === "pin");
    $("switch-wrap").classList.toggle("hidden", blocked);   // 구분점까지 같이 숨김

    clearInterval(lockTimer); lockTimer = null;

    if (!blocked) {
      if (s.fails > 0 && s.fails % 5 !== 0) {
        say("login-msg", "잘못된 시도 " + s.fails + "회. " +
            (5 - (s.fails % 5)) + "회 더 틀리면 잠시 잠깁니다.");
      }
      return false;
    }

    if (s.locked) {
      $("lock-title").textContent = "이 기기에서 잠겼습니다";
      $("lock-count").textContent = "잠김";
      $("lock-sub").textContent =
        "틀린 시도가 " + LOCK_AT + "회를 넘었습니다.\n" +
        "이 브라우저의 저장 데이터를 지우거나 다른 기기에서 접속해야 풀립니다.";
      say("login-msg", "");
      return true;
    }

    function tick() {
      var left = Math.ceil((getLock().until - Date.now()) / 1000);
      if (left <= 0) { clearInterval(lockTimer); paintLock(); return; }
      $("lock-title").textContent = "잠시 후 다시 시도할 수 있습니다";
      $("lock-count").textContent = secText(left);
      $("lock-sub").textContent = "잘못된 시도 " + getLock().fails + "회";
    }
    tick();
    lockTimer = setInterval(tick, 1000);
    say("login-msg", "");
    return true;
  }

  /* =========================================================
     로그인
     ========================================================= */
  var HINTS = {
    invalid_credentials:
      "비밀번호가 맞지 않습니다.\n" +
      "config.js 의 ADMIN_EMAIL 과 Supabase 계정 주소가 같은지도 확인해 주세요.",
    email_not_confirmed:
      "계정이 아직 '인증 대기' 상태라 로그인이 막혀 있습니다.\n" +
      "Supabase > Authentication > Users 에서 그 사용자를 지우고,\n" +
      "Add user 할 때 'Auto Confirm User' 를 켜고 다시 만들어 주세요.",
    email_provider_disabled:
      "Supabase 에서 이메일 로그인이 꺼져 있습니다.\n" +
      "Authentication > Sign In / Providers > Email 을 켜 주세요.",
    over_request_rate_limit: "시도가 너무 잦습니다. 잠시 후 다시 해 주세요.",
    validation_failed: "입력 형식이 올바르지 않습니다."
  };

  function authError(err) {
    var code = err.code || err.name || "";
    return (HINTS[code] || "로그인하지 못했습니다.")
         + "\n\n[원문] " + (err.message || "") + (code ? " (" + code + ")" : "");
  }

  /* ---- PIN 키패드 ---- */
  var pinBuf = "";
  var dotEls = Array.prototype.slice.call($("dots").querySelectorAll("i"));

  function drawDots() {
    dotEls.forEach(function (el, i) { el.classList.toggle("on", i < pinBuf.length); });
  }

  function pinShakeReset() {
    var dots = $("dots");
    dots.classList.add("shake");
    setTimeout(function () { dots.classList.remove("shake"); }, 380);
    pinBuf = "";
    drawDots();
  }

  function pinKey(k) {
    if (getLock().locked || getLock().until > Date.now()) { return; }
    if (k === "reset") { pinBuf = ""; drawDots(); return; }
    if (k === "back")  { pinBuf = pinBuf.slice(0, -1); drawDots(); return; }
    if (pinBuf.length >= 6) { return; }

    pinBuf += k;
    drawDots();
    if (pinBuf.length === 6) { setTimeout(function () { tryLogin(pinBuf, true); }, 120); }
  }

  document.querySelectorAll("#keypad .key").forEach(function (b) {
    b.addEventListener("click", function () { pinKey(b.getAttribute("data-k")); });
  });

  document.addEventListener("keydown", function (e) {
    if ($("view-login").classList.contains("hidden")) { return; }
    if ($("login-pin").classList.contains("hidden")) { return; }
    if (/^[0-9]$/.test(e.key)) { pinKey(e.key); }
    else if (e.key === "Backspace") { e.preventDefault(); pinKey("back"); }
    else if (e.key === "Escape") { pinKey("reset"); }
  });

  function tryLogin(secret, isPin) {
    if (paintLock()) { return; }
    if (!secret) { say("login-msg", "비밀번호를 입력해 주세요."); return; }
    if (!db) { return; }

    $("btn-login").disabled = true;

    db.auth.signInWithPassword({ email: CONFIG.ADMIN_EMAIL, password: secret })
      .then(function (res) {
        $("btn-login").disabled = false;
        if (res.error) {
          console.error("[login]", res.error);
          if (isPin) { pinShakeReset(); }
          $("pw").value = "";

          // 비밀번호가 틀린 경우만 실패로 셉니다 (설정 문제는 세지 않음)
          if (res.error.code === "invalid_credentials") {
            noteFail();
            if (!paintLock()) {
              var s = getLock();
              say("login-msg", "비밀번호가 맞지 않습니다. (" + s.fails + "회 틀림)");
            }
          } else {
            say("login-msg", authError(res.error));
          }
          return;
        }
        clearLock();
        pinBuf = ""; drawDots();
        $("pw").value = "";
        say("login-msg", "");
        show("menu");
        loadAll();
      })
      .catch(function (e) {
        $("btn-login").disabled = false;
        if (isPin) { pinShakeReset(); }
        say("login-msg", "서버에 연결하지 못했습니다.\n\n[원문] " + e.message);
      });
  }

  $("btn-login").addEventListener("click", function () { tryLogin($("pw").value, false); });
  $("pw").addEventListener("keydown", function (e) {
    if (e.key === "Enter") { tryLogin($("pw").value, false); }
  });

  function applyLoginMode(mode) {
    authMode = mode;
    $("btn-switch").textContent = (mode === "pin") ? "비밀번호로 입력" : "PIN 으로 입력";
    pinBuf = ""; drawDots();
    if (!paintLock() && mode !== "pin") { setTimeout(function () { $("pw").focus(); }, 50); }
  }

  $("btn-switch").addEventListener("click", function () {
    applyLoginMode(authMode === "pin" ? "password" : "pin");
  });

  $("btn-logout").addEventListener("click", function () {
    db.auth.signOut().then(function () { location.href = "index.html"; });
  });

  /* ---- 연결 확인 ---- */
  $("btn-diag").addEventListener("click", function () {
    if (!configReady()) { say("diag-msg", "config.js 가 비어 있습니다."); return; }

    var lines = ["주소: " + CONFIG.SUPABASE_URL, "관리자 이메일: " + CONFIG.ADMIN_EMAIL];
    say("diag-msg", "확인 중…", "ok");
    var head = { apikey: CONFIG.SUPABASE_ANON_KEY };

    fetch(CONFIG.SUPABASE_URL + "/auth/v1/settings", { headers: head })
      .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
      .then(function (a) {
        lines.push("", "· 인증 설정 응답: " + a.s);
        if (a.j && a.j.external) {
          lines.push("· 이메일 로그인 켜짐: " + (a.j.external.email ? "예" : "아니오 ← 원인일 수 있습니다"));
        }
        return fetch(CONFIG.SUPABASE_URL + "/rest/v1/vehicles_public?select=plate", { headers: head });
      })
      .then(function (r) {
        lines.push("· 차량 목록(뷰) 응답: " + r.status + (r.status === 200 ? " (정상)" : " ← setup.sql 실행 여부 확인"));
        return fetch(CONFIG.SUPABASE_URL + "/rest/v1/app_settings?select=key,value", { headers: head });
      })
      .then(function (r) {
        lines.push("· 설정 표 응답: " + r.status + (r.status === 200 ? " (정상)" : " ← setup.sql 을 다시 실행하세요"));
        var s = getLock();
        lines.push("· 이 기기 실패 기록: " + s.fails + "회" + (s.locked ? " (잠김)" : ""));
        say("diag-msg", lines.join("\n"), r.status === 200 ? "ok" : "err");
      })
      .catch(function (e) {
        lines.push("", "연결 실패: " + e.message);
        say("diag-msg", lines.join("\n"));
      });
  });

  /* =========================================================
     시작
     ========================================================= */
  if (!configReady()) {
    say("login-msg", "config.js 의 SUPABASE_URL / SUPABASE_ANON_KEY 가 비어 있습니다.");
  } else {
    db = makeClient();

    db.from("app_settings").select("value").eq("key", "auth_mode").maybeSingle()
      .then(function (res) {
        applyLoginMode((res.data && res.data.value === "password") ? "password" : "pin");
      });

    db.auth.getSession().then(function (res) {
      if (res.data.session) { show("menu"); loadAll(); }
    });
  }
  paintLock();

  /* =========================================================
     메뉴
     ========================================================= */
  $("btn-go-register").addEventListener("click", function () {
    ["r-room", "r-plate", "r-type", "r-memo", "r-end"].forEach(function (id) { $(id).value = ""; });
    $("r-start").value = todayStr();
    $("r-plate").sync();
    document.querySelectorAll("#r-chips .chip").forEach(function (c) { c.classList.remove("on"); });
    say("reg-msg", ""); say("r-dup", "");
    loadAll();
    show("reg");
  });

  $("btn-go-manage").addEventListener("click", function () {
    loadAll().then(function () { show("manage"); });
  });

  $("btn-go-pin").addEventListener("click", function () {
    $("p-new").value = ""; $("p-new2").value = "";
    say("pin-msg", "");
    setMode(authMode);
    show("pin");
  });

  /* =========================================================
     등록
     ========================================================= */
  // 같은 번호가 이미 등록되어 있으면 바로 알려 줍니다
  function checkDup(cleaned) {
    var box = $("r-dup");
    box.innerHTML = "";
    if (!cleaned) { return; }

    var plate = formatPlate(cleaned);
    var today = todayStr();
    var hit = cache.filter(function (v) { return !v.deleted && v.plate === plate; });
    if (!hit.length) { return; }

    var v = hit[0];
    say("r-dup",
        "이미 등록된 번호입니다.\n" + v.room + " · " + periodText(v)
        + " (" + STATUS_LABEL[statusOf(v, today)] + ")\n"
        + "그대로 등록할 수도 있지만, 기간 연장이라면 관리 화면에서 수정하는 편이 낫습니다.");
  }

  $("btn-reg-save").addEventListener("click", function () {
    var room  = normRoom($("r-room").value);
    var plate = formatPlate($("r-plate").value);
    var s = $("r-start").value;
    var e = $("r-end").value;

    if (!room)      { say("reg-msg", "호실을 입력해 주세요."); return; }
    if (!plate)     { say("reg-msg", "차량 번호를 입력해 주세요."); return; }
    if (!s)         { say("reg-msg", "시작일을 정해 주세요."); return; }
    if (e && e < s) { say("reg-msg", "종료일이 시작일보다 빠릅니다."); return; }

    $("r-room").value = room;

    var row = {
      room: room, plate: plate, start_date: s, end_date: e || null,
      car_type: $("r-type").value.trim() || null,
      memo:     $("r-memo").value.trim() || null
    };

    $("btn-reg-save").disabled = true;

    db.from("vehicles").insert(row).then(function (res) {
      $("btn-reg-save").disabled = false;
      if (res.error) {
        console.error("[insert]", res.error);
        say("reg-msg", "저장하지 못했습니다.\n\n[원문] " + res.error.message);
        return;
      }
      logIt("등록", row, s + " ~ " + (e || "미정"));
      location.href = "index.html";
    });
  });

  /* =========================================================
     관리 목록
     ========================================================= */
  function loadAll() {
    if (!db) { return Promise.resolve(); }
    return db.from("vehicles").select("*")
      .then(function (res) {
        if (res.error) { console.error("[select]", res.error); cache = []; }
        else { cache = res.data.slice().sort(byRoom); }   // 호실 숫자 순
        renderRows();
      });
  }

  document.querySelectorAll("#tabs .tab").forEach(function (t) {
    t.addEventListener("click", function () {
      document.querySelectorAll("#tabs .tab").forEach(function (x) { x.classList.remove("on"); });
      t.classList.add("on");
      curTab = t.getAttribute("data-s");
      soonOnly = false;
      renderRows();
    });
  });

  $("q").addEventListener("input", renderRows);

  function matchQuery(v, q) {
    if (!q) { return true; }
    var hay = [v.room, v.plate, v.plate.replace(/\s/g, ""), v.car_type || "", v.memo || ""]
              .join(" ").toLowerCase();
    return hay.indexOf(q) >= 0;
  }

  function renderRows() {
    var today = todayStr();
    var box = $("rows");
    var emptyBox = $("rows-empty");
    box.innerHTML = "";

    // 탭 개수
    var counts = { active: 0, upcoming: 0, expired: 0, deleted: 0 };
    var soonCount = 0;
    cache.forEach(function (v) {
      counts[statusOf(v, today)] += 1;
      if (isSoon(v, today)) { soonCount += 1; }
    });
    document.querySelectorAll("#tabs .tab").forEach(function (t) {
      t.querySelector(".n").textContent = counts[t.getAttribute("data-s")];
    });
    $("menu-manage-desc").textContent =
      "등록 중 " + counts.active + "대 · 만료 " + counts.expired + "대"
      + (soonCount ? " · 임박 " + soonCount + "대" : "");

    // 만료 임박 배너
    var bn = $("soon-banner");
    bn.innerHTML = "";
    if (soonCount > 0) {
      var d = document.createElement("div");
      d.className = "banner";
      var txt = document.createElement("span");
      txt.innerHTML = SOON_DAYS + "일 안에 만료되는 차량이 <b>" + soonCount + "대</b> 있습니다.";
      var btn = document.createElement("button");
      btn.textContent = soonOnly ? "전체 보기" : "보기";
      btn.addEventListener("click", function () {
        soonOnly = !soonOnly;
        if (soonOnly) {
          curTab = "active";
          document.querySelectorAll("#tabs .tab").forEach(function (x) {
            x.classList.toggle("on", x.getAttribute("data-s") === "active");
          });
        }
        renderRows();
      });
      d.appendChild(txt); d.appendChild(btn);
      bn.appendChild(d);
    } else {
      soonOnly = false;
    }

    var q = $("q").value.trim().toLowerCase();
    var list = cache.filter(function (v) {
      if (statusOf(v, today) !== curTab) { return false; }
      if (soonOnly && !isSoon(v, today)) { return false; }
      return matchQuery(v, q);
    });

    if (list.length === 0) {
      emptyBox.textContent = q ? "검색 결과가 없습니다." : "해당하는 차량이 없습니다.";
      emptyBox.classList.remove("hidden");
      return;
    }
    emptyBox.classList.add("hidden");

    list.forEach(function (v) {
      var st = statusOf(v, today);
      var left = daysLeft(v, today);

      var row = document.createElement("div");
      row.className = "row s-" + st;

      var open = document.createElement("button");
      open.className = "row-open";
      open.addEventListener("click", function () { openEdit(v); });

      var roomEl = document.createElement("span");
      roomEl.className = "row-room";
      roomEl.textContent = v.room;

      var main = document.createElement("div");
      main.className = "row-main";

      var p = document.createElement("div");
      p.className = "row-plate";
      p.textContent = formatPlate(v.plate);

      var sub = document.createElement("div");
      sub.className = "row-sub";
      sub.textContent = periodText(v) + (v.car_type ? " · " + v.car_type : "");

      main.appendChild(p); main.appendChild(sub);

      var badge = document.createElement("span");
      if (st === "active" && left !== null && left <= SOON_DAYS) {
        badge.className = "badge soon";
        badge.textContent = left <= 0 ? "오늘 만료" : left + "일 남음";
      } else {
        badge.className = "badge " + st;
        badge.textContent = STATUS_LABEL[st];
      }

      open.appendChild(roomEl);
      open.appendChild(main);
      open.appendChild(badge);
      row.appendChild(open);

      // 만료됐거나 임박한 차량에는 빠른 연장 버튼을 붙입니다
      if (st === "expired" || (st === "active" && left !== null && left <= SOON_DAYS)) {
        var acts = document.createElement("div");
        acts.className = "row-actions";
        [["1주", "d7"], ["1개월", "m1"]].forEach(function (kv) {
          var b = document.createElement("button");
          b.className = "mini";
          b.textContent = "＋" + kv[0];
          b.addEventListener("click", function (ev) {
            ev.stopPropagation();
            quickExtend(v, kv[1], b);
          });
          acts.appendChild(b);
        });
        row.appendChild(acts);
      }

      box.appendChild(row);
    });
  }

  function quickExtend(v, kind, btn) {
    var today = todayStr();
    var from = extendFrom(v, today);
    var end  = (kind === "d7") ? addDays(from, 7) : addMonths(from, 1);
    var label = (kind === "d7") ? "1주" : "1개월";

    btn.disabled = true;
    db.from("vehicles").update({ end_date: end }).eq("id", v.id).then(function (res) {
      btn.disabled = false;
      if (res.error) { alert("연장 실패: " + res.error.message); return; }
      logIt("연장", v, label + " 연장 · " + (v.end_date || "미정") + " → " + end);
      loadAll();
    });
  }

  /* =========================================================
     수정 / 삭제
     ========================================================= */
  function openEdit(v) {
    editRow = v;
    $("e-room").value  = v.room;
    $("e-start").value = v.start_date;
    $("e-end").value   = v.end_date || "";
    $("e-plate").value = (v.plate || "").replace(/\s+/g, "");
    $("e-plate").sync();
    $("e-type").value  = v.car_type || "";
    $("e-memo").value  = v.memo || "";
    $("e-created").textContent = fmtDateTime(v.created_at);
    $("e-updated").textContent = fmtDateTime(v.updated_at);
    document.querySelectorAll("#e-chips .chip").forEach(function (c) { c.classList.remove("on"); });
    say("edit-msg", "");

    $("btn-edit-delete").classList.toggle("hidden", v.deleted === true);
    $("deleted-actions").classList.toggle("hidden", v.deleted !== true);

    show("edit");
  }

  $("btn-edit-save").addEventListener("click", function () {
    var room  = normRoom($("e-room").value);
    var plate = formatPlate($("e-plate").value);
    var s = $("e-start").value;
    var e = $("e-end").value;

    if (!room || !plate || !s) { say("edit-msg", "호실·차량번호·시작일은 비울 수 없습니다."); return; }
    if (e && e < s) { say("edit-msg", "종료일이 시작일보다 빠릅니다."); return; }

    var before = periodText(editRow);
    var after  = s + " ~ " + (e || "미정");
    var bits = [];
    if (editRow.room !== room)   { bits.push("호실 " + editRow.room + "→" + room); }
    if (editRow.plate !== plate) { bits.push("번호 " + editRow.plate + "→" + plate); }
    if (before !== after)        { bits.push("기간 " + before + " → " + after); }

    update({
      room: room, plate: plate, start_date: s, end_date: e || null,
      car_type: $("e-type").value.trim() || null,
      memo:     $("e-memo").value.trim() || null
    }, "수정", bits.join(", ") || "내용 수정");
  });

  $("btn-edit-delete").addEventListener("click",  function () { update({ deleted: true }, "삭제"); });
  $("btn-edit-restore").addEventListener("click", function () { update({ deleted: false }, "복구"); });

  $("btn-edit-purge").addEventListener("click", function () {
    if (!confirm("이 차량 정보를 완전히 지웁니다. 되돌릴 수 없습니다. 계속할까요?")) { return; }
    var v = editRow;

    db.from("vehicles").delete().eq("id", v.id).then(function (res) {
      if (res.error) { say("edit-msg", "삭제 실패\n\n[원문] " + res.error.message); return; }
      logIt("영구삭제", v, periodText(v));
      loadAll().then(function () { show("manage"); });
    });
  });

  function update(patch, action, detail) {
    var v = editRow;
    db.from("vehicles").update(patch).eq("id", v.id).then(function (res) {
      if (res.error) {
        console.error("[update]", res.error);
        say("edit-msg", "실패\n\n[원문] " + res.error.message);
        return;
      }
      logIt(action, v, detail || null);
      loadAll().then(function () { show("manage"); });
    });
  }

  /* =========================================================
     변경 기록
     ========================================================= */
  $("btn-go-logs").addEventListener("click", function () {
    var box = $("logs"), empty = $("logs-empty");
    box.innerHTML = "";
    empty.textContent = "불러오는 중…";
    empty.classList.remove("hidden");
    show("logs");

    db.from("logs").select("*").order("at", { ascending: false }).limit(200)
      .then(function (res) {
        if (res.error) {
          empty.textContent = "기록을 불러오지 못했습니다. setup.sql 을 다시 실행했는지 확인해 주세요.";
          return;
        }
        if (!res.data.length) { empty.textContent = "아직 기록이 없습니다."; return; }
        empty.classList.add("hidden");

        res.data.forEach(function (g) {
          var el = document.createElement("div");
          el.className = "log";

          var t = document.createElement("time");
          t.textContent = fmtDateTime(g.at);

          var a = document.createElement("span");
          a.className = "act";
          a.textContent = g.action;

          var w = document.createElement("div");
          w.className = "what";
          var b = document.createElement("b");
          b.textContent = (g.plate || "") + (g.room ? " (" + g.room + ")" : "");
          w.appendChild(b);
          if (g.detail) {
            var d = document.createElement("span");
            d.textContent = " · " + g.detail;
            w.appendChild(d);
          }

          el.appendChild(t); el.appendChild(a); el.appendChild(w);
          box.appendChild(el);
        });
      });
  });

  /* =========================================================
     QR 코드
     ========================================================= */
  function defaultQrUrl() {
    return location.href.replace(/admin\.html.*$/, "index.html");
  }

  function makeQR() {
    var url = $("qr-url").value.trim();
    if (!url) { say("qr-msg", "주소를 입력해 주세요."); return; }
    say("qr-msg", "");

    var holder = $("qr-hidden");
    holder.innerHTML = "";
    try {
      new QRCode(holder, {
        text: url, width: 520, height: 520,
        colorDark: "#17202a", colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.M
      });
    } catch (e) {
      say("qr-msg", "QR 라이브러리를 불러오지 못했습니다. 인터넷 연결을 확인해 주세요.");
      return;
    }

    // qrcode.js 가 canvas 또는 img 를 만듭니다. 둘 다 대응합니다.
    setTimeout(function () {
      var src = holder.querySelector("canvas");
      if (src) { compose(src, url); return; }
      var img = holder.querySelector("img");
      if (!img) { say("qr-msg", "QR 을 만들지 못했습니다."); return; }
      if (img.complete) { compose(img, url); }
      else { img.onload = function () { compose(img, url); }; }
    }, 60);
  }

  // QR 위아래에 글씨를 얹어 인쇄용 그림 한 장으로 만듭니다
  function compose(src, url) {
    var c = $("qr-canvas");
    var W = c.width, H = c.height;
    var g = c.getContext("2d");
    var F = '"Pretendard Variable", Pretendard, -apple-system, "Malgun Gothic", sans-serif';

    g.fillStyle = "#ffffff";
    g.fillRect(0, 0, W, H);

    g.textAlign = "center";

    g.fillStyle = "#17202a";
    g.font = "800 52px " + F;
    g.fillText(B + " 주차", W / 2, 84);

    g.fillStyle = "#66707a";
    g.font = "500 28px " + F;
    g.fillText("등록 차량 확인", W / 2, 128);

    g.drawImage(src, (W - 520) / 2, 168, 520, 520);

    g.fillStyle = "#17202a";
    g.font = "700 34px " + F;
    g.fillText("휴대폰 카메라로 스캔하세요", W / 2, 746);

    g.fillStyle = "#98a2ac";
    g.font = "400 20px " + F;
    g.fillText(url, W / 2, 786);
  }

  $("btn-go-qr").addEventListener("click", function () {
    if (!$("qr-url").value) { $("qr-url").value = defaultQrUrl(); }
    show("qr");
    makeQR();
  });

  $("btn-qr-make").addEventListener("click", makeQR);

  $("btn-qr-save").addEventListener("click", function () {
    var c = $("qr-canvas");
    var a = document.createElement("a");
    a.download = B + "_주차_QR.png";
    a.href = c.toDataURL("image/png");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    say("qr-msg", "저장했습니다. 다운로드 폴더를 확인해 주세요.", "ok");
  });

  /* =========================================================
     비밀번호 / PIN 변경
     ========================================================= */
  var pickedMode = "pin";

  function setMode(m) {
    pickedMode = m;
    document.querySelectorAll("#mode-seg button").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-m") === m);
    });

    var isPin = (m === "pin");
    $("p-new-label").textContent = isPin ? "새 PIN" : "새 비밀번호";
    $("mode-hint").textContent = isPin
      ? "로그인 화면에 숫자 키패드가 뜨고, 6자리를 누르면 바로 들어갑니다."
      : "로그인 화면에 비밀번호 입력칸이 뜹니다.";
    $("rule-hint").textContent = isPin
      ? "숫자 6자리"
      : "8자 이상, 대문자·숫자·특수문자를 모두 포함";

    [$("p-new"), $("p-new2")].forEach(function (i) {
      i.value = "";
      if (isPin) { i.setAttribute("inputmode", "numeric"); i.setAttribute("maxlength", "6"); }
      else { i.removeAttribute("inputmode"); i.removeAttribute("maxlength"); }
    });
    say("pin-msg", "");
  }

  document.querySelectorAll("#mode-seg button").forEach(function (b) {
    b.addEventListener("click", function () { setMode(b.getAttribute("data-m")); });
  });

  function checkSecret(s, mode) {
    if (mode === "pin") {
      return /^[0-9]{6}$/.test(s) ? null : "PIN 은 숫자 6자리여야 합니다.";
    }
    var ok = s.length >= 8 && /[A-Z]/.test(s) && /[0-9]/.test(s) && /[^A-Za-z0-9]/.test(s);
    return ok ? null : "비밀번호는 8자 이상이면서 대문자·숫자·특수문자를 모두 포함해야 합니다.";
  }

  $("btn-pin-save").addEventListener("click", function () {
    var a = $("p-new").value, b = $("p-new2").value;

    if (a !== b) { say("pin-msg", "두 값이 서로 다릅니다."); return; }
    var bad = checkSecret(a, pickedMode);
    if (bad) { say("pin-msg", bad); return; }

    $("btn-pin-save").disabled = true;

    db.auth.updateUser({ password: a }).then(function (res) {
      if (res.error) {
        $("btn-pin-save").disabled = false;
        say("pin-msg", "변경 실패\n\n[원문] " + res.error.message);
        return;
      }
      return db.from("app_settings")
        .upsert({ key: "auth_mode", value: pickedMode }, { onConflict: "key" })
        .then(function (r2) {
          $("btn-pin-save").disabled = false;
          if (r2.error) {
            say("pin-msg", "비밀번호는 바뀌었지만 로그인 방식 저장에 실패했습니다.\n\n[원문] " + r2.error.message);
            return;
          }
          applyLoginMode(pickedMode);
          clearLock();
          $("p-new").value = ""; $("p-new2").value = "";
          say("pin-msg",
              (pickedMode === "pin" ? "PIN" : "비밀번호") + "으로 변경했습니다.\n다음 로그인부터 적용됩니다.",
              "ok");
        });
    });
  });

  setMode("pin");
})();
