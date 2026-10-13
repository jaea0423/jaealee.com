# -*- coding: utf-8 -*-
# 등록(신랑신부) · 설정(신랑신부) · 요청(축의대 담당자가 받는 요청서)
from pages import COUPLE_CAP, BRAND_CAP, flow

# ---------------------------------------------------------------- 1. 등록
REGISTER = dict(title='축의지기 화면 시안', cap=BRAND_CAP, body='''
    <div class="top"><span class="sp"></span>''' + flow(0) + '''</div>

    <section class="card hero">
      <div class="eb">FOR NEWLYWEDS</div>
      <h1>봉투 접수부터 정산까지,<br>축의대를 노트북 한 대로</h1>
      <p>축의대 담당자는 이름과 금액만 넣으면 됩니다. 식권 수와 현금 합계는 자동으로 맞춰 보고, 예식이 끝나면 신랑신부가 명부를 바로 받아 봅니다.</p>
      <div class="price"><b>9,900원</b><span>예식 1건 · 등록과 준비는 무료 · 결제는 축의대를 여는 날 한 번</span></div>
    </section>

    <div class="grid2" style="grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)">
      <form class="card" id="reqForm" novalidate autocomplete="off">
        <div class="ch"><div><h3>예식 등록</h3><p>신랑신부가 함께 쓰는 예식 하나를 만듭니다.</p></div></div>
        <div class="form2">
          <div class="field"><label class="lab" for="rGroom">신랑 이름</label><input class="inp sm" id="rGroom" value="이용범"></div>
          <div class="field"><label class="lab" for="rBride">신부 이름</label><input class="inp sm" id="rBride" value="김홍매"></div>
          <div class="field"><label class="lab" for="rDate">예식 날짜</label><input class="inp sm" id="rDate" type="date" value="2000-04-16"></div>
          <div class="field"><label class="lab" for="rTime">예식 시간</label><input class="inp sm" id="rTime" type="time" value="13:00"></div>
          <div class="field full"><label class="lab" for="rPlace">예식장</label><input class="inp sm" id="rPlace" value="신라호텔 영빈관"></div>
          <div class="field full"><div class="lab"><label for="rMail">이메일</label><span class="hint">결과 안내를 받을 곳</span></div><input class="inp sm" id="rMail" type="email" placeholder="couple@example.com"></div>
          <label class="agree full"><input type="checkbox" id="rAgree">하객 명단과 축의금액을 저장하는 데 동의합니다. 데이터는 암호화돼서 저장되며, 예식일로부터 3개월 뒤 영구삭제됩니다.</label>
        </div>
        <button type="submit" class="save foot-act">예식 만들기 (무료)</button>
      </form>

      <section class="card">
        <div class="ch"><div><h3>이렇게 진행됩니다</h3><p>결제는 5단계 진행에서 한 번입니다.</p></div></div>
        <div class="steps fill">
          <div><span class="k">1</span><span><b>등록</b><small>신랑신부 · 예식 정보 넣기</small></span><span class="pill wait">무료</span></div>
          <div><span class="k">2</span><span><b>설정</b><small>신랑신부 · 담당자·식권·그림</small></span><span class="pill wait">무료</span></div>
          <div><span class="k">3</span><span><b>요청</b><small>신랑신부 → 축의대 담당자에게 부탁</small></span><span class="pill wait">무료</span></div>
          <div><span class="k">4</span><span><b>준비</b><small>축의대 담당자 · 가이드 읽기</small></span><span class="pill wait">무료</span></div>
          <div><span class="k paid">5</span><span><b>진행</b><small>축의대 담당자 · 예식 당일 접수</small></span><span class="pill live" style="animation:none">9,900원</span></div>
          <div><span class="k">6</span><span><b>현황</b><small>신랑신부·혼주 · 실시간 확인</small></span><span></span></div>
          <div><span class="k">7</span><span><b>결과</b><small>신랑신부 · 명부 확인·내려받기</small></span><span></span></div>
        </div>
      </section>
    </div>
''', script='''
  $('#reqForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var need = [['rGroom', '신랑 이름'], ['rBride', '신부 이름'], ['rDate', '예식 날짜'], ['rPlace', '예식장'], ['rMail', '이메일']];
    for (var i = 0; i < need.length; i++) { var el = $('#' + need[i][0]); if (!el.value.trim()) return alertPop(need[i][1] + '이(가) 비어 있습니다', need[i][1] + '을(를) 넣어 주세요.', el); }
    if (!$('#rAgree').checked) return alertPop('저장 동의가 필요합니다', '하객 명단과 축의금액을 저장하려면 동의가 필요합니다. 데이터는 암호화돼서 저장되며, 예식일로부터 3개월 뒤 영구삭제됩니다.', $('#rAgree'));
    openModal('예식을 만들었습니다', '', '<p class="amsg">' + esc($('#rGroom').value) + ' &amp; ' + esc($('#rBride').value) + ' 예식이 만들어졌습니다. 이제 설정 화면에서 축의대를 준비합니다.</p><div class="mbtns"><a class="save" href="../setup/index.html" style="display:grid;place-items:center;text-decoration:none">설정 화면으로</a></div>');
    $('#modal').classList.add('alert');
  });
''')

# ---------------------------------------------------------------- 2. 설정
def tbdlab(f, text, for_=None):
    tag = 'label for="%s"' % for_ if for_ else 'span'
    close = 'label' if for_ else 'span'
    return '<div class="lab"><%s>%s <span class="chg" data-f="%s" hidden title="요청서를 보낸 뒤 바뀜">변동</span></%s><button type="button" class="tbd" data-f="%s" aria-pressed="false">미정</button></div>' % (tag, text, f, close, f)

SETUP = dict(title='축의지기 설정', cap=COUPLE_CAP, body='''
    <div class="top"><span class="role">신랑신부</span><span class="chip">요청서 보냄 · 10월 1일</span><span class="sp"></span>''' + flow(1) + '''</div>

    <section class="card">
      <div class="ch"><div><h3>예식 전 준비</h3><p>아직 정해지지 않은 것은 미정으로 두어도 됩니다. 축의대를 열기 전까지만 채우면 됩니다.</p></div><span class="pill wait" id="readyPill"></span></div>
      <div class="checks" id="checks"></div>
      <div class="bar"><i id="bar"></i></div>
      <div class="chgbox" id="chgbox" hidden><b>요청서를 보낸 뒤 바뀐 것</b><span id="chglist"></span><small>담당자 요청서와 진행 화면에도 표시됩니다.</small></div>
    </section>

    <div class="grid2">
      <section class="card">
        <div class="ch"><div><h3>축의대 담당</h3><p>구분마다 4명까지. 아직 정하지 않은 쪽은 비워 두세요.</p></div><a class="btn2" href="../request/index.html" style="display:inline-grid;place-items:center;text-decoration:none">요청서 미리 보기</a></div>
        <div class="sub">
          <div class="lab"><span>신랑측 <span class="chg" data-f="staffG" hidden title="요청서를 보낸 뒤 바뀜">변동</span></span><span class="hint" id="staffGn"></span></div>
          <div class="staff" id="staffG"></div>
          <button type="button" class="addrow" data-add="G">+ 담당 추가</button>
        </div>
        <div class="sub">
          <div class="lab"><span>신부측 <span class="chg" data-f="staffB" hidden title="요청서를 보낸 뒤 바뀜">변동</span></span><span class="hint" id="staffBn"></span></div>
          <div class="staff" id="staffB"></div>
          <button type="button" class="addrow" data-add="B">+ 담당 추가</button>
        </div>
      </section>

      <section class="card">
        <div class="ch"><div><h3>예식 당일</h3><p>예식장과 합의되는 대로 채워 주세요.</p></div></div>
        <div class="form2">
          <div class="field">''' + tbdlab('arrive', '도착 시간', 'arrive') + '''<input type="time" class="inp sm" id="arrive" value="12:10"></div>
          <div class="field">''' + tbdlab('spot', '축의대 자리', 'spot') + '''<input class="inp sm" id="spot" placeholder="예: 영빈관 1층 로비"></div>
          <div class="field full">''' + tbdlab('hand', '인계받을 분') + '''<div class="srow two"><input class="inp sm" id="handN" placeholder="이름" value="이정수"><input class="inp sm" id="handR" placeholder="관계 (예: 신랑 아버지)" value="신랑 아버지"></div></div>
          <div class="field">''' + tbdlab('tkG', '신랑측 식권', 'tkG') + '''<div class="amtbox"><input class="inp sm" id="tkG" inputmode="numeric" value="230"><span class="unit">장</span></div></div>
          <div class="field">''' + tbdlab('tkB', '신부측 식권', 'tkB') + '''<div class="amtbox"><input class="inp sm" id="tkB" inputmode="numeric" placeholder="미정"><span class="unit">장</span></div></div>
          <div class="field full"><div class="lab"><span>입력 방식 <span class="chg" data-f="mode" hidden title="요청서를 보낸 뒤 바뀜">변동</span></span></div>
            <div class="seg" id="mode" style="grid-template-columns:1fr 1fr;margin:0"><button type="button" aria-pressed="true" data-m="live">현장에서 금액까지</button><button type="button" aria-pressed="false" data-m="later">금액은 나중에</button></div>
            <small class="muted" id="modeNote">봉투를 받는 자리에서 금액까지 넣습니다. 정산이 바로 끝납니다.</small>
          </div>
        </div>
      </section>
    </div>

    <div class="grid2">
      <section class="card">
        <div class="ch"><div><h3>배경 그림</h3><p>축의대와 현황 화면 뒤에 깔립니다. 6가지 중 하나를 고릅니다.</p></div><span class="chip" id="bgName"></span></div>
        <div class="bgpick fill" id="bgpick"></div>
      </section>
      <section class="card">
        <div class="ch"><div><h3>혼주 현황 열람</h3><p>켜면 혼주도 현황 화면을 볼 수 있습니다. 혼주마다 PIN이 발급됩니다.</p></div><button type="button" class="switch" id="swParent" role="switch" aria-checked="true" aria-label="혼주 열람"></button></div>
        <div id="parentBox">
          <div class="staff" id="parents"></div>
          <button type="button" class="addrow" data-addp>+ 혼주 추가</button>
        </div>
        <p class="muted foot-act" style="font-size:12.5px;margin:12px 0 0">PIN 입장 화면은 개발 마지막에 붙습니다.</p>
      </section>
    </div>

    <section class="card">
      <div class="ch"><div><h3>축의대 열기</h3><p>예식 당일 축의대 화면을 쓰려면 결제가 필요합니다. 미정을 모두 채운 뒤 열 수 있습니다.</p></div><span class="pill wait" id="payPill">결제 전</span></div>
      <div class="payrow">
        <div>
          <div class="row"><span>예식 1건</span><b>9,900원</b></div>
          <div class="row"><span>추천 코드</span><span class="refwrap"><input class="inp sm" id="ref" placeholder="예: HONG-2K4F"><button type="button" class="btn2" id="refBtn">적용</button></span></div>
          <div class="row" id="refRow" hidden><span>추천 할인</span><b style="color:var(--gold-d)">− 2,000원</b></div>
          <div class="row"><span>결제 금액</span><b class="big" style="font-size:24px" id="payAmt">9,900원</b></div>
        </div>
        <div class="payact">
          <button type="button" class="save" id="payBtn" style="margin-top:0">결제하고 축의대 열기</button>
          <small class="muted" id="payNote"></small>
          <div class="confirm-box" id="payConfirm" hidden>시안에서는 실제 결제가 일어나지 않습니다. 결제를 마친 것으로 처리할까요?
            <div class="btns"><button type="button" class="no" id="payNo">취소</button><button type="button" class="yes" id="payYes">결제 완료로 보기</button></div></div>
        </div>
      </div>
    </section>
''', script='''
  /* 요청서를 보낸 시점의 값(예시). 그 뒤 달라진 칸에 "변동"이 붙고, 요청서·진행 화면에도 같은 내용이 보인다 */
  var SENT = { staffG: '이재훈·사촌, 이민지·사촌', staffB: '', arrive: '12:10', spot: '', hand: '', tkG: '200', tkB: '', mode: 'live' };
  var LABEL = { staffG: '신랑측 담당', staffB: '신부측 담당', arrive: '도착 시간', spot: '축의대 자리', hand: '인계받을 분', tkG: '신랑측 식권', tkB: '신부측 식권', mode: '입력 방식' };
  var UNIT = { tkG: '장', tkB: '장' };
  var tbd = { arrive: false, spot: true, hand: false, tkG: false, tkB: true };
  var staff = { G: [['이재훈', '사촌'], ['이민지', '사촌']], B: [] };
  var parents = [['신랑 아버지', '이정수', '482915'], ['신부 어머니', '박정희', '730264']];
  var parentOn = true, mode = 'live', paid = false, bg = 3, ref = false;
  var REL = ['신랑 아버지', '신랑 어머니', '신부 아버지', '신부 어머니'];
  function rnd() { return String(Math.floor(100000 + Math.random() * 900000)); }

  function val(f) {
    if (f === 'staffG' || f === 'staffB') return staff[f.slice(-1)].filter(function (r) { return r[0].trim(); }).map(function (r) { return r[0].trim() + (r[1].trim() ? '·' + r[1].trim() : ''); }).join(', ');
    if (f === 'hand') return tbd.hand ? '' : [$('#handN').value.trim(), $('#handR').value.trim()].filter(Boolean).join('·');
    if (f === 'mode') return mode;
    return tbd[f] ? '' : $('#' + f).value.trim();
  }
  var show = function (f, v) { return v ? v + (UNIT[f] || '') : '미정'; };
  function draw() {
    /* 변동 표시 */
    var ch = [];
    Object.keys(SENT).forEach(function (f) {
      var now = val(f), diff = now !== SENT[f];
      document.querySelectorAll('.chg[data-f="' + f + '"]').forEach(function (t) { t.hidden = !diff; });
      if (diff) ch.push(LABEL[f] + ' ' + show(f, SENT[f]) + ' → ' + show(f, now));
    });
    $('#chgbox').hidden = !ch.length;
    $('#chglist').textContent = ch.join(' · ');
    /* 미정 버튼·칸 상태 */
    Object.keys(tbd).forEach(function (f) {
      var b = document.querySelector('.tbd[data-f="' + f + '"]'); b.setAttribute('aria-pressed', tbd[f]);
      if (f === 'hand') { $('#handN').disabled = $('#handR').disabled = tbd.hand; }
      else { var el = $('#' + f); el.disabled = tbd[f]; }
    });
    /* 체크 목록 */
    var C = [
      ['예식 정보', 'ok'],
      ['축의대 담당', val('staffG') && val('staffB') ? 'ok' : 'tbd'],
      ['당일 정보', val('arrive') && val('spot') && val('hand') ? 'ok' : 'tbd'],
      ['식권 장수', val('tkG') && val('tkB') ? 'ok' : 'tbd'],
      ['배경 그림', 'ok'],
      ['결제', paid ? 'ok' : 'pay']
    ];
    var n = C.filter(function (c) { return c[1] === 'ok'; }).length, left = C.filter(function (c) { return c[1] === 'tbd'; }).length;
    $('#checks').innerHTML = C.map(function (c) { return '<div class="' + (c[1] === 'ok' ? 'ok' : 'todo') + '"><b>' + c[0] + '</b><small>' + (c[1] === 'ok' ? '완료' : c[1] === 'tbd' ? '미정' : '결제 전') + '</small>' + (c[1] === 'tbd' ? '<small class="req">진행 전 필수</small>' : c[1] === 'pay' ? '<small class="req">미정을 채운 뒤</small>' : '') + '</div>'; }).join('');
    $('#readyPill').textContent = n + ' / ' + C.length + ' 완료'; $('#readyPill').className = 'pill ' + (n === C.length ? 'ok' : 'wait');
    $('#bar').style.width = Math.round(n / C.length * 100) + '%';
    /* 결제 */
    var can = !left && !paid;
    $('#payBtn').disabled = !can;
    $('#payNote').textContent = paid ? '축의대가 열렸습니다. 예식 당일 진행 화면을 쓸 수 있습니다.' : left ? '미정 ' + left + '개를 채우면 열 수 있습니다' : '결제 뒤에도 설정은 바꿀 수 있습니다';
    $('#payAmt').textContent = ref ? '7,900원' : '9,900원'; $('#refRow').hidden = !ref;
    $('#staffGn').textContent = staff.G.length ? staff.G.length + ' / 4명' : '아직 미정 · 진행 전 필수';
    $('#staffBn').textContent = staff.B.length ? staff.B.length + ' / 4명' : '아직 미정 · 진행 전 필수';
    document.querySelector('[data-add="G"]').hidden = staff.G.length >= 4;
    document.querySelector('[data-add="B"]').hidden = staff.B.length >= 4;
  }
  function drawStaff(side) {
    $('#staff' + side).innerHTML = staff[side].map(function (r, i) {
      return '<div class="srow"><input class="inp sm" value="' + esc(r[0]) + '" placeholder="이름" data-s="' + side + '" data-i="' + i + '" data-k="0"><input class="inp sm" value="' + esc(r[1]) + '" placeholder="관계 (예: 사촌)" data-s="' + side + '" data-i="' + i + '" data-k="1"><button type="button" class="xrow" data-del="' + side + '" data-i="' + i + '" aria-label="담당 빼기">×</button></div>';
    }).join('');
  }
  function drawParents() {
    $('#parentBox').hidden = !parentOn;
    $('#parents').innerHTML = parents.map(function (p, i) {
      return '<div class="srow prow"><input class="inp sm" value="' + esc(p[0]) + '" placeholder="관계 (예: 신랑 아버지)" data-p="' + i + '" data-k="0"><input class="inp sm" value="' + esc(p[1]) + '" placeholder="이름" data-p="' + i + '" data-k="1"><span class="pinc" data-pin="' + i + '" title="눌러서 보기">PIN ••••••</span><button type="button" class="xrow" data-delp="' + i + '" aria-label="혼주 빼기">×</button></div>';
    }).join('') + (parents.length ? '' : '<p class="muted" style="margin:0;font-size:13.5px">혼주를 추가하면 PIN이 발급됩니다.</p>');
    document.querySelector('[data-addp]').hidden = parents.length >= 4;
  }
  var BGS = ['봄 들판', '호수 테라스', '요트', '한복', '겨울 설경', '밤 테라스'];
  function drawBg() {
    $('#bgpick').innerHTML = BGS.map(function (n, i) {
      return '<button type="button" class="bgt" data-bg="' + i + '" aria-pressed="' + (i === bg) + '" style="background-image:url(../bg/' + (i + 1) + '.jpg)"><span>' + n + (i === 3 ? '<small>기본</small>' : '') + '</span></button>';
    }).join('');
    $('#bgName').textContent = '지금: ' + BGS[bg];
    document.documentElement.style.setProperty('--img', 'url(../bg/' + (bg + 1) + '.jpg)');
  }

  document.addEventListener('click', function (e) {
    var t;
    if ((t = e.target.closest('.tbd'))) { var f = t.dataset.f; tbd[f] = !tbd[f]; if (!tbd[f]) { (f === 'hand' ? $('#handN') : $('#' + f)).focus(); } draw(); return; }
    if ((t = e.target.closest('[data-add]'))) { staff[t.dataset.add].push(['', '']); drawStaff(t.dataset.add); draw(); var last = $('#staff' + t.dataset.add).querySelector('.srow:last-child input'); if (last) last.focus(); return; }
    if ((t = e.target.closest('[data-del]'))) { staff[t.dataset.del].splice(+t.dataset.i, 1); drawStaff(t.dataset.del); draw(); return; }
    if ((t = e.target.closest('[data-addp]'))) { parents.push([REL[parents.length % 4], '', rnd()]); drawParents(); toast('혼주를 추가했습니다. PIN을 발급했습니다'); return; }
    if ((t = e.target.closest('[data-delp]'))) { parents.splice(+t.dataset.delp, 1); drawParents(); return; }
    if ((t = e.target.closest('[data-pin]'))) { var p = parents[+t.dataset.pin]; var hid = t.textContent.indexOf('•') > -1; t.textContent = hid ? 'PIN ' + p[2] : 'PIN ••••••'; return; }
    if ((t = e.target.closest('[data-bg]'))) { bg = +t.dataset.bg; drawBg(); toast(BGS[bg] + ' 그림으로 바꿨습니다'); return; }
  });
  document.addEventListener('input', function (e) {
    var el = e.target;
    if (el.dataset.s) { staff[el.dataset.s][+el.dataset.i][+el.dataset.k] = el.value; draw(); return; }
    if (el.dataset.p) { parents[+el.dataset.p][+el.dataset.k] = el.value; return; }
    if (el.id === 'tkG' || el.id === 'tkB') el.value = el.value.replace(/[^0-9]/g, '');
    if (['arrive', 'spot', 'handN', 'handR', 'tkG', 'tkB'].indexOf(el.id) > -1) draw();
  });
  document.addEventListener('change', function (e) { if (e.target.dataset.p) { parents[+e.target.dataset.p][+e.target.dataset.k] = e.target.value; } });
  $('#mode').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return; mode = b.dataset.m;
    this.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
    $('#modeNote').textContent = mode === 'live' ? '봉투를 받는 자리에서 금액까지 넣습니다. 정산이 바로 끝납니다.' : '현장에서는 이름과 식권만 받고, 금액은 예식 뒤 봉투를 열어 넣습니다. 하객이 몰릴 때 빠릅니다.';
    draw();
  });
  $('#swParent').addEventListener('click', function () { parentOn = !parentOn; this.setAttribute('aria-checked', parentOn); drawParents(); toast(parentOn ? '혼주 열람을 켰습니다' : '혼주 열람을 껐습니다'); });
  $('#refBtn').addEventListener('click', function () {
    var v = $('#ref').value.trim().toUpperCase();
    if (!v) { $('#ref').focus(); return; }
    if (v !== 'HONG-2K4F') { ref = false; draw(); toast('시안에서는 HONG-2K4F만 인식합니다'); return; }
    ref = true; draw(); toast('추천 코드를 적용했습니다 · 2,000원 할인');
  });
  $('#payBtn').addEventListener('click', function () { this.hidden = true; $('#payConfirm').hidden = false; });
  $('#payNo').addEventListener('click', function () { $('#payConfirm').hidden = true; $('#payBtn').hidden = false; });
  $('#payYes').addEventListener('click', function () {
    $('#payConfirm').hidden = true; $('#payBtn').hidden = false; paid = true; draw();
    $('#payPill').textContent = '결제 완료 · 축의대 열림'; $('#payPill').className = 'pill ok';
    toast('축의대를 열었습니다. 예식 당일 진행 화면을 쓸 수 있습니다');
  });
  drawStaff('G'); drawStaff('B'); drawParents(); drawBg(); draw();
''')

# ---------------------------------------------------------------- 3. 요청서 (축의대 담당자가 받는 화면)
REQUEST = dict(title='축의지기 요청', cap=COUPLE_CAP, body='''
    <div class="top"><span class="role">축의대 담당자에게</span><span class="chip">이용범 · 김홍매가 10월 1일에 보냄</span><span class="sp"></span>''' + flow(2) + '''</div>

    <section class="card hero">
      <div class="eb">A LITTLE FAVOR</div>
      <h1>재훈아, 민지야,<br>우리 결혼식 신랑측 축의대를 부탁해</h1>
      <p>노트북으로 이름이랑 금액만 넣으면 돼서 어렵지 않아. 시간이랑 할 일을 아래에 정리해 뒀어. 아직 정해지지 않은 건 정해지는 대로 여기에 다시 표시될 거야.</p>
      <p style="margin-top:10px;font-family:var(--ko);color:var(--ink)">— 이용범 · 김홍매</p>
    </section>

    <div class="chgbox strip"><b>요청서를 받은 뒤 바뀐 것</b><span>식권 200장 → 230장 (10월 5일) · 인계받을 분 미정 → 신랑 아버지 이정수 (10월 8일)</span></div>

    <div class="grid2">
      <section class="card">
        <div class="ch"><div><h3>언제, 어디서</h3></div></div>
        <div class="rows fill">
          <div class="row"><span>예식</span><b>2000. 4. 16. 일요일 오후 1시</b></div>
          <div class="row"><span>장소</span><b>신라호텔 영빈관</b></div>
          <div class="row"><span>도착</span><b style="color:var(--gold-d)">오후 12시 10분까지 · 예식 50분 전</b></div>
          <div class="row"><span>축의대 자리</span><b class="tbdv">미정 · 정해지면 알려 드릴게요</b></div>
          <div class="row"><span>끝나는 때</span><b>오후 2시 30분쯤 · 정산 후 인계</b></div>
          <div class="row"><span>인계받을 분</span><b>신랑 아버지 이정수 <span class="chg" title="미정이었다가 10월 8일에 정해짐">변동</span></b></div>
          <div class="row"><span>식권</span><b>230장 · 혼주가 전달 <span class="chg" title="200장에서 10월 5일에 바뀜">변동</span></b></div>
        </div>
      </section>

      <section class="card">
        <div class="ch"><div><h3>함께하는 분</h3><p>신랑측 축의대 · 두 분이 역할을 나눠 주세요.</p></div></div>
        <div class="rows fill">
          <div class="row"><span>이재훈</span><b>사촌</b></div>
          <div class="row"><span>이민지</span><b>사촌</b></div>
          <div class="row"><span class="muted" style="font-size:13px">받는 사람 1명 · 입력하는 사람 1명이 편합니다. 자세한 역할은 준비 가이드에 있습니다.</span></div>
          <div class="row"><span>노트북과 충전기</span><b class="pill wait">직접</b></div>
          <div class="row"><span>볼펜 (봉투에 순번 적기)</span><b class="pill wait">직접</b></div>
          <div class="row"><span>식권 230장 · 봉투 담을 가방</span><b class="pill ok">혼주 · 예식장 준비</b></div>
        </div>
      </section>
    </div>

    <section class="card">
      <div class="ch"><div><h3>하루 흐름</h3><p>예식 오후 1시 기준입니다.</p></div></div>
      <div class="tl">
        <div><b>12:10</b><strong>도착 · 식권 받기</strong><small>장수를 세어 화면에 확인</small></div>
        <div><b>12:30</b><strong>하객 몰림</strong><small>예식 30분 전부터 가장 바쁩니다</small></div>
        <div><b>13:00</b><strong>예식 시작</strong><small>늦게 오는 하객은 계속 받습니다</small></div>
        <div><b>14:20</b><strong>명부 마감 · 정산</strong><small>현금·식권 세고 제출</small></div>
      </div>
    </section>

    <section class="card closing">
      <div><div class="eb">TAKE YOUR TIME</div><h3>충분히 고민해 보시고, 승낙 여부는 신랑신부에게 직접 전해 주세요.</h3><p>맡기로 하셨다면 예식 전에 준비 가이드를 한 번 읽어 두시면 당일이 편합니다.</p></div>
      <a class="save" href="../guide/index.html" style="display:grid;place-items:center;text-decoration:none;margin:0;min-width:220px">준비 가이드 보기</a>
    </section>
''', script='')
