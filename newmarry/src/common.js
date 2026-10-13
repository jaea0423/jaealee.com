  var $ = function (s) { return document.querySelector(s); };
  var won = function (n) { return n.toLocaleString('ko-KR') + '원'; };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function hhmm(d) { d = d || new Date(); return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); }
  /* 50000 → "5만 원", 135000000 → "1억 3,500만 원" */
  function kor(n) {
    if (!n) return '0원';
    var eok = Math.floor(n / 100000000), man = Math.floor(n % 100000000 / 10000), rest = n % 10000, s = '';
    if (eok) s += eok.toLocaleString('ko-KR') + '억';
    if (man) s += ' ' + man.toLocaleString('ko-KR') + '만';
    if (rest) { var ch = Math.floor(rest / 1000); if (ch) s += ' ' + ch + '천'; }
    return s.trim() + ' 원';
  }
  /* 입력 칸은 만 원 단위, 소수점 첫째 자리 = 천 원 */
  function parseAmt(v) {
    v = String(v).replace(/[^0-9.]/g, '').replace(/^(\d*\.\d?).*$/, '$1');
    var x = parseFloat(v);
    return isFinite(x) && x > 0 ? Math.round(x * 10) * 1000 : 0;
  }
  var tt;
  function toast(m) { var t = $('#toast'); t.textContent = m; t.hidden = false; clearTimeout(tt); tt = setTimeout(function () { t.hidden = true; }, 2600); }
  function openModal(title, desc, body, wide) {
    $('#modal').className = 'modal' + (wide ? ' wide' : '');
    $('#modal').innerHTML = '<div class="mh"><div><h3>' + title + '</h3>' + (desc ? '<p>' + desc + '</p>' : '') + '</div><button type="button" class="x" data-close aria-label="닫기">×</button></div>' + body;
    $('#scrim').hidden = false;
  }
  function closeModal() { $('#scrim').hidden = true; }
  $('#scrim').addEventListener('click', function (e) { if (e.target === this || e.target.closest('[data-close]')) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !$('#scrim').hidden) closeModal(); });
  function alertPop(title, msg, focusEl) {
    openModal(title, '', '<p class="amsg">' + msg + '</p><div class="mbtns"><button type="button" class="save" id="aOk">확인</button></div>');
    $('#modal').classList.add('alert');
    $('#aOk').onclick = function () { closeModal(); if (focusEl) focusEl.focus(); };
    $('#aOk').focus();
  }
  /* 예시 명부 (진행 화면과 같은 데이터) */
  var SEED = {
    groom: [['박준혁',50000,1],['최성민',100000,2],['정태윤',50000,1],['한지훈',30000,0,1],['',50000,1],['오세진',100000,2],['서민호',50000,2,0,'12:52 식권 1장 → 2장'],['신동현',200000,2],['권재우',50000,1],['문하늘',100000,1],['송유진',50000,1],['백승호',50000,2]],
    bride: [['이서연',50000,1],['박지유',100000,2],['최수아',50000,1],['정하린',30000,1],['강예린',100000,0],['',50000,1],['조윤서',50000,1],['윤채원',200000,2],['장소율',50000,1],['임다은',100000,2],['한가을',50000,1],['오나래',50000,1]]
  };
  function seedRows(side) {
    return SEED[side].map(function (r, i) {
      var m = 12 * 60 + 10 + i * 3 + (side === 'bride' ? 1 : 0);
      return { side: side, no: i + 1, name: r[0], anon: !r[0], amt: r[1], tk: r[2], x: !!r[3], memo: '', method: '현금', hist: r[4] ? [r[4]] : (r[3] ? ['12:41 금액 잘못 받아 취소'] : []), t: ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + m % 60).slice(-2) };
    });
  }
