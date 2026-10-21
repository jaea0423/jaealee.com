# 주차 묶음 파일 생성: week01.md ~ week07.md
# 한 파일 = 그 주차의 1-QUESTIONS(A) + 4-NOTES(C~D) + 2-SLIDES(A) + 3-TRANSCRIPT(B) + 0-INDEX 전체(개념→주차 지도)
# 전체 파일(2-SLIDES 600KB + 3-TRANSCRIPT 660KB)을 한 채팅에 붙이면 길이 한도를 넘길 수 있어, 주차별로 나눠 첨부하기 위한 것.
# 사용: 이 파일이 있는 폴더(midterm/)에서  python build_weeks.py
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
WEEK_TITLE = {1:'보안약점과 시큐어코딩 개요', 2:'SW개발보안 방법론·위협 모델링', 3:'Spring Boot 개발 환경·실습',
    4:'정규식과 입력값 검증·XSS 필터', 5:'인증과 인가 · OAuth2 · JWT', 6:'ORM·MyBatis / SQL 인젝션 / Command 인젝션',
    7:'프론트엔드 데이터 처리 / XSS / CSRF'}

def read(n): return open(f'{HERE}/{n}', encoding='utf-8').read()

def h1_sections(md, tag):
    # '# [TAG] N주차 …' 로 시작하는 1단계 섹션을 (주차, 본문) 으로 돌려준다. 파일 머리말은 버린다.
    out = []
    for m in re.finditer(r'^(# \[' + re.escape(tag) + r'\] (\d)주차[^\n]*\n.*?)(?=^# \[|\Z)', md, re.S | re.M):
        out.append((int(m.group(2)), m.group(1).rstrip('\n') + '\n'))
    return out

def notes_sections(md):
    # 4-NOTES는 2단계 제목. 'N주차'가 있으면 그 주차, 없으면(공통·시험 안내) 모든 주차에 넣는다.
    out = []
    for m in re.finditer(r'^(## \[4-NOTES\] ([^\n]*)\n.*?)(?=^## \[4-NOTES\]|\Z)', md, re.S | re.M):
        wm = re.search(r'(\d)주차', m.group(2))
        out.append((int(wm.group(1)) if wm else 0, m.group(1).rstrip('\n') + '\n'))
    return out

Q = h1_sections(read('1-QUESTIONS.md'), '1-QUESTIONS')
S = h1_sections(read('2-SLIDES.md'), '2-SLIDES')
T = h1_sections(read('3-TRANSCRIPT.md'), '3-TRANSCRIPT')
N = notes_sections(read('4-NOTES.md'))
IDX = read('0-INDEX.md')

for w in range(1, 8):
    parts = [f'# WEEK0{w} — {w}주차 {WEEK_TITLE[w]} (시큐어코딩 중간고사 주차 묶음)\n\n',
             f'> 이 파일 하나에 {w}주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.\n',
             '> 위치 표기 규칙은 전체 파일과 같다: `[2-SLIDES] N주차 M차시 p.X` = 교안, `[N주차 M차시 mm:ss]` = 발화, `[1-QUESTIONS] N주차 M차시 퀴즈 K` = 퀴즈.\n',
             '> 맨 앞의 찾아보기(0-INDEX)는 1~7주차 전체 지도다. 다른 주차 개념이면 그 주차 파일(weekNN.md)을 봐야 한다.\n\n',
             '---\n\n', IDX.rstrip('\n') + '\n\n---\n\n']
    for wk, body in Q:
        if wk == w: parts.append(body + '\n')
    parts.append('---\n\n')
    parts.append(f'# [4-NOTES] {w}주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.\n\n')
    for wk, body in N:
        if wk in (w, 0): parts.append(body + '\n')
    parts.append('---\n\n')
    for wk, body in S:
        if wk == w: parts.append(body + '\n')
    parts.append('---\n\n')
    for wk, body in T:
        if wk == w: parts.append(body + '\n')
    txt = ''.join(parts)
    open(f'{HERE}/week0{w}.md', 'w', encoding='utf-8').write(txt)
    print(f'week0{w}.md {len(txt.encode("utf-8"))//1024} KB')
