"""
study-pack.md 생성 스크립트
================================
사용법:
  1) 이 파일을 더블클릭하거나
  2) cmd/PowerShell에서 `python build-study-pack.py`

결과: 같은 폴더에 study-pack.md 생성
"""
import json
import os
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent

WEEK_INFO = {
    1: "윤리이론 (공리주의·칸트·상황윤리)",
    2: "AI 정의·역사·유형·한계",
    3: "편향성·투명성·책무성 ★ 족보 최다",
    4: "자율성·전자인격",
    5: "위험관리·마케팅·분배정의",
    6: "자율주행차 윤리",
    7: "사용 주의·신뢰성·인간중심성",
    9: "응용·인간향상·로봇 ★ 족보",
    10: "소셜·수술·군사로봇 ★ 족보",
    11: "미래사회·미래직업",
    12: "권력·감시·사회조종",
    13: "인간 관계·인간 감정",
    14: "정체성·존엄성·자유의지",
}


# ============================================================
# 1. 데이터 로드
# ============================================================

def load_from_keywords_js():
    """keywords-data.js 안의 PAST_EXAM, KEYWORDS 추출."""
    js_path = BASE / 'keywords-data.js'
    if not js_path.exists():
        return None, []
    txt = js_path.read_text(encoding='utf-8')

    past_exam = None
    m = re.search(r'const\s+PAST_EXAM\s*=\s*(\{.*?\});\s*\n\s*const', txt, re.DOTALL)
    if m:
        try:
            past_exam = json.loads(m.group(1))
        except Exception as e:
            print('PAST_EXAM 파싱 실패:', e)

    keywords = []
    m = re.search(r'const\s+KEYWORDS\s*=\s*(\[.*\])\s*;\s*$', txt, re.DOTALL)
    if m:
        try:
            keywords = json.loads(m.group(1))
        except Exception as e:
            print('KEYWORDS 파싱 실패:', e)

    return past_exam, keywords


def clean_script(text: str):
    """타임코드(0:09)와 빈 줄을 정리해 차시·라인 구조로 변환."""
    out = []
    for line in text.split('\n'):
        s = line.strip()
        if not s:
            continue
        if re.match(r'^\[\s*\d+주차\s+\d+차시\s*\]', s):
            out.append(('chasi', s))
            continue
        if re.match(r'^\d+:\d+(?::\d+)?$', s):
            continue
        if '진도처리기간' in s or '동영상을 시청하시더라도' in s:
            continue
        if s.startswith('('):
            out.append(('note', s))
            continue
        if re.match(r'^\d+주차는', s):
            out.append(('note', s))
            continue
        out.append(('line', s))
    return out


def load_scripts():
    """1~14주차 강의 스크립트 로드."""
    data = {}
    for w in range(1, 15):
        if w == 8:
            continue
        path = BASE / f'{w:02d}주차' / f'{w:02d}주차 강의 스크립트.txt'
        if path.exists():
            data[w] = clean_script(path.read_text(encoding='utf-8'))
    return data


# ============================================================
# 2. 마크다운 빌드
# ============================================================

def render_chasi_blocks(items):
    """차시별로 묶기 + 단락 결합."""
    blocks = []
    title = None
    lines = []
    for typ, txt in items:
        if typ == 'chasi':
            if title is not None:
                blocks.append((title, lines))
            title = txt
            lines = []
        else:
            lines.append((typ, txt))
    if title is not None:
        blocks.append((title, lines))
    if not blocks and items:
        blocks.append((None, [(t, x) for t, x in items]))

    out = []
    for t, ls in blocks:
        if t:
            clean_title = re.sub(r'^\[\s*|\s*\]$', '', t)
            out.append(f'#### {clean_title}')
            out.append('')
        para = []
        for typ, x in ls:
            if typ == 'note':
                if para:
                    out.append(' '.join(para))
                    out.append('')
                    para = []
                out.append(f'> ※ {x}')
                out.append('')
            else:
                para.append(x)
                if len(para) >= 3 and re.search(r'[.?!다죠요함음임됨]$', x):
                    out.append(' '.join(para))
                    out.append('')
                    para = []
        if para:
            out.append(' '.join(para))
            out.append('')
    return out


def build_markdown(past_exam, keywords, scripts):
    md = []
    md.append('# 인공지능시대의 윤리 — 학습 통합본 (study-pack.md)')
    md.append('')
    md.append('> **이 파일 = 족보 + 강의 스크립트 + 핵심 키워드 정리.**')
    md.append('> 새 Claude 세션이나 코워크에 첨부하고 아래 시스템 프롬프트를 사용하세요.')
    md.append('')
    md.append('## ⚙️ 시스템 프롬프트 (복사해서 사용)')
    md.append('')
    md.append('```')
    md.append('첨부한 study-pack.md만 보고 답한다. 외부 지식은 마지막 수단.')
    md.append('')
    md.append('답변 우선순위 (반드시 이 순서로):')
    md.append('1. 족보(🔥) 섹션에서 먼저 찾는다. 있으면 즉시 답.')
    md.append('2. 없으면 강의 스크립트 전문에서 찾는다.')
    md.append('3. 그래도 없으면 외부 지식으로 답한다.')
    md.append('')
    md.append('답변 형식 (짧고 빠르게):')
    md.append('- **정답**: [단어 또는 ①②③ 번호]')
    md.append('- **출처**: [족보 / 강의 N주차 / 외부]')
    md.append('- **근거**: [한 줄 핵심]')
    md.append('')
    md.append('장황한 설명 금지. 헤더·인사·생각 과정 출력 금지.')
    md.append('객관식이면 정답 보기 번호 + 단어. 단답형이면 정확한 단어 하나만.')
    md.append('확신 없으면 "확신 부족: [후보 답]" 으로 표시.')
    md.append('```')
    md.append('')
    md.append('---')
    md.append('')
    md.append('## 📋 빠른 사용 예시')
    md.append('')
    md.append('**입력 (캡처 또는 텍스트)**: "편향과 편견의 차이를 바르게 설명한 것은?"')
    md.append('')
    md.append('**기대 출력**:')
    md.append('```')
    md.append('정답: ② 편향은 특정 행동 성향을 자동으로 야기할 수 있다.')
    md.append('출처: 족보 객관식 Q1 (3주차 편향성)')
    md.append('근거: 편견=심리적 고정관념, 편향=시스템의 구조적 기울어짐(자동 행동 야기).')
    md.append('```')
    md.append('')
    md.append('---')
    md.append('')

    # 1. 족보
    if past_exam:
        mc = past_exam.get('객관식', [])
        sa = past_exam.get('단답형', [])
        md.append(f'## 🔥 족보 (2024학년도 겨울학기 — 객관식 {len(mc)} + 단답형 {len(sa)} = 총 {len(mc)+len(sa)}문제)')
        md.append('')
        md.append('> ⚠️ 2025학년도 여름학기는 다르게 출제됨. 키워드·주제 패턴 참고용.')
        md.append('')

        md.append(f'### 객관식 ({len(mc)}문제)')
        md.append('')
        for i, q in enumerate(mc, 1):
            md.append(f"#### Q{i}. [{q.get('주차','?')}주차 · {q.get('주제','')}]")
            md.append('')
            md.append(f"**문제**: {q.get('질문','')}")
            md.append('')
            md.append('**보기**:')
            ans = q.get('정답', [])
            if not isinstance(ans, list):
                ans = [ans]
            ans_strip = [a.strip() for a in ans]
            for j, opt in enumerate(q.get('보기', []), 1):
                mark = '✅ ' if opt.strip() in ans_strip else ''
                md.append(f'- {mark}{j}) {opt}')
            md.append('')
            md.append(f"**정답**: {' / '.join(ans)}")
            md.append('')
            if q.get('해설'):
                md.append(f"**해설**: {q['해설']}")
            md.append('')

        md.append(f'### 단답형 주관식 ({len(sa)}문제)')
        md.append('')
        for i, q in enumerate(sa, 1):
            md.append(f"#### S{i}. [{q.get('주차','?')}주차 · {q.get('주제','')}]")
            md.append('')
            md.append(f"**문제**: {q.get('질문','')}")
            md.append('')
            md.append(f"**정답**: {q.get('정답','')}")
            md.append('')
            if q.get('해설'):
                md.append(f"**해설**: {q['해설']}")
            md.append('')

    md.append('---')
    md.append('')

    # 2. 핵심 키워드
    if keywords:
        md.append(f'## 📚 핵심 키워드 정리 ({len(keywords)}개)')
        md.append('')
        by_week = {}
        for k in keywords:
            w = '?'
            for i in range(1, 15):
                if k.get('file', '').startswith(f'{i:02d}주차/'):
                    w = i
                    break
            by_week.setdefault(w, []).append(k)

        for w in sorted(by_week.keys(), key=lambda x: (isinstance(x, str), x)):
            md.append(f"### WEEK {str(w).zfill(2)} — {WEEK_INFO.get(w, '')}")
            md.append('')
            for k in by_week[w]:
                bopo = ' 🔥' if k.get('fromBopo') else ''
                eng = f" (*{k['english']}*)" if k.get('english') else ''
                md.append(f"- **{k.get('keyword','')}**{eng}{bopo}: {k.get('summary','')}")
            md.append('')

    md.append('---')
    md.append('')

    # 3. 강의 스크립트
    md.append('## 📖 강의 스크립트 전문')
    md.append('')
    for w in sorted(scripts.keys()):
        md.append(f"### WEEK {w:02d} — {WEEK_INFO.get(w, '')}")
        md.append('')
        md.extend(render_chasi_blocks(scripts[w]))
        md.append('')

    return '\n'.join(md)


# ============================================================
# 3. 실행
# ============================================================

def main():
    print('데이터 불러오는 중...')
    past_exam, keywords = load_from_keywords_js()
    if past_exam is None:
        print('⚠️ keywords-data.js를 찾지 못했거나 PAST_EXAM 파싱 실패. 족보 섹션이 비어있을 수 있음.')
    print(f'  - 족보: 객관식 {len(past_exam.get("객관식", [])) if past_exam else 0}, 단답형 {len(past_exam.get("단답형", [])) if past_exam else 0}')
    print(f'  - 키워드: {len(keywords)}개')

    scripts = load_scripts()
    total_lines = sum(1 for items in scripts.values() for t, _ in items if t == 'line')
    print(f'  - 강의 스크립트: {len(scripts)}개 주차, 총 {total_lines}개 본문 라인')

    print('마크다운 빌드 중...')
    md = build_markdown(past_exam, keywords, scripts)

    out_path = BASE / 'study-pack.md'
    out_path.write_text(md, encoding='utf-8')
    size_kb = out_path.stat().st_size // 1024
    print(f'\n✅ 생성됨: {out_path}')
    print(f'   크기: {size_kb} KB ({len(md):,} 자)')
    print(f'   사용법: 새 Claude 세션에 첨부하세요.')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'❌ 오류: {e}')
        sys.exit(1)
    # 더블클릭으로 실행한 경우 창이 바로 닫히지 않도록
    if os.name == 'nt' and not sys.stdout.isatty():
        input('\n엔터를 누르면 종료합니다...')
