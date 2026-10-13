# -*- coding: utf-8 -*-
# 각 화면의 본문과 스크립트. build.py가 공통 틀(배경·왼쪽 사진 칸·시안 이동 막대)에 끼워 넣는다.

COUPLE_CAP = '''
      <div class="eb">WEDDING RECEPTION</div>
      <div class="couple"><div><small>신랑</small><b>이용범</b></div><span class="amp">&amp;</span><div><small>신부</small><b>김홍매</b></div></div>
      <div class="when"><b>2000. 4. 16. 일요일 오후 1시</b><br>신라호텔 영빈관</div>
      <span class="sample">시안 · 예시 데이터</span>'''

BRAND_CAP = '''
      <div class="eb">CHUKUIJIGI</div>
      <div class="couple"><div><b style="letter-spacing:.14em">축의지기</b></div></div>
      <div class="when">축의대를 노트북 한 대로</div>
      <span class="sample">시안</span>'''

def flow(active):
    names = ['등록', '설정', '요청', '준비', '진행', '현황', '결과']
    out = []
    for i, n in enumerate(names):
        if i < active: out.append('<span class="f-done" title="%s"><b>✓</b></span>' % n)
        elif i == active: out.append('<span class="f-on"><b>%d</b><em>%s</em></span>' % (i + 1, n))
        else: out.append('<span title="%s"><b>%d</b></span>' % (n, i + 1))
    return '<div class="flow" aria-label="진행 단계">' + '<i></i>'.join(out) + '</div>'

# ---------------------------------------------------------------- 1. 요청
# ---------------------------------------------------------------- 4. 현황
STATUS = dict(title='축의지기 현황', cap=COUPLE_CAP, body='''
    <div class="top"><span class="role" id="roleName">신랑신부 · 혼주</span><span class="pill live">실시간</span><div class="tabs" id="viewTabs" aria-label="볼 쪽"><button type="button" aria-pressed="true" data-v="all">신랑신부</button><button type="button" aria-pressed="false" data-v="groom">신랑측</button><button type="button" aria-pressed="false" data-v="bride">신부측</button></div><span class="sp"></span>''' + flow(5) + '''</div>

    <section class="stats" aria-label="전체 현황" style="grid-template-columns:repeat(3,1fr)">
      <div><small><span class="vlab">전체</span> 접수</small><b class="n" id="allCount">0</b></div>
      <div><small><span class="vlab">전체</span> 현금 <span class="meta">· 눌러서 보기</span></small><button type="button" class="veil hide" id="allVeil" style="text-align:left"><b class="n" id="allCash">0</b></button></div>
      <div><small>마지막 접수</small><b class="n" id="allLast">-</b></div>
    </section>

    <div class="grid2" style="grid-template-columns:minmax(0,1fr) minmax(0,1.05fr)">
      <div style="display:grid;gap:16px;grid-auto-rows:1fr">
        <section class="sidecard card" id="cardG"></section>
        <section class="sidecard card" id="cardB"></section>
      </div>
      <section class="card">
        <div class="ch"><div><h3>들어오는 봉투</h3><p>축의대에서 저장하는 대로 바로 나타납니다.</p></div><span class="chip" id="simNote" style="white-space:nowrap">시안 · 예시 자동 추가</span></div>
        <div class="feed" id="feed"></div>
      </section>
    </div>
''', script='''
  var R = { groom: seedRows('groom'), bride: seedRows('bride') };
  var submitted = { groom: false, bride: false };
  var START = { groom: 230, bride: 200 }, LEDGER = { groom: 3, bride: 0 };
  var live = function (s) { return R[s].filter(function (r) { return !r.x; }); };
  var cash = function (s) { return live(s).reduce(function (a, r) { return a + r.amt; }, 0); };
  var tk = function (s) { return live(s).reduce(function (a, r) { return a + r.tk; }, 0) + LEDGER[s]; };
  var shown = false, view = 'all';
  var sides = function () { return view === 'all' ? ['groom', 'bride'] : [view]; };
  function card(s) {
    var last = R[s][R[s].length - 1];
    return '<h4>' + (s === 'groom' ? '신랑측 · 이용범' : '신부측 · 김홍매') + (submitted[s] ? '<span class="pill ok">제출 완료</span>' : '<span class="pill live">접수 중</span>') + '</h4>' +
      '<p class="muted" style="margin:4px 0 0;font-size:13px">마지막 저장 ' + (last ? last.t : '-') + ' · 입력 기기 1대</p>' +
      '<div class="kpis"><div class="kpi"><small>접수</small><b>' + live(s).length + '<span>건</span></b></div>' +
      '<div class="kpi"><small>현금</small><b>' + (shown ? kor(cash(s)).replace(' 원', '') : '••••') + '<span>' + (shown ? '원' : '') + '</span></b></div>' +
      '<div class="kpi"><small>식권 남음</small><b>' + (START[s] - tk(s)) + '<span>장</span></b></div></div>' +
      '<div class="row" style="margin-top:12px;border-top:1px solid var(--line)"><span>마지막 봉투</span><b>' + (last ? (last.anon ? '무기명' : esc(last.name)) + ' · ' + kor(last.amt) + ' · ' + last.t : '-') + '</b></div>';
  }
  function feedHTML(r, isNew) {
    return '<div class="fi' + (isNew ? ' new' : '') + '"><time>' + r.t + '</time><span class="sd ' + (r.side === 'groom' ? 'g' : 'b') + '">' + (r.side === 'groom' ? '신랑측' : '신부측') + '</span><span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + (r.anon ? '무기명' : esc(r.name)) + (r.x ? ' <span class="tag x">취소</span>' : '') + '</span><b>' + kor(r.amt) + '</b></div>';
  }
  function draw(newRow) {
    $('#cardG').innerHTML = card('groom'); $('#cardB').innerHTML = card('bride');
    $('#cardG').hidden = view === 'bride'; $('#cardB').hidden = view === 'groom';
    document.querySelectorAll('.vlab').forEach(function (x) { x.textContent = { all: '전체', groom: '신랑측', bride: '신부측' }[view]; });
    var all = sides().reduce(function (a, s) { return a.concat(R[s]); }, []).sort(function (a, b) { return a.t < b.t ? 1 : -1; });
    $('#feed').innerHTML = all.map(function (r) { return feedHTML(r, r === newRow); }).join('');
    $('#allCount').innerHTML = sides().reduce(function (a, s) { return a + live(s).length; }, 0) + '<span>건</span>';
    $('#allCash').textContent = won(sides().reduce(function (a, s) { return a + cash(s); }, 0));
    $('#allLast').textContent = all[0] ? all[0].t : '-';
  }
  $('#viewTabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; view = b.dataset.v; this.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); draw(); });
  $('#allVeil').addEventListener('click', function () { shown = !this.classList.toggle('hide'); draw(); });
  var NAMES = ['김도윤', '이하준', '박서윤', '최지안', '정민서', '강유나', '조현우', '윤시우'], ni = 0, clock = 12 * 60 + 47;
  setInterval(function () {
    var s = Math.random() < .5 ? 'groom' : 'bride';
    if (ni >= NAMES.length) return;
    clock += 1;
    var r = { side: s, no: R[s].length + 1, name: NAMES[ni++], anon: false, amt: [50000, 50000, 100000, 30000][Math.floor(Math.random() * 4)], tk: 1, x: false, t: ('0' + Math.floor(clock / 60)).slice(-2) + ':' + ('0' + clock % 60).slice(-2) };
    R[s].push(r); draw(r);
  }, 6000);
  draw();
''')

# ---------------------------------------------------------------- 5. 결과
RESULT = dict(title='축의지기 결과', cap=COUPLE_CAP, body='''
    <div class="top"><span class="role">신랑신부</span><span class="chip">2000. 7. 16.까지 보관 후 삭제</span><span class="sp"></span>''' + flow(6) + '''</div>

    <section class="stats" aria-label="결과 요약" style="grid-template-columns:repeat(4,1fr)">
      <div><small>축의금 합계</small><b class="n" id="sAll">0</b></div>
      <div><small>신랑측</small><b class="n" id="sG">0</b></div>
      <div><small>신부측</small><b class="n" id="sB">0</b></div>
      <div><small>봉투 <span class="meta" id="sCountMeta"></span></small><b class="n" id="sCount">0</b></div>
    </section>

    <section class="card">
        <div class="toolbar">
          <div class="tabs" id="tabs"><button type="button" aria-pressed="true" data-t="all">전체</button><button type="button" aria-pressed="false" data-t="groom">신랑측</button><button type="button" aria-pressed="false" data-t="bride">신부측</button></div>
          <input class="search" id="q" placeholder="이름으로 찾기" aria-label="이름으로 찾기">
          <button type="button" class="btn2 rose" id="addBank">계좌이체 추가</button>
        </div>
        <div class="tbl resulttbl"><table><thead><tr><th>순번</th><th>구분</th><th>성함</th><th class="r">축의금</th><th>받은 방법</th><th class="r">식권</th><th>메모·기록</th></tr></thead><tbody id="tb"></tbody></table></div>
    </section>

    <section class="card">
      <div class="ch"><div><h3>정산 기록</h3><p>축의대가 제출한 내용입니다. 잘못된 점이 있으면 잠금을 풀어 축의대가 다시 고칠 수 있습니다.</p></div></div>
      <div id="settle" class="grid2"></div>
    </section>
    <div class="grid2" style="grid-template-columns:1fr">
        <section class="card">
          <div class="ch" style="margin-bottom:0"><div><h3>내려받기</h3><p>엑셀과 웹페이지 두 가지로 받을 수 있습니다. 2000. 7. 16.이 지나면 명부가 완전히 지워지니 그 전에 받아 두세요.</p></div><div style="display:flex;gap:8px;flex:none"><button type="button" class="btn2" data-dl>엑셀 (.xlsx)</button><button type="button" class="btn2" data-dl>웹페이지 (.html)</button></div></div>
        </section>
    </div>
''', script='''
  var R = seedRows('groom').concat(seedRows('bride'));
  R.push({ side: 'groom', no: '이체', name: '김태호', anon: false, amt: 100000, tk: 0, x: false, memo: '해외 거주', method: '계좌이체', hist: [] });
  R.push({ side: 'bride', no: '이체', name: '배수진', anon: false, amt: 50000, tk: 0, x: false, memo: '', method: '계좌이체', hist: [] });
  var tab = 'all';
  var live = function (s) { return R.filter(function (r) { return !r.x && (!s || r.side === s); }); };
  var sum = function (s) { return live(s).reduce(function (a, r) { return a + r.amt; }, 0); };
  function draw() {
    $('#sAll').textContent = kor(sum()); $('#sG').textContent = kor(sum('groom')); $('#sB').textContent = kor(sum('bride'));
    var bank = live().filter(function (r) { return r.method === '계좌이체'; }).length;
    $('#sCount').innerHTML = live().length + '<span>건</span>'; $('#sCountMeta').textContent = '· 계좌이체 ' + bank + ' · 취소 ' + R.filter(function (r) { return r.x; }).length;
    var q = $('#q').value.trim();
    var rs = R.filter(function (r) { return (tab === 'all' || r.side === tab) && (!q || (r.anon ? '무기명' : r.name).indexOf(q) > -1); });
    $('#tb').innerHTML = rs.length ? rs.map(function (r) {
      var note = [r.memo, r.hist && r.hist.length ? r.hist[r.hist.length - 1] : ''].filter(Boolean).map(esc).join(' · ');
      return '<tr class="' + (r.x ? 'x' : '') + '"><td class="num">' + r.no + '</td><td><span class="sd ' + (r.side === 'groom' ? 'g' : 'b') + '" style="font-size:12px;font-weight:800;padding:2px 8px;border-radius:7px">' + (r.side === 'groom' ? '신랑측' : '신부측') + '</span></td><td>' + (r.anon ? '무기명' : esc(r.name)) + (r.x ? ' <span class="tag x">취소</span>' : '') + '</td><td class="r num">' + kor(r.amt) + '</td><td><span class="mth' + (r.method === '계좌이체' ? ' bank' : '') + '">' + r.method + '</span></td><td class="r num">' + r.tk + '장</td><td style="color:var(--sub);font-size:13px">' + note + '</td></tr>';
    }).join('') : '<tr><td colspan="7" class="emptyl">찾는 이름이 없습니다</td></tr>';
  }
  $('#tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; tab = b.dataset.t; this.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); draw(); });
  $('#q').addEventListener('input', draw);

  var SET = {
    groom: { counted: 850000, book: 850000, have: 230, used: 19, rec: 19, reason: '', at: '14:20', open: false },
    bride: { counted: 875000, book: 880000, have: 200, used: 14, rec: 14, reason: '5천 원권 한 장 확인 못 함', at: '14:26', open: false }
  };
  function drawSettle() {
    $('#settle').innerHTML = ['groom', 'bride'].map(function (s) {
      var x = SET[s], ok = x.counted === x.book && x.used === x.rec;
      return '<div class="sidecard">' +
        '<h4>' + (s === 'groom' ? '신랑측 · 이용범' : '신부측 · 김홍매') + (x.open ? '<span class="pill live" style="animation:none">잠금 풀림</span>' : '<span class="pill ' + (ok ? 'ok' : 'wait') + '">' + (ok ? '일치' : '차이 있음') + '</span>') + '</h4>' +
        '<p class="muted" style="margin:4px 0 8px;font-size:13px">' + x.at + ' 제출' + (x.open ? ' · 지금 축의대에서 고칠 수 있습니다' : '') + '</p>' +
        '<div class="row"><span>센 현금</span><b>' + won(x.counted) + '</b></div>' +
        '<div class="row"><span>명부 합계</span><b' + (x.counted !== x.book ? ' style="color:var(--err)"' : '') + '>' + won(x.book) + '</b></div>' +
        '<div class="row"><span>나간 식권 (실제 / 기록)</span><b' + (x.used !== x.rec ? ' style="color:var(--err)"' : '') + '>' + x.used + '장 / ' + x.rec + '장</b></div>' +
        (x.reason ? '<div class="row"><span>차이 사유</span><b style="font-weight:500;text-align:right">' + esc(x.reason) + '</b></div>' : '') +
        '<div class="row" style="padding-bottom:0"><span class="muted" style="font-size:12.5px">' + (x.open ? '다시 잠그면 제출 상태로 돌아갑니다' : '잠금을 풀면 기록이 남습니다') + '</span><button type="button" class="btn2' + (x.open ? ' rose' : '') + '" data-unlock="' + s + '">' + (x.open ? '다시 잠그기' : '잠금 풀기') + '</button></div></div>';
    }).join('');
  }
  document.addEventListener('click', function (e) {
    var u = e.target.closest('[data-unlock]');
    if (u) { var x = SET[u.dataset.unlock]; x.open = !x.open; drawSettle(); toast(x.open ? '잠금을 풀었습니다. 기록은 남습니다' : '다시 잠갔습니다'); }
    if (e.target.closest('[data-dl]')) toast('시안에서는 내려받기가 동작하지 않습니다');
  });
  $('#addBank').addEventListener('click', function () {
    openModal('계좌이체 추가', '축의대 밖에서 받은 축의금을 신랑신부가 적습니다.',
      '<div class="field"><div class="lab">구분</div><div class="seg" id="bSide" style="grid-template-columns:1fr 1fr;margin:0"><button type="button" aria-pressed="true" data-s="groom">신랑측</button><button type="button" aria-pressed="false" data-s="bride">신부측</button></div></div>' +
      '<div class="field"><label class="lab" for="bName">성함</label><input class="inp" id="bName" placeholder="보낸 분 이름"></div>' +
      '<div class="field"><div class="lab"><label for="bAmt">금액</label><span class="readout empty" id="bRead">5 → 5만 · 3.5 → 3만 5천</span></div><div class="amtbox"><input class="inp" id="bAmt" inputmode="decimal" placeholder="0" style="padding-right:64px"><span class="unit">만 원</span></div></div>' +
      '<div class="field"><label class="lab" for="bMemo">메모</label><input class="inp" id="bMemo" placeholder="예: 회사 동기 단체"></div>' +
      '<div class="mbtns"><button type="button" class="save" id="bSave">추가</button></div>');
    var side = 'groom';
    $('#bSide').onclick = function (e) { var b = e.target.closest('button'); if (!b) return; side = b.dataset.s; this.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); };
    $('#bAmt').oninput = function () { var v = parseAmt(this.value); $('#bRead').textContent = v ? kor(v) + ' (' + won(v) + ')' : '5 → 5만 · 3.5 → 3만 5천'; $('#bRead').classList.toggle('empty', !v); };
    $('#bName').focus();
    $('#bSave').onclick = function () {
      var nm = $('#bName').value.trim(), amt = parseAmt($('#bAmt').value);
      if (!nm) { $('#bName').focus(); return; }
      if (!amt) { $('#bAmt').focus(); return; }
      R.push({ side: side, no: '이체', name: nm, anon: false, amt: amt, tk: 0, x: false, memo: $('#bMemo').value.trim(), method: '계좌이체', hist: [] });
      closeModal(); draw(); toast(nm + ' · ' + kor(amt) + ' 계좌이체를 추가했습니다');
    };
  });
  draw(); drawSettle();
''')
