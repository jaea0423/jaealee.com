# -*- coding: utf-8 -*-
"""전수 검토 2차: 차림 편집에서 '이름 | 설명' 은 주류만(요리·만두 tag 는 사이트에 안 나오므로 헷갈리지 않게) """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

s = load("js/14b-site-admin.js")
s = rep(s, '''  var itemLines = function(items){ return items.map(function(x){ return x.name + (x.tag ? " | " + x.tag : ""); }); };''',
           '''  var itemLines = function(items, withTag){ return items.map(function(x){ return x.name + (withTag && x.tag ? " | " + x.tag : ""); }); };''', 1)
s = rep(s, '''가격은 홈페이지에 안 나옵니다(메뉴판 PDF 에서만). 이름 뒤에 <b>|</b> 를 두고 적으면 작은 설명이 됩니다 — 예: <code>중새우요리 | 칠리 · 크림 · 깐풍 중 택 1</code>''',
           '''가격은 홈페이지에 안 나옵니다(메뉴판 PDF 에서만). 요리·만두는 이름만 보이고, 주류는 이름 뒤에 <b>|</b> 를 두고 적으면 작은 설명이 붙습니다 — 예: <code>소주 | 참이슬 · 처음처럼</code>''', 1)
# 요리(dishes)·만두: 이름만. 주류: 설명 포함
s = rep(s, '''saMenuLines(gp + "items", "메뉴", itemLines(g.items || [])) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrMove(''',
           '''saMenuLines(gp + "items", "메뉴", itemLines(g.items || []), false) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrMove(''', 1)
s = rep(s, '''saBox("만두", saMenuLines("menu.dumplings.items", "메뉴", itemLines(DM))) +''',
           '''saBox("만두", saMenuLines("menu.dumplings.items", "메뉴", itemLines(DM), false)) +''', 1)
s = rep(s, '''saMenuLines(gp + "items", "메뉴", itemLines(g.items || [])) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrDel(''',
           '''saMenuLines(gp + "items", "메뉴", itemLines(g.items || [], true), true) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrDel(''', 1)
s = rep(s, '''function saMenuLines(path, label, lines){
  return '<label class="f sa-f"><div class="lb">' + esc(label) + ' <span class="lbl-note">한 줄에 하나 · 이름 | 설명</span></div><textarea class="in-sm" rows="' + Math.max(3, lines.length + 1) + '" oninput="saSetMenuLines(\\'' + path + '\\', this.value)">' + esc(lines.join("\\n")) + '</textarea></label>';
}''',
'''function saMenuLines(path, label, lines, withTag){
  return '<label class="f sa-f"><div class="lb">' + esc(label) + ' <span class="lbl-note">한 줄에 하나' + (withTag ? ' · 이름 | 설명' : '') + '</span></div><textarea class="in-sm" rows="' + Math.max(3, lines.length + 1) + '" oninput="saSetMenuLines(\\'' + path + '\\', this.value, ' + (withTag ? 'true' : 'false') + ')">' + esc(lines.join("\\n")) + '</textarea></label>';
}''', 1)
s = rep(s, '''function saSetMenuLines(path, text){
  var old = saGet(path) || [];
  var items = String(text).split("\\n").map(function(l){ return l.trim(); }).filter(function(l){ return l.length; }).map(function(l){
    var sp = l.split("|"), name = sp[0].trim(), tag = sp.slice(1).join("|").trim();
    var prev = old.filter(function(x){ return x.name === name; })[0];
    var it = prev ? deepClone(prev) : {name:name};
    it.name = name; if(tag) it.tag = tag; else delete it.tag;
    return it;
  });
  saSet(path, items);
}''',
'''/* 줄 → 항목. withTag(주류)면 "이름 | 설명" 을 tag 로. 아니면(요리·만두) 이름만 받고, 있던 tag·price 는 이름이 같으면 그대로 둠(화면엔 안 나와도 자료로 남김) */
function saSetMenuLines(path, text, withTag){
  var old = saGet(path) || [];
  var items = String(text).split("\\n").map(function(l){ return l.trim(); }).filter(function(l){ return l.length; }).map(function(l){
    var sp = withTag ? l.split("|") : [l], name = sp[0].trim(), tag = withTag ? sp.slice(1).join("|").trim() : null;
    var prev = old.filter(function(x){ return x.name === name; })[0];
    var it = prev ? deepClone(prev) : {name:name};
    it.name = name; if(withTag){ if(tag) it.tag = tag; else delete it.tag; }
    return it;
  });
  saSet(path, items);
}''', 1)
save("js/14b-site-admin.js", s)
print("ok")
