# -*- coding: utf-8 -*-
"""재아 요청(2026-09-17) 사이트 쪽:
   문구(안집과 · 새마을로 골목 초입에 위치 · 축적과 다를 수 · 유선으로 예약) · 테이블 8명 규칙 삭제 · 룸 안내는 '미정' 눌렀을 때만 ·
   점심에도 저녁 코스 함께(저녁 코스 (종일) 이 먼저) · 알러지 칸 따로(requests.allergy) """
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def fix(name, pairs):
    p = os.path.join(ROOT, name); s = io.open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:60], s.count(a)); s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8").write(s); print("ok", name)

fix("data/site.js", [
 ('sub: "서현동과 율동공원을 잇는 새마을로 골목 초입, 기와지붕이 보이면 다 오신 겁니다."', 'sub: "서현동과 율동공원을 잇는 새마을로 골목 초입에 위치하고 있습니다."'),
 ('mapCaption: "약도는 실제 축적과 다소 다를 수 있습니다."', 'mapCaption: "약도는 실제 축적과 다를 수 있습니다."'),
 ('"주차장은 맞은편 음식점 \'안집\'의 주차장을 함께 사용하고 있습니다."', '"주차장은 맞은편 음식점 \'안집\'과 함께 사용하고 있습니다."'),
 ('    tableMax: 8,          /* 테이블은 몇 명까지 */\n', ''),
 ('    courses: { title: "저녁 코스", sub: "종일 주문하실 수 있습니다." },', '    courses: { title: "저녁 코스 (종일)", sub: "종일 주문하실 수 있습니다." },'),
])
fix("visit.html", [
 ('서현동과 율동공원을 잇는 새마을로 골목 초입, 기와지붕이 보이면 다 오신 겁니다.', '서현동과 율동공원을 잇는 새마을로 골목 초입에 위치하고 있습니다.'),
 ('약도는 실제 축적과 다소 다를 수 있습니다.', '약도는 실제 축적과 다를 수 있습니다.'),
 ("<p>주차장은 맞은편 음식점 '안집'의 주차장을 함께 사용하고 있습니다.</p>", "<p>주차장은 맞은편 음식점 '안집'과 함께 사용하고 있습니다.</p>"),
])
fix("menu.html", [
 ('<h2 data-t="menuPage.courses.title">저녁 코스</h2>', '<h2 data-t="menuPage.courses.title">저녁 코스 (종일)</h2>'),
])
fix("js/reserve.js", [
 # 테이블 8명 규칙 삭제
 ('''  const R = () => Object.assign({enabled:true, maxDays:30, minAdults:2, maxPeople:12, roomMinAdults:5, tableMax:8, limitMin:5,''',
  '''  const R = () => Object.assign({enabled:true, maxDays:30, minAdults:2, maxPeople:12, roomMinAdults:5, limitMin:5,'''),
 ('''    if(S.seat === "table" && total() > R().tableMax) return `테이블은 ${R().tableMax}명까지 온라인으로 받고 있습니다.`;
''', ''),
 # 13명 문구
 ('''        ? `${total()}명은 온라인으로 접수하기 어렵습니다.<br>전화로 문의해 주세요. <a href="tel:${INFO.tel}">${esc(INFO.tel)}</a>`''',
  '''        ? `유선으로 예약 도와드리겠습니다. <a href="tel:${INFO.tel}">${esc(INFO.tel)}</a>`'''),
 # 메뉴: 저녁 코스(종일)를 먼저, 점심 시각이면 그 아래 점심 세트도
 ('''  function menuGroups(){
    const out = [];
    if(mins(S.time) < LUNCH_END){
      const want = isWeekend(S.date) ? "주말" : "평일";
      const set = MENU.lunch.filter(g => g.title.indexOf(want) === 0)[0] || MENU.lunch[0];
      out.push({ title: set.title, items: set.items.map(x => ({key:"set:"+x.name, name:x.name, cn:""})) });
    }
    out.push({ title: MENU.courses.title, items: MENU.courses.items.map(c => ({key:"course:"+c.name, name:c.name, cn:c.cn})) });
    return out;
  }''',
  '''  /* 저녁 코스는 종일 되니 늘 먼저(비싼 것부터 — 재아), 점심 시각이면 그 아래 점심 세트 */
  function menuGroups(){
    const out = [{ title: "저녁 코스 (종일)", items: MENU.courses.items.map(c => ({key:"course:"+c.name, name:c.name, cn:c.cn})) }];
    if(mins(S.time) < LUNCH_END){
      const want = isWeekend(S.date) ? "주말" : "평일";
      const set = MENU.lunch.filter(g => g.title.indexOf(want) === 0)[0] || MENU.lunch[0];
      out.push({ title: set.title, items: set.items.map(x => ({key:"set:"+x.name, name:x.name, cn:""})) });
    }
    return out;
  }'''),
 # 룸 안내는 '미정' 을 골랐을 때만
 ('''        ${room ? `<p class="rv-quiet">룸은 코스, 또는 그에 상응하는 금액의 단품 주문이 가능합니다.</p>` : ""}
''', ''),
 ('''      if(room) ask("룸 이용 안내", "룸에서는 <b>코스</b>, 또는 그에 상응하는 금액의 단품 주문만 가능합니다.", "확인", go);
      else go();''',
  '''      if(room && S.course === "later") ask("룸 이용 안내", "룸에서는 <b>코스</b>, 또는 그에 상응하는 금액의 단품 주문만 가능합니다.", "확인", go);
      else go();'''),
 # 알러지 칸 따로
 ('''         sent:false, verified:false, req:"", agree:{rule:false, priv:false, age:false}};''',
  '''         sent:false, verified:false, req:"", allergy:"", agree:{rule:false, priv:false, age:false}};'''),
 ('''        <div class="rv-fld"><label for="rv-req">요청사항 <em>선택</em></label>
          <textarea id="rv-req" rows="3" maxlength="300" placeholder="알레르기가 있으시거나 어린이 의자·식기가 필요하시면 적어 주세요. 예약하시는 분과 방문하시는 분이 다르면 함께 적어 주세요.">${esc(S.req)}</textarea></div>''',
  '''        <div class="rv-fld"><label for="rv-allergy">알레르기 <em>선택</em></label>
          <input id="rv-allergy" value="${esc(S.allergy)}" maxlength="100" placeholder="예: 갑각류 · 땅콩 · 밀가루 (없으면 비워 두세요)"></div>
        <div class="rv-fld"><label for="rv-req">요청사항 <em>선택</em></label>
          <textarea id="rv-req" rows="3" maxlength="300" placeholder="어린이 의자·식기가 필요하시거나, 예약하시는 분과 방문하시는 분이 다르면 적어 주세요.">${esc(S.req)}</textarea></div>'''),
 ('''    req.addEventListener("input", () => { S.req = req.value; });''',
  '''    req.addEventListener("input", () => { S.req = req.value; });
    $("#rv-allergy", b).addEventListener("input", e => { S.allergy = e.target.value; });'''),
 ('''    if(S.req.trim()) rows.push(["요청사항", S.req.trim()]);''',
  '''    if(S.allergy.trim()) rows.push(["알레르기", S.allergy.trim()]);
    if(S.req.trim()) rows.push(["요청사항", S.req.trim()]);'''),
 ('''                                      name:S.name.trim(), phone:S.phone, request:S.req.trim()});''',
  '''                                      name:S.name.trim(), phone:S.phone, request:S.req.trim(), allergy:S.allergy.trim()});'''),
 ('''        name:p.name, phone:String(p.phone).replace(/\\D/g,""), request:p.request||"", status:"대기" };''',
  '''        name:p.name, phone:String(p.phone).replace(/\\D/g,""), request:p.request||"", allergy:p.allergy||"", status:"대기" };'''),
])
