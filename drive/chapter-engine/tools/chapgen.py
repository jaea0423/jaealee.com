# 개념노트 A4 인쇄판 — 공통 생성 도구 (drive/chapter-engine/tools/chapgen.py)
# 규칙: ../README.md
import html as H, json
# ═════════ 도우미 ═════════
def v(x): return f'<i class="v">{x}</i>'
def sb(x, s): return f'{v(x)}<sub>{s}</sub>'
def frac(a, b): return f'<span class="frac"><span>{a}</span><span>{b}</span></span>'
FN = []
def fn(kind, text):
    FN.append((kind, text)); return f'<sup class="fr" data-fn="{len(FN) - 1}"></sup>'
def hl(t): return f'<mark>{t}</mark>'
def code(lang, title, src):
    out = []
    for line in src.strip(chr(10)).split(chr(10)):
        if '#' in line:
            c, cm = line.split('#', 1); out.append(H.escape(c) + '<span class="cm">#' + H.escape(cm) + '</span>')
        else: out.append(H.escape(line))
    return f'<div class="code"><div class="ch"><span class="lang">{lang}</span><span>{title}</span></div><pre>{chr(10).join(out)}</pre></div>'
def proof(title, steps):
    lis = ''.join(f'<li class="{c}"><div class="k">{l}</div><div class="b"><div>{m}</div>{f"<div class=why>{w}</div>" if w else ""}</div></li>' for c, l, m, w in steps)
    return f'<div class="proof"><div class="ph">{title}</div><ol>{lis}</ol></div>'
def unit(title, body, cls=''):
    h = f'<h3>{title}</h3>' if title else ''
    return f'<div class="unit {cls}">{h}{body}</div>'
def table(head, rows, widths=None, cls=''):
    cg = ''.join(f'<col style="width:{w}">' for w in widths) if widths else ''
    th = ''.join(f'<th class="{"c" if h.startswith("^") else ""}">{h.lstrip("^")}</th>' for h in head)
    tr = ''
    for r in rows:
        rc = ''
        if isinstance(r, tuple) and r and r[0] in ('sel', 'bad', 'tot'): rc, r = r[0], r[1]
        tr += f'<tr class="{rc}">' + ''.join(f'<td class="{"c" if head[i].startswith("^") else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>'
    return f'<table class="t {cls}"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


# ── 공통 그림 ──
# ── 그림 (색: 검정 · 노랑 선택 · 빨강 반례) ──
YEL, RED = '#FFD84D', '#C0341D'
def layers(iv):
    lay, out = [], []
    for (s, f) in iv:
        for li, row in enumerate(lay):
            if all(f2 <= s or f <= s2 for (s2, f2) in row): row.append((s, f)); out.append(li); break
        else: lay.append([(s, f)]); out.append(len(lay) - 1)
    return out, len(lay)
def fig_iv(iv, names, sel=(), bad=(), lo=0, hi=14, W=680, title=''):
    lv, nl = layers(iv); U = (W - 40) / (hi - lo); X0 = 20; RH = 30; base = nl * RH + 14
    o = [f'<svg viewBox="0 0 {W} {base + 30}" role="img"><title>{title}</title>']
    for idx, ((s, f), l) in enumerate(zip(iv, lv)):
        y = base - (l + 1) * RH + 3; x1, x2 = X0 + (s - lo) * U, X0 + (f - lo) * U
        fill = YEL if idx in sel else ('#F7D9D1' if idx in bad else '#fff'); st = RED if idx in bad else '#000'
        o.append(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="23" fill="{fill}" stroke="{st}" stroke-width="1.6"/>')
        o.append(f'<text x="{(x1 + x2) / 2}" y="{y + 16.5}" font-size="14" font-weight="800" text-anchor="middle" fill="{st}">{names[idx]}</text>')
    o.append(f'<line x1="{X0}" y1="{base + 4}" x2="{X0 + (hi - lo) * U}" y2="{base + 4}" stroke="#000" stroke-width="1.6"/>')
    for t in range(lo, hi + 1):
        x = X0 + (t - lo) * U
        o.append(f'<line x1="{x}" y1="{base + 4}" x2="{x}" y2="{base + 10}" stroke="#000" stroke-width="1.4"/><text x="{x}" y="{base + 25}" font-size="13" font-weight="600" text-anchor="middle">{t}</text>')
    o.append('</svg>'); return ''.join(o)
def fig_tree(nodes, edges, W=680, Hh=250, title=''):
    """nodes: id -> (x, y, label, leaf);  edges: (부모, 자식, 비트)"""
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img"><title>{title}</title>']
    for p, c, bit in edges:
        x1, y1 = nodes[p][:2]; x2, y2 = nodes[c][:2]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1.5"/>')
        o.append(f'<text x="{(x1 + x2) / 2 + (-9 if bit == "0" else 9)}" y="{(y1 + y2) / 2 + 2}" font-size="13" font-weight="800" text-anchor="middle">{bit}</text>')
    for _, (x, y, lab, leaf) in nodes.items():
        if leaf: o.append(f'<rect x="{x - 30}" y="{y - 15}" width="60" height="30" fill="{YEL}" stroke="#000" stroke-width="1.6"/>')
        else: o.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#fff" stroke="#000" stroke-width="1.6"/>')
        o.append(f'<text x="{x}" y="{y + 5}" font-size="13.5" font-weight="800" text-anchor="middle">{lab}</text>')
    o.append('</svg>'); return ''.join(o)
def tri(cx, top, w, h, label, inner):
    """삼각형으로 그린 트리 + 표시할 노드"""
    o = [f'<polygon points="{cx},{top} {cx - w / 2},{top + h} {cx + w / 2},{top + h}" fill="#fff" stroke="#000" stroke-width="1.5"/>',
         f'<text x="{cx}" y="{top + h + 27}" font-size="15" font-weight="800" text-anchor="middle">{label}</text>']
    for kind, x, y, t in inner:
        if kind == 'leaf':
            fill = YEL if t[0] in 'xyz' or t.startswith('w') else '#fff'
            o.append(f'<rect x="{x - 15}" y="{y - 12}" width="30" height="24" fill="{fill}" stroke="#000" stroke-width="1.5"/><text x="{x}" y="{y + 5}" font-size="14" font-weight="800" font-style="italic" text-anchor="middle" font-family="STIX Two Text, serif">{t}</text>')
        elif kind == 'line': o.append(f'<line x1="{x}" y1="{y}" x2="{t[0]}" y2="{t[1]}" stroke="#000" stroke-width="1.4"/>')
        elif kind == 'dot': o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="#000" stroke-width="1.4"/>')
        elif kind == 'note': o.append(f'<text x="{x}" y="{y}" font-size="12.5" font-weight="600" text-anchor="middle">{t}</text>')
    return ''.join(o)
def deep_pair(cx, top, h, l, r, mid=None):
    py = top + h - 62
    out = [('line', cx, py, (cx - 22, py + 30)), ('line', cx, py, (cx + 22, py + 30)), ('dot', cx, py, ''), ('leaf', cx - 22, py + 30, l), ('leaf', cx + 22, py + 30, r)]
    if mid: out.append(('leaf', cx - 70, top + h * .5, mid))
    return out
def fig_pair(left, right, arrow, title):
    o = [f'<svg viewBox="0 0 680 236" role="img"><title>{title}</title>', tri(170, 10, 260, 180, *left), tri(510, 10, 260, 180, *right)]
    o.append(f'<text x="340" y="100" font-size="14" font-weight="800" text-anchor="middle">{arrow}</text><line x1="300" y1="110" x2="380" y2="110" stroke="#000" stroke-width="1.6"/><polygon points="380,110 372,105 372,115" fill="#000"/>')
    o.append('</svg>'); return ''.join(o)

def build(out, *, title, run, kick, h1, h1_en, chapters, engine='../../../chapter-engine', pdf='', back='../index.html',
          foot_l='Kangwon National University, Dept. of CSE', foot_r='이재아 202313564'):
    """chapters: [(번호, 장 제목, 출처, [unit(...), ...]), ...]"""
    cover = f'<div class="cover"><div class="top"><div class="kick">{kick}</div><h1>{h1}<span>{h1_en}</span></h1></div><div class="toc"></div></div>'
    chaps = ''.join(f'<div data-title="{no}. {H.escape(t)}"><h2 class="chap">{no}. {t}<small>{w}</small></h2>{"".join(us)}</div>' for no, t, w, us in chapters)
    pdfbtn = f'<a class="btn" href="./{pdf}" download>PDF 내려받기</a>' if pdf else ''
    page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=STIX+Two+Text:ital,wght@1,500&display=swap">
<link rel="stylesheet" href="{engine}/chapter.css"></head>
<body data-run="{H.escape(run)}" data-foot-l="{H.escape(foot_l)}" data-foot-r="{H.escape(foot_r)}">
<div class="bar"><a href="{back}">강의 정리로</a><span>A4 <span id="total"></span></span><button type="button" class="btn" onclick="window.print()">출력</button>{pdfbtn}</div>
<main id="pages"></main>
<template id="cover-src">{cover}</template>
<div id="src">{chaps}</div>
<script type="application/json" id="fn-data">{json.dumps([[k, t] for k, t in FN], ensure_ascii=False)}</script>
<script src="{engine}/chapter.js"></script>
</body></html>'''
    open(out, 'w').write(page)


# ── 정리노트 (summary.css · summary.js) ──
def sunit(title, body, ref=''):
    """정리노트 한 칸 — 단 하나 안에 들어가야 함. ref = 개념노트 쪽 번호"""
    r = f'<span class="ref">→ 개념노트 p.{ref}</span>' if ref else ''
    h = f'<h3><span>{title}</span>{r}</h3>' if title else ''
    return f'<div class="unit">{h}{body}</div>'
def trap(items, title='헷갈리는 점 · 판서 정정'):
    return f'<div class="trap"><b>{title}</b><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'
def exam(items, title='시험 포인트'):
    return f'<div class="exam"><b>{title}</b><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'

def build_summary(out, *, title, unit, kick, h1, h1_en, lead, chapters, engine='../../chapter-engine', pdf='', back='../lecture/index.html',
                  foot_l='Kangwon National University, Dept. of CSE', foot_r='이재아 202313564'):
    """chapters: [(번호, 장 제목, 출처, 개념노트 쪽, [sunit(...), ...]), ...] — 첫 sunit 에 장 제목이 붙는다"""
    head = (f'<div class="shead">' + (f'<div class="kick">{kick}</div>' if kick else '') + f'<h1>{h1}<span>{h1_en}</span></h1>' + (f'<p>{lead}</p>' if lead else '') +
            '<table class="t"><colgroup><col style="width:56%"><col style="width:20%"><col style="width:24%"></colgroup>'
            '<thead><tr><th>장</th><th class="c">정리노트</th><th class="c">개념노트</th></tr></thead><tbody></tbody></table></div>')
    chs = ''
    for no, t, w, ref, us in chapters:
        first = us[0].replace('<div class="unit">', f'<div class="unit"><h2 class="chap">{no}. {t}<small>{w}</small></h2>', 1)
        chs += f'<div data-title="{no}. {H.escape(t)}" data-ref="{ref}">{first}{"".join(us[1:])}</div>'
    pdfbtn = f'<a class="btn" href="./{pdf}" download>PDF 내려받기</a>' if pdf else ''
    page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=STIX+Two+Text:ital,wght@1,500&display=swap">
<link rel="stylesheet" href="{engine}/chapter.css"><link rel="stylesheet" href="{engine}/summary.css"></head>
<body data-unit="{H.escape(unit)}" data-foot-l="{H.escape(foot_l)}" data-foot-r="{H.escape(foot_r)}">
<div class="bar"><a href="{back}">강의 정리로</a><span>정리노트 A4 <span id="total"></span></span><button type="button" class="btn" onclick="window.print()">출력</button>{pdfbtn}</div>
<main id="pages"></main>
<template id="cover-src">{head}</template>
<div id="src">{chs}</div>
<script type="application/json" id="fn-data">{json.dumps([[k, t] for k, t in FN], ensure_ascii=False)}</script>
<script src="{engine}/summary.js"></script>
</body></html>'''
    open(out, 'w').write(page)


# ── 암기노트 (memorize.css · memorize.js) ──
def qa(title, rows):
    """질문 | 답 표 한 묶음. rows = [(질문, 답), ...]"""
    tr = ''.join(f'<tr><td>{q}</td><td>{a}</td></tr>' for q, a in rows)
    return (f'<div class="unit"><h3>{title}</h3><table class="t qa"><colgroup><col style="width:44%"><col style="width:56%"></colgroup>'
            f'<thead><tr><th>질문</th><th>답</th></tr></thead><tbody>{tr}</tbody></table></div>')

def build_memorize(out, *, title, subject, h1, h1_en, ranges, engine='../../chapter-engine', pdf='', back='../lecture/index.html',
                   foot_l='Kangwon National University, Dept. of CSE', foot_r='이재아 202313564'):
    """ranges: [(범위 이름, 출처, 개념노트 쪽 범위 문자열, [qa(...), ...]), ...] — 범위마다 새 쪽"""
    head = (f'<div class="mhead"><h1>{h1}<span>{h1_en}</span></h1>'
            '<table class="t"><colgroup><col style="width:56%"><col style="width:20%"><col style="width:24%"></colgroup>'
            '<thead><tr><th>범위</th><th class="c">암기노트</th><th class="c">개념노트</th></tr></thead><tbody></tbody></table></div>')
    rs = ''.join(f'<div data-title="{H.escape(n)}" data-ref="{ref}"><div class="mrange">{n}<small>{w}</small></div>{"".join(us)}</div>' for n, w, ref, us in ranges)
    pdfbtn = f'<a class="btn" href="./{pdf}" download>PDF 내려받기</a>' if pdf else ''
    page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=STIX+Two+Text:ital,wght@1,500&display=swap">
<link rel="stylesheet" href="{engine}/chapter.css"><link rel="stylesheet" href="{engine}/memorize.css"></head>
<body data-subject="{H.escape(subject)}" data-foot-l="{H.escape(foot_l)}" data-foot-r="{H.escape(foot_r)}">
<div class="bar"><a href="{back}">강의 정리로</a><span>암기노트 A4 <span id="total"></span></span><button type="button" class="btn" onclick="window.print()">출력</button>{pdfbtn}</div>
<main id="pages"></main>
<template id="cover-src">{head}</template>
<div id="src">{rs}</div>
<script type="application/json" id="fn-data">{json.dumps([[k, t] for k, t in FN], ensure_ascii=False)}</script>
<script src="{engine}/memorize.js"></script>
</body></html>'''
    open(out, 'w').write(page)
