# -*- coding: utf-8 -*-
"""1단계(2026-09-16): 여섯 장 HTML 에 data-t/data-paras/data-img/data-list 표시를 붙이고 스크립트 순서를 바꿉니다.
   HTML 의 글은 그대로 두고(JS 꺼졌을 때 대비) 표시만 붙입니다 — 실제 글은 data/site.js + 서버 값으로 다시 채워집니다."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
HEAD_ADD = '<link rel="stylesheet" href="css/site.css">\n<script>document.documentElement.className += " pending";</script><!-- 내용이 정해질 때까지 잠깐 숨김(js/content.js 가 풂) -->'
SCRIPTS_OLD = '<script src="data/menu.js"></script>\n<script src="js/site.js"></script>\n<script src="js/config.js"></script>\n<script src="js/reserve.js"></script>'
SCRIPTS_NEW = '<script src="data/site.js"></script>\n<script src="js/config.js"></script>\n<script src="js/content.js"></script>\n<script src="js/site.js"></script>\n<script src="js/reserve.js"></script>'

def fix(name, pairs):
    p = os.path.join(ROOT, name)
    s = open(p, encoding="utf-8").read()
    for a, b in [('<link rel="stylesheet" href="css/site.css">', HEAD_ADD), (SCRIPTS_OLD, SCRIPTS_NEW)] + pairs:
        assert s.count(a) == 1, (name, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s); print("ok", name)

fix("index.html", [
 ('<h1>한옥에서 즐기는 중식</h1>\n    <p>경기 성남시 분당구 새마을로51번길 2</p>', '<h1 data-t="home.heroTitle">한옥에서 즐기는 중식</h1>\n    <p data-t="home.heroSub">경기 성남시 분당구 새마을로51번길 2</p>'),
 ('<figure><img src="img/bg7.jpg" alt="1층 테이블"></figure>\n    <div class="t">\n      <h2>한옥을 지어<br>문을 열었습니다</h2>\n      <p>2020년 분당',
  '<figure><img src="img/bg7.jpg" alt="1층 테이블" data-img="home.intro.img" data-alt="home.intro.imgAlt"></figure>\n    <div class="t">\n      <h2 data-t="home.intro.title">한옥을 지어<br>문을 열었습니다</h2>\n      <div data-paras="home.intro.paras"><p>2020년 분당'),
 ('룸 여덟 곳과 테이블 두 곳이 있습니다.</p>\n      <a class="more" href="about.html">이야기 전체</a>', '룸 여덟 곳과 테이블 두 곳이 있습니다.</p></div>\n      <a class="more" href="about.html" data-t="home.intro.more">이야기 전체</a>'),
 ('<div class="hd"><div><h2>차림</h2><p>우리 가족이 먹는다는 생각으로, 신선한 재료를 매일 직접 준비합니다</p></div><a class="more" href="menu.html">차림 전체</a></div>',
  '<div class="hd"><div><h2 data-t="home.menuSec.title">차림</h2><p data-t="home.menuSec.lead">우리 가족이 먹는다는 생각으로, 신선한 재료를 매일 직접 준비합니다</p></div><a class="more" href="menu.html" data-t="home.menuSec.more">차림 전체</a></div>'),
 ('<figure><img src="img/bg1.jpg" alt="관우 룸의 원탁"></figure>', '<figure><img src="img/bg1.jpg" alt="관우 룸의 원탁" data-img="home.menuSec.img" data-alt="home.menuSec.imgAlt"></figure>'),
 ('<div class="hd"><div><h2>공간</h2><p>나무와 창호가 만드는 조용한 자리. 문을 닫으면 방 하나가 온전히 손님의 것이 됩니다</p></div><a class="more" href="space.html">공간 전체</a></div>\n    <div class="tiles">',
  '<div class="hd"><div><h2 data-t="home.spaceSec.title">공간</h2><p data-t="home.spaceSec.lead">나무와 창호가 만드는 조용한 자리. 문을 닫으면 방 하나가 온전히 손님의 것이 됩니다</p></div><a class="more" href="space.html" data-t="home.spaceSec.more">공간 전체</a></div>\n    <div class="tiles" id="home-tiles">'),
 ('<div class="v">경기 성남시 분당구<br>새마을로51번길 2</div>\n        <p>주차비 1,000원 · 발렛 무료</p>\n        <div class="lk"><a class="more" href="visit.html">오시는 길 전체</a></div>',
  '<div class="v" data-t="info.addr2">경기 성남시 분당구<br>새마을로51번길 2</div>\n        <p data-t="info.parking">주차비 1,000원 · 발렛 무료</p>\n        <div class="lk"><a class="more" href="visit.html" data-t="home.infoSec.visitMore">오시는 길 전체</a></div>'),
 ('<div class="v"><a href="tel:031-724-1004">031-724-1004</a></div>\n        <p>예약과 문의는 영업시간 중 언제든 전화 주세요</p>',
  '<div class="v"><a href="tel:031-724-1004" data-tel>031-724-1004</a></div>\n        <p data-t="home.infoSec.telNote">예약과 문의는 영업시간 중 언제든 전화 주세요</p>'),
 ('<img src="img/bg6.jpg" alt="">\n  <div class="in">\n    <h2>예약</h2>\n    <p>머무실 자리를 미리 준비해 두겠습니다.<br>접수하신 내용은 확인 후 문자로 확정해 드립니다.</p>\n    <button type="button" class="btn" data-reserve>예약하기</button>',
  '<img src="img/bg6.jpg" alt="" data-img="home.band.img">\n  <div class="in">\n    <h2 data-t="home.band.title">예약</h2>\n    <p>머무실 자리를 미리 준비해 두겠습니다.<br>접수하신 내용은 확인 후 문자로 확정해 드립니다.</p>\n    <button type="button" class="btn" data-reserve data-t="home.band.button">예약하기</button>'),
])

fix("about.html", [
 ('<section class="page-head"><img class="pic" src="img/bg7.jpg" alt=""><div class="wrap"><h1>이야기</h1><p>한옥을 지어 중식당을 열기까지.</p></div></section>',
  '<section class="page-head"><img class="pic" src="img/bg7.jpg" alt="" data-img="about.head.img"><div class="wrap"><h1 data-t="about.head.title">이야기</h1><p data-t="about.head.sub">한옥을 지어 중식당을 열기까지.</p></div></section>'),
 ('<div class="eh"><h2>인사말</h2><p>대표 김지아</p></div>\n    <div class="prose">\n      <p>안녕하세요',
  '<div class="eh"><h2 data-t="about.greeting.title">인사말</h2><p data-t="about.greeting.by">대표 김지아</p></div>\n    <div class="prose">\n      <div data-paras="about.greeting.paras"><p>안녕하세요'),
 ('언제든 말씀해 주세요. 감사합니다.</p>\n      <p class="sign">김지아 드림</p>', '언제든 말씀해 주세요. 감사합니다.</p></div>\n      <p class="sign" data-t="about.greeting.sign">김지아 드림</p>'),
 ('<figure><img src="img/chef.png" alt="총주방장 박수일"></figure>\n    <div class="t">\n      <p class="who">총주방장 · 중식 경력 35년</p>\n      <h2>박수일</h2>\n      <p class="quote">"정성을 담습니다.<br>최고만을 대접하기 위해."</p>\n      <p>서른다섯',
  '<figure><img src="img/chef.png" alt="총주방장 박수일" data-img="about.chef.img"></figure>\n    <div class="t">\n      <p class="who" data-t="about.chef.who">총주방장 · 중식 경력 35년</p>\n      <h2 data-t="about.chef.name">박수일</h2>\n      <p class="quote" data-t="about.chef.quote">"정성을 담습니다.<br>최고만을 대접하기 위해."</p>\n      <p data-t="about.chef.para">서른다섯'),
 ('<div class="eh"><h2>한옥을<br>지었습니다</h2><p>2020년부터</p></div>\n    <div class="prose">\n      <p>나무로',
  '<div class="eh"><h2 data-t="about.story.title">한옥을<br>지었습니다</h2><p data-t="about.story.sub">2020년부터</p></div>\n    <div class="prose">\n      <div data-paras="about.story.paras"><p>나무로'),
 ('한 가족이 함께 운영합니다.</p>\n      <div class="pics">', '한 가족이 함께 운영합니다.</p></div>\n      <div class="pics" id="story-pics">'),
])

fix("space.html", [
 ('<section class="page-head"><img class="pic" src="img/bg4.jpg" alt=""><div class="wrap"><h1>공간</h1><p>창호를 지난',
  '<section class="page-head"><img class="pic" src="img/bg4.jpg" alt="" data-img="space.head.img"><div class="wrap"><h1 data-t="space.head.title">공간</h1><p data-t="space.head.sub">창호를 지난'),
 ('<div class="hd"><h2>룸</h2></div>', '<div class="hd"><h2 data-t="space.roomsTitle">룸</h2></div>'),
 ('<div class="hd"><h2>테이블</h2></div>', '<div class="hd"><h2 data-t="space.hallsTitle">테이블</h2></div>'),
])

fix("menu.html", [
 ('<img class="pic" src="img/bg1.jpg" alt="">\n  <div class="wrap">\n    <h1>차림</h1>\n    <p>고객님의',
  '<img class="pic" src="img/bg1.jpg" alt="" data-img="menuPage.head.img">\n  <div class="wrap">\n    <h1 data-t="menuPage.head.title">차림</h1>\n    <p data-t="menuPage.head.sub">고객님의'),
 ('<a class="btn pdf" target="_blank" rel="noopener">메뉴판 PDF</a>', '<a class="btn pdf" target="_blank" rel="noopener" data-t="menuPage.pdfLabel">메뉴판 PDF</a>'),
 ('<div class="t"><span>총주방장 박수일 · 중식 경력 35년</span><b>"정성을 담습니다. 최고만을 대접하기 위해."</b></div>\n    <img src="img/chef.png" alt="">',
  '<div class="t"><span data-t="menuPage.chefBand.who">총주방장 박수일 · 중식 경력 35년</span><b data-t="menuPage.chefBand.quote">"정성을 담습니다. 최고만을 대접하기 위해."</b></div>\n    <img src="img/chef.png" alt="" data-img="menuPage.chefBand.img">'),
 ('<div class="eh"><h2>저녁 코스</h2><p>종일 주문하실 수 있습니다.</p></div>', '<div class="eh"><h2 data-t="menuPage.courses.title">저녁 코스</h2><p data-t="menuPage.courses.sub">종일 주문하실 수 있습니다.</p></div>'),
 ('<div class="eh"><h2>점심 세트</h2><p>오전 11:00 – 오후 3:30</p></div>', '<div class="eh"><h2 data-t="menuPage.lunch.title">점심 세트</h2><p data-t="menuPage.lunch.sub">오전 11:00 – 오후 3:30</p></div>'),
 ('<div class="eh"><h2>요리</h2></div>', '<div class="eh"><h2 data-t="menuPage.dishes.title">요리</h2></div>'),
 ('<div class="eh"><h2>만두</h2></div>', '<div class="eh"><h2 data-t="menuPage.dumplings.title">만두</h2></div>'),
 ('<div class="eh"><h2>주류</h2></div>', '<div class="eh"><h2 data-t="menuPage.drinks.title">주류</h2></div>'),
])

fix("visit.html", [
 ('<section class="page-head"><img class="pic" src="img/hanok.jpg" alt=""><div class="wrap"><h1>오시는 길</h1><p>새마을로 골목 초입, 기와지붕이 보이면 다 오신 겁니다.</p></div></section>',
  '<section class="page-head"><img class="pic" src="img/hanok.jpg" alt="" data-img="visit.head.img"><div class="wrap"><h1 data-t="visit.head.title">오시는 길</h1><p data-t="visit.head.sub">새마을로 골목 초입, 기와지붕이 보이면 다 오신 겁니다.</p></div></section>'),
 ('<address><b>경기 성남시 분당구<br>새마을로51번길 2</b>전화 <a href="tel:031-724-1004" class="num">031-724-1004</a></address>',
  '<address><b data-t="info.addr2">경기 성남시 분당구<br>새마을로51번길 2</b>전화 <a href="tel:031-724-1004" class="num" data-tel>031-724-1004</a></address>'),
 ('<h3>영업시간</h3>\n      <div class="hours" id="hours"></div>', '<h3 data-t="visit.hoursTitle">영업시간</h3>\n      <div class="hours" id="hours"></div>'),
 ('<p class="cap" style="margin-top:10px">약도는 실제 축적과 다소 다를 수 있습니다.</p>', '<p class="cap" style="margin-top:10px" data-t="visit.mapCaption">약도는 실제 축적과 다소 다를 수 있습니다.</p>'),
 ('<h3>주차</h3>\n      <div class="prose-s">\n        <p>주차장은', '<h3 data-t="visit.parkingTitle">주차</h3>\n      <div class="prose-s" data-paras="visit.parking">\n        <p>주차장은'),
 ('<h3>대중교통</h3>\n      <ul class="plain">', '<h3 data-t="visit.transitTitle">대중교통</h3>\n      <ul class="plain" data-list="visit.transit">'),
])

fix("reserve.html", [
 ('<section class="page-head"><img class="pic" src="img/bg6.jpg" alt=""><div class="wrap"><h1>예약</h1><p>온라인으로 접수하시면 가게에서 확인한 뒤 문자로 확정을 알려드립니다.</p></div></section>',
  '<section class="page-head"><img class="pic" src="img/bg6.jpg" alt="" data-img="reserve.head.img"><div class="wrap"><h1 data-t="reserve.head.title">예약</h1><p data-t="reserve.head.sub">온라인으로 접수하시면 가게에서 확인한 뒤 문자로 확정을 알려드립니다.</p></div></section>'),
 ('<ul class="notes">', '<ul class="notes" id="rv-notes">'),
 ('<h3>예약하기</h3>\n      <p>차례대로 고르시면 됩니다. 시간을 고른 뒤 5분 안에 마쳐 주세요.</p>\n      <ol>',
  '<h3 data-t="reserve.go.title">예약하기</h3>\n      <p data-t="reserve.go.lead">차례대로 고르시면 됩니다. 시간을 고른 뒤 5분 안에 마쳐 주세요.</p>\n      <ol id="rv-steps">'),
 ('<button type="button" class="btn fill" data-reserve>예약하기</button>\n      <p class="cap">접수 후 영업시간 중에는 보통 한 시간 안에 문자를 드립니다.</p>',
  '<button type="button" class="btn fill" data-reserve data-t="reserve.go.button">예약하기</button>\n      <p class="cap" data-t="reserve.go.cap">접수 후 영업시간 중에는 보통 한 시간 안에 문자를 드립니다.</p>'),
])
