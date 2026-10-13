# -*- coding: utf-8 -*-
"""축의지기 시안 빌드.

  python src/build.py              → 저장소 루트에 index.html, register/ … result/, bg/ 를 만든다 (사이트용, 모든 페이지 독립 실행)
  python src/build.py --artifact   → 루트 index.html을 <title>부터 시작하는 조각으로 만든다 (claude.ai 아티팩트 게시용)

소스: src/desk.html(진행 화면 원본, 공통 테마 CSS 포함), src/pages*.py(나머지 화면), src/extra.css, src/common.js, src/bg/*.jpg
"""
import re, os, sys, shutil
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
sys.path.insert(0, D)
from pages import STATUS, RESULT
from pages_setup import REGISTER, SETUP, REQUEST
from pages2 import GUIDE, NAV as NAVPAGE
ARTIFACT = '--artifact' in sys.argv
day = open(os.path.join(D, 'desk.html'), encoding='utf-8').read()
DEFAULT_BG = 4  # 한복 그림이 기본
def img_url(cur): return '"%sbg/%d.jpg"' % ('' if cur is None else '../', DEFAULT_BG)
base_css = day[day.index('<style>') + 7: day.index('</style>')]
extra = open(os.path.join(D, 'extra.css'), encoding='utf-8').read()
common_js = open(os.path.join(D, 'common.js'), encoding='utf-8').read()
FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700;800&display=swap">'''
HEAD_STANDALONE = '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
NAV = [('register', '등록'), ('setup', '설정'), ('request', '요청'), ('guide', '준비'), ('desk', '진행'), ('status', '현황'), ('result', '결과')]

def nav(cur):
    pre = '' if cur is None else '../'
    items = '<a href="%sindex.html"%s>목록</a>' % (pre, ' aria-current="page"' if cur is None else '')
    for i, (f, n) in enumerate(NAV):
        items += '<a href="%s%s/index.html"%s>%d %s</a>' % (pre, f, ' aria-current="page"' if f == cur else '', i + 1, n)
    return '<nav class="proto" aria-label="시안 화면 이동"><em>시안</em>' + items + '</nav>'

def page(p, cur):
    standalone = cur is not None or not ARTIFACT
    out = '<title>%s</title>\n%s\n<style>%s\n%s</style>\n' % (p['title'], FONTS, base_css, extra)
    if standalone: out = HEAD_STANDALONE + out + '</head>\n<body>\n'
    # 각 화면의 위쪽 줄(.top)은 맨 위 막대(.gnav) 안으로 옮긴다
    m = re.search(r'^[ \t]*(<div class="top">.*</div>)[ \t]*\n', p['body'], re.M)
    top, body = (m.group(1), p['body'][:m.start()] + p['body'][m.end():]) if m else ('', p['body'])
    out += '''<div class="bg" aria-hidden="true"><div class="art"></div></div>
%s
<header class="gnav"><div class="gin"><a class="brand" href="%sindex.html">축의지기</a>%s</div></header>
<div class="app">
  <aside class="photo" aria-label="배경 사진"><div class="cap">%s
  </div></aside>
  <div class="work">%s
  </div>
</div>
<div class="scrim" id="scrim" hidden><div class="modal" id="modal" role="dialog" aria-modal="true"></div></div>
<div class="toast" id="toast" hidden></div>
<script>
(function () {
  'use strict';
%s
%s
})();
</script>
''' % (nav(cur), '' if cur is None else '../', top, p['cap'], body, common_js, p['script'])
    if standalone: out += '</body>\n</html>\n'
    return out.replace('__IMG__', img_url(cur))

def desk():
    j = day.replace('<title>축의지기 진행 시안</title>', '<title>축의지기 진행</title>')
    j = j.replace('</style>', extra + '</style>', 1).replace('<div class="bg" id="bg"', nav('desk') + '\n<div class="bg" id="bg"', 1)
    # PIN은 개발 마지막에 붙인다: 구분 선택부터 시작, 입력자 교체는 기록만
    j = j.replace('<div id="g1">', '<div id="g1" hidden>', 1).replace('<div id="g2" hidden>', '<div id="g2">', 1)
    j, n = re.subn(r"\$\('#swap'\)\.addEventListener\('click', function \(\) \{.*?\n  \}\);",
                   "$('#swap').addEventListener('click', function () { toast('입력자를 바꿨습니다. 교체 시각이 기록됩니다 (PIN 확인은 나중에 붙입니다)'); });", j, count=1, flags=re.S)
    assert n == 1
    # 요청서 이후 바뀐 것: 위쪽 막대의 칩으로 보여 주고, 구분을 고르면 한 번 자동으로 띄운다
    CHIP = '<button type="button" class="chgchip" id="chgChip"><i></i>요청서 이후 변동 2건</button>\n      '
    j = j.replace('<span class="sp"></span>', CHIP + '<span class="sp"></span>', 1)
    CHG_JS = """<script>
(function () {
  var seen = false;
  function openChg() {
    var m = document.getElementById('modal'), s = document.getElementById('scrim');
    m.className = 'modal';
    m.innerHTML = '<div class="mh"><div><h3>요청서 이후 바뀐 것</h3><p>신랑신부가 설정을 바꾸면 여기에 표시됩니다.</p></div><button type="button" class="x" data-close aria-label="닫기">×</button></div>' +
      '<div class="chglist">' +
      '<div><span>식권</span><b>200장 → 230장<small>10월 5일 · 혼주가 전달</small></b></div>' +
      '<div><span>인계받을 분</span><b>미정 → 신랑 아버지 이정수<small>10월 8일</small></b></div>' +
      '<div><span>축의대 자리</span><b style="color:var(--gold-d)">아직 미정<small>정해지면 다시 표시됩니다</small></b></div>' +
      '</div><div class="mbtns"><button type="button" class="save" id="chgOk">확인했습니다</button></div>';
    s.hidden = false;
    document.getElementById('chgOk').onclick = function () { s.hidden = true; seen = true; document.getElementById('chgChip').classList.add('seen'); var n = document.getElementById('name'); if (n) n.focus(); };
    document.getElementById('chgOk').focus();
  }
  document.getElementById('chgChip').addEventListener('click', openChg);
  /* 구분을 고른 직후 한 번 자동으로 띄운다 */
  document.querySelectorAll('.pick button').forEach(function (b) { b.addEventListener('click', function () { if (!seen) setTimeout(openChg, 350); }); });
  document.addEventListener('keydown', function (e) { if (!seen && (e.key === '1' || e.key === '2') && !document.getElementById('gate').hidden && !document.getElementById('g2').hidden) setTimeout(openChg, 350); }, true);
})();
</script>"""
    j = j.replace('</script>', '</script>\n' + CHG_JS, 1)
    j = j.replace('<a class="brand" href="#">', '<a class="brand" href="../index.html">', 1)
    j = HEAD_STANDALONE + j
    j = j.replace('</style>\n', '</style>\n</head>\n<body>\n', 1) + '\n</body>\n</html>\n'
    return j.replace('__IMG__', img_url('desk'))

OUT = ROOT
# 생성물은 덮어쓴다 (지우지 않으므로 저장소의 다른 파일은 건드리지 않는다)
shutil.copytree(os.path.join(D, 'bg'), os.path.join(OUT, 'bg'), dirs_exist_ok=True)
shutil.copytree(os.path.join(D, 'shop'), os.path.join(OUT, 'shop'), dirs_exist_ok=True)  # 축의대 용품 사진
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page(NAVPAGE, None))
for p, f in [(REGISTER, 'register'), (SETUP, 'setup'), (REQUEST, 'request'), (GUIDE, 'guide'), (STATUS, 'status'), (RESULT, 'result')]:
    os.makedirs(os.path.join(OUT, f), exist_ok=True); open(os.path.join(OUT, f, 'index.html'), 'w', encoding='utf-8').write(page(p, f))
os.makedirs(os.path.join(OUT, 'desk'), exist_ok=True); open(os.path.join(OUT, 'desk', 'index.html'), 'w', encoding='utf-8').write(desk())
# 스크립트 문법 검사 (node가 있으면)
import subprocess, tempfile
ok = True
for f in ['index'] + [n for n, _ in NAV]:
    t = open(os.path.join(OUT, f, 'index.html') if f != 'index' else os.path.join(OUT, 'index.html'), encoding='utf-8').read()
    js = '\n;\n'.join(re.findall(r'<script>(.*?)</script>', t, re.S))
    tmp = os.path.join(tempfile.gettempdir(), 'chukuijigi_' + f + '.js')
    open(tmp, 'w', encoding='utf-8').write(js)
    try:
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        if r.returncode: ok = False; print('JS 문법 오류:', f, r.stderr.strip()[:400])
    except FileNotFoundError:
        print('node 없음: 문법 검사 생략'); break
print('built →', OUT, '(artifact 모드)' if ARTIFACT else '(site 모드)', '' if ok else '— 오류 있음')
