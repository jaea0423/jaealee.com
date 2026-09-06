"""
scripts-pack.md 생성 스크립트
================================
14주차 강의 스크립트 전체를 누락 없이 단일 마크다운 파일로 합칩니다.

사용법:
  - 이 파일을 더블클릭하거나
  - cmd/PowerShell에서: python build-scripts-pack.py

결과: 같은 폴더에 scripts-pack.md 생성
"""
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


def clean_script(text: str):
    """타임코드(0:09) + 빈 줄 + 운영 안내문 제거."""
    out = []
    for line in text.split('\n'):
        s = line.strip()
        if not s:
            continue
        # 차시 헤더
        if re.match(r'^\[\s*\d+주차\s+\d+차시\s*\]', s):
            out.append(('chasi', s))
            continue
        # 타임코드만 있는 줄
        if re.match(r'^\d+:\d+(?::\d+)?$', s):
            continue
        # 운영 안내
        if '진도처리기간' in s or '동영상을 시청하시더라도' in s:
            continue
        # 차시 없음 안내 (괄호로 시작)
        if s.startswith('('):
            out.append(('note', s))
            continue
        # "13주차는 추후 업데이트 예정" 같은 안내
        if re.match(r'^\d+주차는', s):
            out.append(('note', s))
            continue
        out.append(('line', s))
    return out


def render_week(week: int, items):
    """한 주차의 마크다운 생성."""
    # 차시별로 묶기
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

        # 단락 결합: 3줄 이상 + 문장 끝이면 단락 끊기
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
                if len(para) >= 3 and re.search(r'[.?!다죠요함음임됨까]$', x):
                    out.append(' '.join(para))
                    out.append('')
                    para = []
        if para:
            out.append(' '.join(para))
            out.append('')
    return out


def build_markdown():
    md = []
    md.append('# 📖 강의 스크립트 전체 — 인공지능시대의 윤리')
    md.append('')
    md.append('> 1~14주차 강의 본문 전체. 타임코드와 운영 안내 제거. 차시별 정리.')
    md.append('> Ctrl+F로 직접 검색하거나 Claude에 첨부해 사용하세요.')
    md.append('')
    md.append('---')
    md.append('')
    md.append('## 📚 목차')
    md.append('')

    # 목차
    weeks = sorted(WEEK_INFO.keys())
    for w in weeks:
        md.append(f'- [WEEK {w:02d} — {WEEK_INFO[w]}](#week-{w:02d})')
    md.append('')
    md.append('---')
    md.append('')

    # 본문
    total_lines = 0
    loaded_weeks = 0
    missing_weeks = []
    for w in weeks:
        path = BASE / f'{w:02d}주차' / f'{w:02d}주차 강의 스크립트.txt'
        if not path.exists():
            missing_weeks.append(w)
            print(f'  ⚠️ 누락: {path.name}')
            continue
        text = path.read_text(encoding='utf-8')
        items = clean_script(text)
        line_count = sum(1 for t, _ in items if t == 'line')
        total_lines += line_count
        loaded_weeks += 1
        print(f'  ✓ {w:02d}주차: {line_count}개 본문 라인')

        md.append(f'## WEEK {w:02d} — {WEEK_INFO[w]}')
        md.append('')
        md.append(f'<a id="week-{w:02d}"></a>')
        md.append('')
        md.extend(render_week(w, items))
        md.append('---')
        md.append('')

    md.insert(4, f'**통계**: {loaded_weeks}개 주차 / 본문 {total_lines:,}줄')
    md.insert(5, '')
    if missing_weeks:
        md.insert(6, f'**누락된 주차**: {", ".join(str(w) for w in missing_weeks)}')
        md.insert(7, '')

    return '\n'.join(md)


def main():
    print('=' * 60)
    print('scripts-pack.md 빌더 시작')
    print('=' * 60)
    print()

    md = build_markdown()

    out_path = BASE / 'scripts-pack.md'
    out_path.write_text(md, encoding='utf-8')

    size_kb = out_path.stat().st_size // 1024
    chars = len(md)
    print()
    print('=' * 60)
    print(f'✅ 완료: {out_path}')
    print(f'   크기: {size_kb} KB ({chars:,} 자)')
    print('=' * 60)
    print()
    print('이제 새 Claude 세션에 다음 3개 파일을 함께 첨부하세요:')
    print('  1) bopo-pack.md')
    print('  2) scripts-pack.md')
    print('  3) prompt.md (시스템 프롬프트)')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
        import traceback
        traceback.print_exc()

    # 윈도우 더블클릭으로 실행 시 창이 바로 닫히지 않게
    if os.name == 'nt':
        try:
            input('\n엔터를 누르면 종료합니다...')
        except EOFError:
            pass
