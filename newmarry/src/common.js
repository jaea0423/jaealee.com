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
  /* 축의대 용품 (data-shop="그림 폴더 경로" 버튼으로 연다). 시안이라 주문은 되지 않음 */
  /* [번호, 이름, 설명, 가격(1묶음), 표시, 묶음 단위(n매), 담기 기본 수량] */
  var SHOP = [
    [1, '축의대 안내판', '"찾아주셔서 감사합니다" 탁상 안내판. 봉투에 성함을 적어 달라고 미리 알려 혼동이 줄어듭니다.', 12900, '추천'],
    [2, '고급 축의금 봉투 100매', '두꺼운 미색 종이에 금박 매듭. 100매 단위로 팔며, 하객 수를 생각하면 200매를 권합니다.', 24900, '200매 추천', 100, 2],
    [3, '현금 띠지 30매', '매수 적는 칸이 있는 띠지. 정산 때 권종별로 묶어 두면 세고 넘기기 쉽습니다.', 4900],
    [4, '현금 가방', '지퍼가 달린 보관·전달 가방. 정산이 끝나면 인계받을 분께 그대로 건넵니다.', 19900],
    [5, '고급 싸인펜 3자루', '축의대용 1자루, 하객용 2자루. 봉투 뒷면 순번, 봉투·방명록에 성함 쓰기에 알맞은 붓펜.', 8900],
    [6, '추가 안내판', '식사·답례품·주차 등 원하는 문구로 만드는 탁상 안내판.', 9900],
    [7, '방명록', '안내판과 같은 꽃 무늬의 하드커버 방명록.', 24900]
  ];
  var SHIP = 3000, SHIP_FREE = 20000;  // 2만 원 이상 무료배송, 아니면 3천 원
  var cart = {};
  function drawShop() {
    $('#shopGrid').innerHTML = SHOP.map(function (p) {
      var q = cart[p[0]] || 0;
      return '<div class="prod"><div class="pimg" style="background-image:url(' + $('#shopGrid').dataset.base + p[0] + '.webp)">' + (p[4] ? '<span class="pbadge">' + p[4] + '</span>' : '') + '</div>' +
        '<b>' + p[1] + '</b><small>' + p[2] + '</small><div class="pfoot"><span class="pprice">' + won(p[3]) + '</span>' +
        (q ? '<span class="pq"><button type="button" data-q="' + p[0] + '" data-d="-1" aria-label="하나 빼기">−</button><em>' + (p[5] ? q * p[5] + '매' : q) + '</em><button type="button" data-q="' + p[0] + '" data-d="1" aria-label="하나 더">+</button></span>'
           : '<button type="button" class="btn2 rose" data-q="' + p[0] + '" data-d="' + (p[6] || 1) + '">담기</button>') + '</div></div>';
    }).join('');
    var n = 0, sum = 0;
    SHOP.forEach(function (p) { var q = cart[p[0]] || 0; if (q) n++; sum += q * p[3]; });
    var ship = sum >= SHIP_FREE ? 0 : SHIP;
    $('#shopSum').innerHTML = n ? '<span>' + n + '가지 · 용품 ' + won(sum) + ' · 배송비 ' + (ship ? won(ship) : '무료') + '</span><b>' + won(sum + ship) + '</b>'
      : '<span>2만 원 이상 무료배송 (그 밖에는 배송비 3,000원)</span>';
    $('#shopBuy').disabled = !n;
  }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-shop]');
    if (o) {
      openModal('축의대 용품', '축의대에 올려 두면 하객도 담당자도 덜 헷갈립니다. 필요한 것만 골라 담으세요.',
        '<div class="shop" id="shopGrid" data-base="' + o.dataset.shop + '"></div>' +
        '<div class="shopbar"><button type="button" class="linkbtn" id="shopAll">권하는 대로 전부 담기</button><div class="ssum" id="shopSum"></div><button type="button" class="save" id="shopBuy">주문하기</button></div>', true);
      $('#modal').classList.add('shopm');
      drawShop();
      $('#shopAll').onclick = function () { SHOP.forEach(function (p) { if (!cart[p[0]]) cart[p[0]] = p[6] || 1; }); drawShop(); };
      $('#shopBuy').onclick = function () { toast('시안에서는 주문이 되지 않습니다'); };
      return;
    }
    var b = e.target.closest('[data-q]');
    if (b && $('#shopGrid')) { var id = +b.dataset.q; cart[id] = Math.max(0, Math.min(20, (cart[id] || 0) + +b.dataset.d)); drawShop(); }
  });
