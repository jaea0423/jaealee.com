# 마크다운 → 검색 index.html 한 개. (kit 템플릿 CSS 재사용 + 자체 데이터 모델/JS)
# 사용: 이 파일이 있는 폴더(midterm/)에서  python build_page.py
#   - 읽는 파일: 같은 폴더의 00-PROMPT.md, 0-INDEX.md, 1-QUESTIONS.md, 2-SLIDES.md, 3-TRANSCRIPT.md, 4-NOTES.md
#   - kit 템플릿: 같은 폴더의 exam-kit/ (template/exam.tpl.html, themes/navy-sky.css). 다른 곳이면 환경변수 SC_KIT로 지정
import re, os, json

HERE = os.path.dirname(os.path.abspath(__file__))           # 스크립트가 있는 폴더 = 마크다운이 있는 폴더
KIT = os.environ.get('SC_KIT') or (f'{HERE}/exam-kit' if os.path.isdir(f'{HERE}/exam-kit') else '/home/claude/kit/exam-kit')
THEME = f'{KIT}/themes/navy-sky.css'
OUT = f'{HERE}/index.html'

WEEK_TITLE = {1:'보안약점과 시큐어코딩 개요', 2:'SW개발보안 방법론·위협 모델링', 3:'Spring Boot 개발 환경·실습',
    4:'정규식과 입력값 검증·XSS 필터', 5:'인증과 인가 · OAuth2 · JWT', 6:'ORM·MyBatis / SQL 인젝션 / Command 인젝션',
    7:'프론트엔드 데이터 처리 / XSS / CSRF'}
HAS_NOTES = {1,2,3,4,5}  # NN-1.html 정리 페이지가 있는 주차

# 동의어 묶음 (검색 확장용) — build_exam.py와 동일
SYN = [
 ['보안약점','Weakness','CWE','취약점','Vulnerability'],
 ['SQL Injection','SQL 인젝션','SQL 삽입','에스큐엘 인젝션','에스큐엘','SQLi','CWE-89'],
 ['PreparedStatement','프리페어드 스테이트먼트','파라미터 바인딩','바인딩','setString'],
 ['XSS','Cross-Site Scripting','크로스사이트 스크립팅','크로스 사이트 스크립팅','크로스사이트스크립팅','CWE-79'],
 ['Reflected XSS','반사형 XSS','리플렉티드'],
 ['Stored XSS','저장형 XSS','스토어드'],
 ['DOM XSS','DOM 기반 XSS','돔 기반','document.write','innerHTML'],
 ['CSRF','Cross-Site Request Forgery','크로스사이트 요청 위조','크로스 사이트 요청 위조','XSRF','CWE-352'],
 ['Command Injection','커맨드 인젝션','명령어 삽입','명령 삽입','OS Command','CWE-78'],
 ['CSP','Content Security Policy','콘텐츠 보안 정책','컨텐츠 시큐리티 폴리시'],
 ['SameSite','세임사이트','Strict','Lax'],
 ['HTML Encoding','HTML 인코딩','이스케이프','Escape','엔티티','escapeHtml','textContent'],
 ['화이트리스트','Whitelist','최소 허용'],
 ['ORM','Object-Relational Mapping','객체 관계 매핑','JPA','Hibernate','하이버네이트'],
 ['MyBatis','마이바티스','Mapper','매퍼','동적 SQL'],
 ['Dirty Checking','더티 체킹','변경 감지'],
 ['Mass Assignment','대량 할당','DTO'],
 ['Authentication','인증','로그인'],
 ['Authorization','인가','권한','RBAC','ABAC','PBAC','최소 권한'],
 ['Session','세션','JSESSIONID','세션 쿠키','HttpOnly','Secure'],
 ['Token','토큰','Bearer','베어러'],
 ['OAuth2','OAuth 2.0','권한 위임','Authorization Code','인가 코드','PKCE','state'],
 ['JWT','JSON Web Token','클레임','Claims','HS256','RS256'],
 ['Refresh Token','리프레시 토큰','토큰 회전','Rotation'],
 ['MFA','Multi-Factor','다중 인증','OTP','FIDO2','WebAuthn'],
 ['HSTS','Strict-Transport-Security'],
 ['IDOR','Insecure Direct Object References','직접 객체 참조','권한 상승','수평 권한','수직 권한'],
 ['Regex','정규식','Pattern','Matcher','정규 표현식'],
 ['ReDoS','레도스','백트래킹','Backtracking'],
 ['Filter','필터','Interceptor','인터셉터','DispatcherServlet'],
 ['Threat Modeling','위협 모델링','STRIDE','DREAD','MS-SDL','MTMT'],
 ['SSR','CSR','Server-Side Rendering','Client-Side Rendering','서버 사이드 렌더링','클라이언트 사이드 렌더링'],
 ['localStorage','로컬 저장소','로컬 스토리지','Same-Origin','sessionStorage'],
 ['CORS','교차 출처','Cross-Origin'],
 ['SQLMap','에스큐엘맵'],
 ['OWASP ZAP','ZAP','Active Scan','Burp','버프스위트'],
 ['코드 리뷰','Code Review','SAST','DAST','정적 분석','동적 분석'],
]
def norm(s): return re.sub(r'\s+','',s).lower()

def read(p): return open(p, encoding='utf-8').read()

def pdf_path(w, c):
    ww = f'{w:02d}'
    return f'../week{ww}/{ww}-1-slides{c}.pdf' if w == 1 else f'../week{ww}/{ww}-{c}-slides1.pdf'
def notes_path(w):
    return f'../week{w:02d}/{w:02d}-1.html' if w in HAS_NOTES else ''

# ---------- 파싱 ----------
def split_chasi(md, tag):
    # [(week,chasi,kw,inner_text)]
    out = []
    for m in re.finditer(rf'^# \[{tag}\] (\d)주차 (\d)차시[^\n]*\n(.*?)(?=^# \[{tag}\]|\Z)', md, re.S|re.M):
        w, c, body = int(m.group(1)), int(m.group(2)), m.group(3)
        kwm = re.search(r'^키워드:\s*(.+)$', body, re.M)
        out.append((w, c, kwm.group(1).strip() if kwm else '', body))
    return out

def parse_slides():
    md = read(f'{HERE}/2-SLIDES.md'); items = []
    for w, c, kw, body in split_chasi(md, '2-SLIDES'):
        for m in re.finditer(r'^## \[2-SLIDES\] \d주차 \d차시 p\.(\S+)(?: · ([^\n]*))?\n(.*?)(?=^## \[2-SLIDES\]|\Z)', body, re.S|re.M):
            page, title, txt = m.group(1), (m.group(2) or '').strip(), m.group(3).strip()
            items.append({'week':w,'chasi':c,'page':page,'title':title,'body':txt,'kw':kw,
                          'pdf':pdf_path(w,c),'notes':notes_path(w)})
    return items

def parse_quizzes():
    # 1-QUESTIONS.md는 build_exam.py가 "문제 하나 = 섹션 하나"로 정규화해 둔 형식:
    #   ## [1-QUESTIONS] W주차 C차시 p.X · 퀴즈 K  /  문제: … / 1) … / 정답: … / 해설: … / 출처: …
    #   ## [1-QUESTIONS] W주차 C차시 p.X · 비고   (※ 메모 줄들)
    md = read(f'{HERE}/1-QUESTIONS.md'); items = []
    for w, c, kw, body in split_chasi(md, '1-QUESTIONS'):
        for m in re.finditer(r'^## \[1-QUESTIONS\] \d주차 \d차시 p\.(\d+) · (퀴즈 (\d+)|비고)\n(.*?)(?=^## \[1-QUESTIONS\]|\Z)', body, re.S|re.M):
            page, lab, n, sec = m.group(1), m.group(2), m.group(3), m.group(4)
            lines = [l.rstrip() for l in sec.split('\n') if l.strip()]
            if lab == '비고':
                items.append({'week':w,'chasi':c,'n':0,'page':page,'q':'비고(교안 퀴즈 쪽 메모)','opts':[],'a':'','detail':' '.join(lines),
                              'src':'','kw':kw,'pdf':pdf_path(w,c),'notes':notes_path(w)}); continue
            q = a = detail = src = ''; opts = []
            for l in lines:
                if l.startswith('문제: '): q = l[4:].strip()
                elif l.startswith('정답: '): a = l[4:].strip()
                elif l.startswith('해설: '): detail = l[4:].strip()
                elif l.startswith('출처: '): src = l[4:].strip()
                elif re.match(r'^\d\) ', l): opts.append(l)
            items.append({'week':w,'chasi':c,'n':int(n),'page':page,'q':q,'opts':opts,'a':a,'detail':detail,'src':src,
                          'kw':kw,'pdf':pdf_path(w,c),'notes':notes_path(w)})
    return items

def parse_tx():
    md = read(f'{HERE}/3-TRANSCRIPT.md'); items = []
    for m in re.finditer(r'^\[(\d)주차 (\d)차시 (\d+:\d+)\] (.*)$', md, re.M):
        items.append({'week':int(m.group(1)),'chasi':int(m.group(2)),'t':m.group(3),'text':m.group(4)})
    return items

def parse_notes():
    md = read(f'{HERE}/4-NOTES.md'); items = []
    for m in re.finditer(r'^## \[4-NOTES\] (.*?)\n(.*?)(?=^## \[4-NOTES\]|\Z)', md, re.S|re.M):
        head, body = m.group(1).strip(), m.group(2).strip()
        wm = re.search(r'(\d)주차 (\d)차시', head)
        w = int(wm.group(1)) if wm else 0; c = int(wm.group(2)) if wm else 0
        gm = re.search(r'\(([A-D])\)\s*$', head)
        grade = gm.group(1) if gm else 'C'
        title = re.sub(r'\s*\([A-D]\)\s*$','',head)
        kwm = re.search(r'^키워드:\s*(.+)$', body, re.M)
        kw = kwm.group(1).strip() if kwm else ''
        body2 = re.sub(r'^키워드:.*$','',body, flags=re.M).strip()
        items.append({'week':w,'chasi':c,'title':title,'grade':grade,'body':body2,'kw':kw,'notes':notes_path(w) if w else '','pdf':pdf_path(w,c) if w else ''})
    return items

slides = parse_slides(); quizzes = parse_quizzes(); tx = parse_tx(); notes = parse_notes()

# ---------- 0-INDEX: 핵심/전체 위치 계산 ----------
# 핵심 = 개념이 교안 페이지 제목 / 퀴즈 질문·보기 / 4-NOTES 제목에 나온 (주차,차시)
title_by_wc = {}
for s in slides: title_by_wc.setdefault((s['week'],s['chasi']),[]).append(norm(s['title']))
for q in quizzes: title_by_wc.setdefault((q['week'],q['chasi']),[]).append(norm(q['q']+' '+' '.join(q['opts'])))
for n in notes:
    if n['week']: title_by_wc.setdefault((n['week'],n['chasi']),[]).append(norm(n['title']))
body_by_wc = {}
for s in slides: body_by_wc.setdefault((s['week'],s['chasi']),[]).append(norm(s['body']))
tx_by_w = {}
for t in tx: tx_by_w.setdefault(t['week'],[]).append(norm(t['text']))

index = []
for syns in SYN:
    ns = [norm(x) for x in syns]
    core, alll = [], []
    for (w,c) in sorted(title_by_wc):
        tt = ' '.join(title_by_wc.get((w,c),[]))
        if any(x in tt for x in ns): core.append([w,c])
    for (w,c) in sorted(body_by_wc):
        bb = ' '.join(body_by_wc.get((w,c),[]))
        if any(x in bb for x in ns): alll.append([w,c])
    txw = sorted(w for w in tx_by_w if any(x in ' '.join(tx_by_w[w]) for x in ns))
    if core or alll or txw:
        index.append({'concept':syns[0],'syns':syns,'core':core,'all':alll,'txw':txw})

weeks = [{'week':w,'title':WEEK_TITLE[w],'notes':notes_path(w),'hasNotes':w in HAS_NOTES} for w in range(1,8)]

DATA = {
 'course':{'name':'시큐어코딩','prof':'이동재','author':'이재아'},
 'exam':{'name':'중간고사','date':'2026-10-22','weekday':'목','time':'19:00~20:00','format':'온라인 LMS 퀴즈','ai':'가능(오픈북)','range':'1~7주차'},
 'weeks':weeks,'quizzes':quizzes,'slides':slides,'tx':tx,'notes':notes,'index':index,'syn':SYN,
}
counts = {'quizzes':len(quizzes),'slides':len(slides),'tx':len(tx),'notes':len(notes),'index':len(index)}
print('파싱:', counts)
# 짝 안 맞은 퀴즈 보고
print('퀴즈 문제', sum(1 for q in quizzes if q['n']), '개 / 비고', sum(1 for q in quizzes if not q['n']), '개 / 정답 없는 문제', [f"{q['week']}-{q['chasi']}-{q['n']}" for q in quizzes if q['n'] and not q['a']])

# ---------- HTML 조립 ----------
tpl = read(f'{KIT}/template/exam.tpl.html')
head = tpl[:tpl.index('</head>')+len('</head>')]
theme = ''.join(l for l in open(THEME, encoding='utf-8') if not l.lstrip().startswith('/*'))
head = head.replace('/*THEME*/', theme.strip())
# 추가 스타일(코드블록·배너·찾아보기)
EXTRA_CSS = r'''<style>
.rmeta.note{background:rgba(224,138,0,.16);color:#9a5c00}
.rmeta.idx{background:rgba(var(--primary-rgb),.14);color:var(--primary)}
.body .codewrap{margin:14px 0;border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.body .codewrap .clab{font-size:12.5px;font-weight:800;padding:5px 12px;color:#fff;display:flex;justify-content:space-between;gap:10px}
.body .codewrap.vuln .clab{background:#c0392b}.body .codewrap.safe .clab{background:#1d7a6e}.body .codewrap.plain .clab{background:#51607a}
.body pre{margin:0;background:#0e1726;color:#e9eef7;padding:14px 16px;overflow-x:auto;font-size:15px;line-height:1.62;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.body pre code{font-family:inherit;white-space:pre;background:none;padding:0;color:inherit}
.body code{background:var(--surface-2);padding:1px 5px;border-radius:5px;font-size:.92em;font-family:ui-monospace,Menlo,Consolas,monospace}
.body ol{padding-left:24px;margin:8px 0}.body ol li{margin:6px 0}
.qopts{margin:8px 0 2px}.qopts div{padding:2px 0;font-size:16px}
.idxbox{margin:6px 0}.idxbox .lab{font-size:13px;font-weight:800;color:var(--ink-3);margin:10px 0 4px}
.idxloc{display:inline-block;margin:3px 6px 3px 0;padding:4px 11px;border-radius:999px;font-size:14px;font-weight:700;background:rgba(var(--primary-rgb),.12);color:var(--primary-dark);cursor:pointer}
.idxloc.dim{background:var(--surface-2);color:var(--ink-3);font-weight:500;opacity:.8}
.synnote{font-size:13.5px;color:var(--ink-2);padding:6px 14px;background:rgba(var(--accent-rgb),.1);border-radius:10px;margin:0 0 8px}
.qsrc{font-size:13.5px;color:var(--ink-3);margin:10px 0 0}
.howto{margin-top:46px;padding:26px 28px;background:var(--surface);border:1.5px solid var(--line);border-radius:24px;box-shadow:var(--shadow-soft)}
.howto .stitle{margin:0 0 12px}
.steps{padding-left:24px;margin:0 0 18px;font-size:17px;line-height:1.75;color:var(--ink)}.steps li{margin:6px 0}
.steps code,.plat code{background:var(--surface-2);padding:1px 6px;border-radius:6px;font-size:.92em}
.plat{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-bottom:16px}
.pc{padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:var(--surface-2)}
.pt{font-weight:800;font-size:16px;margin-bottom:6px;color:var(--primary-dark)}.pb{font-size:15.5px;line-height:1.7;color:var(--ink-2)}
.fb{padding:14px 16px;border-radius:14px;background:rgba(224,138,0,.12);border:1px solid rgba(224,138,0,.35)}.fb .pt{color:#9a5c00}
.fbq{display:inline-block;margin:4px 8px 6px 0;padding:8px 14px;border-radius:999px;border:1px solid rgba(224,138,0,.5);background:#fff;font:inherit;font-size:15px;font-weight:700;color:#7a4800;cursor:pointer}
.fbq:hover{background:rgba(224,138,0,.18)}
.lg{margin-top:14px}.gt{font-size:14.5px;font-weight:800;opacity:.9;margin:0 0 8px 2px;letter-spacing:.2px}
.lgrid.wk{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.lf .s{font-size:13.5px}.lf .r{font-size:13px}
.gradeB{font-size:12px;font-weight:800;padding:2px 8px;border-radius:6px;background:var(--accent-soft);color:var(--accent-dark);margin-left:6px}
</style>'''
head = head.replace('</head>', EXTRA_CSS + '\n</head>')

def jss(o): return json.dumps(o, ensure_ascii=False, separators=(',',':')).replace('</','<\\/')
FILE_LIST = ['00-PROMPT.md','01-RESUME.md','EXAM-LOG.md','0-INDEX.md','1-QUESTIONS.md','4-NOTES.md','2-SLIDES.md','3-TRANSCRIPT.md'] + [f'week0{w}.md' for w in range(1,8)]
FILES = {f: read(f'{HERE}/{f}') for f in FILE_LIST if os.path.exists(f'{HERE}/{f}')}
missing = [f for f in FILE_LIST if f not in FILES]
if missing: print('경고: 없는 파일(페이지에 포함 안 됨):', missing)

BODY_JS = r'''<body>
<div class="page">
  <div class="header">
    <div class="badge" id="hbadge"></div><h1 id="htitle"></h1>
    <div class="subtitle" id="hsub"></div><div class="meta" id="hmeta"></div>
  </div>
  <div class="search-section" id="ss">
    <div class="search-box" id="sbox"><span class="icon">🔍</span>
      <input type="text" id="q" placeholder="검색" autocomplete="off" aria-label="검색">
      <span class="pos" id="pos"></span><button class="clr" id="clr" aria-label="지우기">×</button>
      <span class="kbd">Enter 다음 · Esc 닫기</span><button class="tocbtn" id="tocBtn">☰ 목차</button>
    </div>
    <div class="filters" id="filters"></div>
    <div class="results" id="results" role="listbox"></div>
  </div>
  <div class="priority">
    <button class="pa" id="goQ"><span class="e">🎯</span><span class="tx"><span class="t">교안 퀴즈 모음</span><span class="s">각 차시 퀴즈와 정답</span></span><span class="b" id="qcnt"></span></button>
    <button class="pa blue" id="goIdx"><span class="e">🔎</span><span class="tx"><span class="t">찾아보기 (0-INDEX)</span><span class="s">개념 → 주차·위치</span></span><span class="b" id="icnt"></span></button>
  </div>
  <h2 class="stitle">📖 주차별 교안 <span class="cnt" id="wrange"></span></h2>
  <div class="wgrid" id="wgrid"></div>
  <h2 class="stitle" id="qsec">🎯 교안 퀴즈 <span class="cnt" id="qsecCnt"></span></h2>
  <div class="qfilter" id="qfilter"></div>
  <div class="qwrap" id="qwrap"></div>
  <h2 class="stitle">📅 시험 정보</h2>
  <div class="exam"><div class="ic">📝</div><div>
    <h3 id="ename"></h3><div class="sched" id="sched"></div>
    <div class="note">⚠️ 교안과 사실이 다르면 <b>교안 기준</b>으로 답합니다. 강의 발화는 자동 음성 인식이라 오인식이 있을 수 있습니다. 숫자·정답은 2-SLIDES·1-QUESTIONS로 대조하세요.</div>
  </div></div>
  <div class="howto">
    <h2 class="stitle">🧭 시험 중 순서</h2>
    <ol class="steps">
      <li><b>세션 열기</b> — <code>00-PROMPT.md</code> 내용을 <b>첫 메시지 본문에 붙여 넣는다</b>(파일 첨부만 하면 규칙을 잘 안 지킴). AI가 "준비됨"이라고 답하면 시작. 프로젝트 지침·사용자 지침 칸이 있는 플랫폼이면 거기에도 넣는다.</li>
      <li><b>자료 첨부</b> — 핵심 4개(<code>0-INDEX</code>·<code>1-QUESTIONS</code>·<code>4-NOTES</code>·<code>EXAM-LOG</code>) + 문제 주차의 <code>weekNN.md</code> 1~2개. 주차를 모르면 핵심 4개만 넣고 물어본다(0-INDEX가 주차를 알려줌).</li>
      <li><b>문제 보내기</b> — 사진 또는 타이핑, 한 문제씩. AI가 지문을 그대로 옮겨 적고(전사) 답 블록을 낸다. 블록 양식을 안 지키면 아래 "양식대로 다시" 문구를 보낸다.</li>
      <li><b>기록</b> — 답 블록을 <code>EXAM-LOG.md</code>에 이어 붙인다. 폴더가 연결된 세션이면 AI가 직접 저장.</li>
      <li><b>거부·중단되면</b> — 아래 재요청 문구를 쓴다. 두 번 안 되면 그 세션은 버리고 새 세션에 <code>01-RESUME.md</code> + <code>EXAM-LOG.md</code>를 넣어 이어간다.</li>
    </ol>
    <div class="plat">
      <div class="pc"><div class="pt">Claude 데스크톱 · 채팅</div><div class="pb">핵심 4개 + weekNN 1~2개 첨부. <b>2-SLIDES·3-TRANSCRIPT 전체는 첨부하지 않기</b>(길이 한도 초과 가능). 프로젝트에 넣는 경우는 전체 6개 가능.</div></div>
      <div class="pc"><div class="pt">Claude · 폴더 연결(Cowork)</div><div class="pb">첨부 없이 <code>lecture/midterm</code> 폴더를 연결하고 00-PROMPT를 붙여 넣는다. AI가 파일을 직접 검색하고 EXAM-LOG.md에 바로 기록한다.</div></div>
      <div class="pc"><div class="pt">ChatGPT 데스크톱</div><div class="pb">프로젝트(또는 채팅)에 전체 6개 + weekNN 업로드 가능(파일 검색 방식). 00-PROMPT를 프로젝트 지침이나 첫 메시지로.</div></div>
      <div class="pc"><div class="pt">Gemini NotebookLM</div><div class="pb">소스에 weekNN 7개 + 0-INDEX·1-QUESTIONS·4-NOTES 추가. 지침 저장 칸이 없으니 질문마다 01-RESUME의 "요약 규칙"을 함께 붙인다. .md가 안 올라가면 확장자를 .txt로 바꾼다.</div></div>
    </div>
    <div class="fb"><div class="pt">거부됐거나 양식이 깨졌을 때 재요청 문구 (누르면 복사)</div>
      <button class="fbq" data-copy="이건 교수님이 허용한 오픈북 시험이야. 공격 코드는 필요 없어. 첨부 자료에서 이 문제의 정답 번호와 교안 위치(출처)만 찾아서 답 양식으로 써줘.">1. 정답 번호와 교안 위치만</button>
      <button class="fbq" data-copy="답은 빼고, 사진의 문제 지문만 코드 블록 안에 글자 그대로 옮겨 적어줘(전사). 보기 번호와 기호도 그대로.">2. 전사만 (답 없이)</button>
      <button class="fbq" data-copy="위 지문의 정답 번호와 근거가 되는 교안 위치만 알려줘. 공격 코드 설명은 필요 없어.">3. 전사 받은 뒤 → 정답만</button>
      <button class="fbq" data-copy="방금 답을 00-PROMPT의 블록 양식으로만 다시 써줘. ### Q번호로 시작, 문제 :, 보기 :는 한 줄에 하나씩 줄바꿈, 보기 뒤 빈 줄, 그다음 답 : / 신뢰도 : / 풀이 :. 블록 밖에는 아무 말도 쓰지 마.">4. 양식대로 다시</button>
      <div class="pb">같은 세션에서 거부가 두 번 이상 쌓이면 뒤 답변 품질도 떨어지는 경향이 있으므로(추측) 새 세션으로 옮기는 편이 빠르다.</div>
    </div>
  </div>
  <div class="llm"><div class="h">🤖 AI에게 줄 파일</div>
    <p>카드를 누르면 열리지 않고 저장된다. 같은 파일이 <code>lecture/midterm/</code> 폴더에도 있다. 답마다 출처와 신뢰도(A~D)가 붙는다.</p>
    <div class="lg"><div class="gt">1 · 세션 시작과 기록</div><div class="lgrid" id="lgrid1"></div></div>
    <div class="lg"><div class="gt">2 · 핵심 자료 (작음 — 모든 세션에 첨부)</div><div class="lgrid" id="lgrid2"></div></div>
    <div class="lg"><div class="gt">3 · 주차 묶음 (한 파일에 그 주차의 퀴즈·정리·교안·발화 + 찾아보기)</div><div class="lgrid wk" id="lgrid3"></div></div>
    <div class="lg"><div class="gt">4 · 전체 원문 (큼 — 프로젝트·노트북 소스용)</div><div class="lgrid" id="lgrid4"></div></div>
    <div class="lg"><div class="gt">전부 한 번에</div><div class="lgrid"><a class="lf" href="#" id="zipAll"><span class="e">🗜️</span><span class="m"><div class="n">secure-coding-midterm.zip</div><div class="s">위 파일 전부 (ZIP)</div></span><span class="r" id="zipSize"></span></a></div></div>
  </div>
  <footer><div id="foot"></div></footer>
</div>
<nav class="toc" id="toc"></nav>
<section class="reader" id="reader">
  <div class="rbar">
    <button class="rbtn" id="prevR">◀ 이전</button><button class="rbtn" id="nextR">다음 ▶</button><button class="rbtn" id="listR">결과 목록</button>
    <span class="hits" id="hitnav"></span>
    <button class="rbtn" onclick="copyBody()">본문 복사 (AI용)</button>
    <span id="rlinks"></span><button class="rbtn x" id="closeR">✕ 닫기</button>
  </div>
  <div class="rscroll" id="rscroll"><div class="rin" id="rin"></div></div>
</section>
<div class="toast" id="toast"></div>
<script id="data" type="application/json">/*DATA*/</script>
<script id="files" type="application/json">/*FILES*/</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pad=n=>String(n).padStart(2,'0');
const RANGE='1~7주차';
const TYPES=[['q','교안 퀴즈'],['slide','교안'],['note','정리·함정'],['idx','찾아보기'],['tx','강의 발화']];
const TNAME=Object.fromEntries(TYPES);
const W_TYPE={q:6,slide:1,note:3,idx:5,tx:0};
const LIMIT={q:20,slide:12,note:10,idx:10,tx:8};

const items=[];
D.quizzes.forEach((q,i)=>items.push({type:'q',week:q.week,chasi:q.chasi,title:q.q,text:q.opts.join(' ')+' '+q.a+' '+q.detail,key:q.kw,sub:(q.n?'퀴즈 '+q.n+' · ':'')+'p.'+q.page,ref:q,qi:i}));
D.slides.forEach((s,i)=>items.push({type:'slide',week:s.week,chasi:s.chasi,title:'교안 p.'+s.page+(s.title?' · '+s.title:''),text:s.body,key:s.kw,sub:'',ref:s,si:i}));
D.notes.forEach((n,i)=>items.push({type:'note',week:n.week,chasi:n.chasi,title:n.title,text:n.body,key:n.kw,sub:'신뢰도 '+n.grade,ref:n,ni:i}));
D.index.forEach((x,i)=>items.push({type:'idx',week:0,chasi:0,title:x.concept,text:x.syns.join(' '),key:x.syns.join(' '),sub:x.syns.slice(1,4).join(', '),ref:x,ii:i}));
D.tx.forEach((t,i)=>items.push({type:'tx',week:t.week,chasi:t.chasi,title:t.text,text:'',key:'',sub:t.t,ref:t,ti:i}));

function termRe(t){const ch=[...t.replace(/\s+/g,'')].map(c=>c.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));return new RegExp(ch.join('\\s*'),'gi');}
function synExpand(q){const nq=q.replace(/\s+/g,'').toLowerCase();let hit=[];for(const g of D.syn){if(g.some(s=>{const ns=s.replace(/\s+/g,'').toLowerCase();return ns===nq||ns.includes(nq)&&nq.length>=2||nq.includes(ns)&&ns.length>=2;})){hit=hit.concat(g);}}return [...new Set(hit)];}
let state={q:'',type:'all',weeks:new Set(),chasis:new Set(),list:[],at:-1,expanded:{},syn:[]};

function run(res1,orMode){const res=[];for(const it of items){
  if(state.type!=='all'&&it.type!==state.type)continue;
  if(state.weeks.size&&it.type!=='idx'&&!state.weeks.has(it.week))continue;
  if(state.chasis.size&&it.type!=='idx'&&!state.chasis.has(it.chasi))continue;
  if(!res1.length){res.push({it,score:0});continue;}
  let score=0,ok=orMode?false:true,any=false;
  for(const re of res1){re.lastIndex=0;const inT=re.test(it.title);re.lastIndex=0;const inK=it.key?re.test(it.key):false;re.lastIndex=0;const cnt=(it.text.match(re)||[]).length;
    const m=inT||inK||cnt;if(m)any=true;if(!orMode&&!m){ok=false;break;}
    score+=(inT?20:0)+(inK?8:0)+Math.min(cnt,6);}
  if(orMode)ok=any;
  if(ok)res.push({it,score:score+W_TYPE[it.type]});}
  if(res1.length)res.sort((a,b)=>b.score-a.score);return res;}
function search(){const q=state.q.trim();state.syn=[];if(!q)return{res1:[],res:run([])};
  const syn=synExpand(q);
  if(syn.length>1){state.syn=syn;const res1=syn.map(termRe);return{res1,res:run(res1,true)};}
  const words=q.split(/\s+/).filter(Boolean);let res1=[termRe(q)],res=run(res1);
  if(!res.length&&words.length>1){res1=words.map(termRe);res=run(res1);}return{res1,res};}
function hl(text,res1,max){let s=String(text);if(max&&s.length>max){let pos=-1;for(const re of res1){re.lastIndex=0;const m=re.exec(s);if(m&&(pos<0||m.index<pos))pos=m.index;}const st=Math.max(0,(pos<0?0:pos)-Math.floor(max/3));s=(st>0?'… ':'')+s.slice(st,st+max)+(st+max<s.length?' …':'');}
  let h=esc(s);for(const re of res1){const r2=new RegExp(re.source.split('\\s*').map(c=>esc(c.replace(/\\(.)/g,'$1')).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('\\s*'),'gi');h=h.replace(r2,m=>'<mark class="h">'+m+'</mark>');}return h;}

function showResults(){const R=$('#results');const active=state.q.trim()||state.type!=='all'||state.weeks.size||state.chasis.size;
  state.list=[];state.at=-1;if(!active){R.classList.remove('active');R.innerHTML='';showPos();return;}
  const{res1,res}=search();
  let syn=state.syn.length?`<div class="synnote">동의어 포함: ${esc(state.syn.join(', '))}</div>`:'';
  if(!res.length){R.innerHTML=syn+`<div class="none">“${esc(state.q)}”에 대한 결과가 없습니다 🤔<br>단어를 줄이거나 다른 표현으로 찾아보세요.</div>`;R.classList.add('active');showPos();return;}
  const groups={};res.forEach(r=>(groups[r.it.type]=groups[r.it.type]||[]).push(r.it));
  let shown=0;for(const[ty]of TYPES){const g=groups[ty];if(g)shown+=Math.min(g.length,(state.type!=='all'||state.expanded[ty])?500:LIMIT[ty]);}
  let h=syn+`<div class="rcount"><span>총 <b>${res.length}</b>개${shown<res.length?` · 목록 ${shown}개`:''}</span><span>Enter 다음 · Shift+Enter 이전 · ↑↓ 선택</span></div>`;
  for(const[ty]of TYPES){const g=groups[ty];if(!g)continue;const lim=(state.type!=='all'||state.expanded[ty])?500:LIMIT[ty];
    h+=`<div class="rgrp">${TNAME[ty]} · ${g.length}</div>`;g.slice(0,lim).forEach(it=>h+=ritem(it,res1));
    if(g.length>lim)h+=`<button class="more" data-more="${ty}">${TNAME[ty]} ${g.length-lim}개 더 보기</button>`;}
  R.innerHTML=h;R.classList.add('active');R.scrollTop=0;showPos();}
function ritem(it,res1){const i=state.list.push(it)-1;
  const loc=it.type==='idx'?'전 범위':(it.week+'주차 '+it.chasi+'차시');
  const meta=`<span class="rmeta ${it.type}">${loc} · ${TNAME[it.type]}${it.type==='tx'?' '+esc(it.ref.t):''}</span>`;
  if(it.type==='q')return `<div class="ritem" data-i="${i}"><div class="r1"><span class="rkw">${hl(it.title,res1)}</span>${meta}</div>${it.ref.a?`<div class="rans"><b>답</b>${hl(it.ref.a,res1)}</div>`:''}</div>`;
  if(it.type==='tx')return `<div class="ritem" data-i="${i}"><div class="r1"><span class="rsum" style="margin:0;flex:1">${hl(it.title,res1)}</span>${meta}</div></div>`;
  const sub=it.sub?`<div class="rsub">${esc(it.sub)}</div>`:'';const snip=it.text?`<div class="rsum">${hl(it.text,res1,res1.length?150:100)}</div>`:'';
  return `<div class="ritem" data-i="${i}"><div class="r1"><span class="rkw">${hl(it.title,res1)}</span>${meta}</div>${sub}${snip}</div>`;}
function mark(i){const els=[...document.querySelectorAll('#results .ritem')];els.forEach((el,j)=>el.classList.toggle('sel',j===i));const el=els[i];if(!el)return;const R=$('#results'),r=el.getBoundingClientRect(),c=R.getBoundingClientRect();if(r.bottom>c.bottom)R.scrollTop+=r.bottom-c.bottom+8;else if(r.top<c.top)R.scrollTop-=c.top-r.top+8;}
function showPos(){const n=state.list.length;$('#pos').textContent=n?(state.at>=0?`${state.at+1} / ${n}`:`${n}개`):'';}
function go(i){const n=state.list.length;if(!n)return;state.at=(i+n)%n;showPos();mark(state.at);openItem(state.list[state.at]);}

/* 마크다운 렌더 (코드블록·표·목록·인용·굵게·인라인코드) */
function mdRender(t,title){const lines=t.split('\n');let out='',i=0,tb=[],ul=[],ol=[];let lastText=(title||'');
  const inl=s=>esc(s).replace(/`([^`]+)`/g,(m,x)=>'<code>'+x+'</code>').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
  const flushT=()=>{if(!tb.length)return;const rows=tb.filter(r=>!/^\|\s*:?-{2,}/.test(r)).map(r=>r.replace(/^\||\|$/g,'').split('|'));out+='<div class="tablewrap"><table>'+rows.map((r,k)=>'<tr>'+r.map(c=>`<${k?'td':'th'}>${inl(c.trim())}</${k?'td':'th'}>`).join('')+'</tr>').join('')+'</table></div>';tb=[];};
  const flushU=()=>{if(ul.length){out+='<ul>'+ul.map(x=>`<li>${inl(x)}</li>`).join('')+'</ul>';ul=[];}};
  const flushO=()=>{if(ol.length){out+='<ol>'+ol.map(x=>`<li>${inl(x)}</li>`).join('')+'</ol>';ol=[];}};
  const flush=()=>{flushT();flushU();flushO();};
  while(i<lines.length){const l=lines[i];
    if(/^```/.test(l.trim())){flush();const lang=l.trim().slice(3).trim();const code=[];i++;
      while(i<lines.length&&!/^```/.test(lines[i].trim())){code.push(lines[i]);i++;}i++;
      const ctx=(lastText+' '+(code[0]||'')).toLowerCase();
      let cls='plain',lab=lang||'code';
      if(/안전하지\s*않|취약한?\s*코드|#fail|vulnerable/.test(ctx)){cls='vuln';lab=(lang||'code')+' · 취약 코드';}
      else if(/안전한?\s*코드|safe\s*code/.test(ctx)){cls='safe';lab=(lang||'code')+' · 안전 코드';}
      out+=`<div class="codewrap ${cls}"><div class="clab"><span>${esc(lab)}</span></div><pre><code>${esc(code.join('\n'))}</code></pre></div>`;i++? i--:0;continue;}
    if(l.trim().startsWith('|')){flushU();flushO();tb.push(l.trim());i++;continue;}
    if(/^\s*[-*]\s+/.test(l)){flushT();flushO();ul.push(l.replace(/^\s*[-*]\s+/,''));lastText=l;i++;continue;}
    if(/^\s*\d+\.\s+/.test(l)){flushT();flushU();ol.push(l.replace(/^\s*\d+\.\s+/,''));lastText=l;i++;continue;}
    flush();
    if(!l.trim()){i++;continue;}
    if(/^#{1,6}\s/.test(l)){out+=`<h3>${inl(l.replace(/^#{1,6}\s/,''))}</h3>`;lastText=l;}
    else if(/^>\s?/.test(l)){out+=`<p style="border-left:3px solid var(--line);padding-left:10px;color:var(--ink-2)">${inl(l.replace(/^>\s?/,''))}</p>`;lastText=l;}
    else{out+=`<p>${inl(l)}</p>`;lastText=l;}
    i++;}
  flush();return out;}

let hits=[],hitAt=0;
function pin(){const y=$('#ss').getBoundingClientRect().top;if(y>20)window.scrollBy(0,y-14);}
function setTop(){const b=$('#sbox').getBoundingClientRect();document.documentElement.style.setProperty('--rtop',Math.max(70,b.bottom+$('#filters').offsetHeight+20)+'px');}
function head(crumbs,title,sub){return `<div class="dh"><div class="crumb">${crumbs.map(c=>'<span>'+esc(c)+'</span>').join('')}</div><h2>${title}</h2>${sub?`<div class="bd">${esc(sub)}</div>`:''}</div>`;}
function linkBtns(it){let h='';const r=it.ref;if(r.notes)h+=`<a class="rbtn" href="${r.notes}" target="_blank">${it.week}주차 정리 ↗</a>`;if(r.pdf)h+=`<a class="rbtn" href="${r.pdf}" target="_blank">교안 PDF ↗</a>`;return h;}
function openItem(it){const{res1}=search();let h='',links='';
  if(it.type==='q'){const q=it.ref;const opts=q.opts.length?`<div class="qopts">${q.opts.map(o=>`<div>${inlB(o)}</div>`).join('')}</div>`:'';
    h=head([`${q.week}주차 ${q.chasi}차시`,'교안 퀴즈'],esc(q.q),(q.n?'퀴즈 '+q.n+' · ':'')+'p.'+q.page)+`<div class="body">${opts}${q.n?`<div class="call warn"><div class="t">답</div><p>${esc(q.a||'(정답 표기 확인)')}</p>${q.detail?`<p>${esc(q.detail)}</p>`:''}</div>`:''}${q.n?'':`<p>${esc(q.detail)}</p>`}${q.src?`<p class="qsrc">출처: ${esc(q.src)}</p>`:''}</div>`;links=linkBtns(it);}
  else if(it.type==='slide'){const s=it.ref;h=head([`${s.week}주차 ${s.chasi}차시`,'교안 원문'],'교안 p.'+s.page+(s.title?' · '+esc(s.title):''),'')+`<div class="body">${mdRender(s.body,s.title)}</div>`;links=linkBtns(it);}
  else if(it.type==='note'){const n=it.ref;h=head([`${n.week?n.week+'주차 '+n.chasi+'차시':'공통'}`,'정리·함정'],esc(n.title)+`<span class="gradeB">신뢰도 ${n.grade}</span>`,'')+`<div class="body">${mdRender(n.body,n.title)}</div>`;links=linkBtns(it);}
  else if(it.type==='tx'){const all=D.tx.filter(x=>x.week===it.week&&x.chasi===it.chasi),k=all.indexOf(it.ref);
    h=head([`${it.week}주차 ${it.chasi}차시`,'강의 발화'],`${it.ref.t} 부근`,'자동 음성 인식 — 오인식 가능')+`<div class="body">${all.slice(Math.max(0,k-8),k+9).map(x=>`<div class="txl${x===it.ref?' cur':''}"><span class="tm">${x.t}</span>${esc(x.text)}</div>`).join('')}</div>`;links=linkBtns(it);}
  else if(it.type==='idx'){const x=it.ref;const loc=(arr,dim)=>arr.map(([w,c])=>`<span class="idxloc${dim?' dim':''}" data-wc="${w}-${c}">${w}-${c}</span>`).join('');
    h=head(['전 범위','찾아보기'],esc(x.concept),'')+`<div class="body"><div class="idxbox"><div class="lab">검색 표기</div><p>${esc(x.syns.join(' · '))}</p>`
      +`<div class="lab">핵심 위치 (제목·퀴즈에 나온 차시)</div><div>${x.core.length?loc(x.core,false):'<span class="idxloc dim">없음</span>'}</div>`
      +`<div class="lab">그 밖에 언급된 차시</div><div>${loc(x.all.filter(a=>!x.core.some(c=>c[0]===a[0]&&c[1]===a[1])),true)||'<span class="idxloc dim">—</span>'}</div>`
      +(x.txw.length?`<div class="lab">강의 발화에 나온 주차</div><p>${x.txw.join(', ')}주차</p>`:'')+`</div></div>`;}
  $('#rin').innerHTML=h;$('#rlinks').innerHTML=links;
  const many=state.list.length>1&&state.at>=0;$('#prevR').style.display=$('#nextR').style.display=many?'':'none';$('#listR').style.display=state.list.length?'':'none';
  pin();setTop();document.body.classList.add('reading');document.body.classList.remove('toc-on');$('#results').classList.remove('active');$('#rscroll').scrollTop=0;
  markHits($('#rin'),res1);}
function inlB(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');}
function closeReader(){document.body.classList.remove('reading');}
function markHits(root,res1){hits=[];hitAt=0;$('#hitnav').innerHTML='';if(!res1.length)return;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>(n.parentNode.closest('.dh'))?NodeFilter.FILTER_REJECT:(n.parentNode.closest('.body,.lq'))?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_REJECT});
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  for(const n of nodes){const txt=n.nodeValue,rg=[];for(const re of res1){re.lastIndex=0;let m;while((m=re.exec(txt))){if(!m[0].length){re.lastIndex++;continue;}rg.push([m.index,m.index+m[0].length]);}}if(!rg.length)continue;rg.sort((a,b)=>a[0]-b[0]);
    const f=document.createDocumentFragment();let last=0;for(const[a,b]of rg){if(a<last)continue;f.append(txt.slice(last,a));const mk=document.createElement('mark');mk.className='h';mk.textContent=txt.slice(a,b);f.append(mk);hits.push(mk);last=b;}f.append(txt.slice(last));n.replaceWith(f);}
  if(hits.length){$('#hitnav').innerHTML=`<span>본문 ${hits.length}곳</span><button class="rbtn" onclick="jump(-1)">▲</button><button class="rbtn" onclick="jump(1)">▼</button>`;jump(0);}}
function jump(d){if(!hits.length)return;hits[hitAt]&&hits[hitAt].classList.remove('now');hitAt=(hitAt+d+hits.length)%hits.length;hits[hitAt].classList.add('now');hits[hitAt].scrollIntoView({block:'center'});}
function copyBody(){const crumb=$('#rin .crumb')?$('#rin .crumb').innerText.replace(/\s*›\s*/g,' '):'';const t=$('#rin h2')?$('#rin h2').innerText:'';const b=[...$('#rin').querySelectorAll('.body,.lq')].map(x=>x.innerText).join('\n\n');navigator.clipboard.writeText('['+crumb+'] '+t+'\n\n'+b).then(()=>toast('복사했습니다 — AI에 붙여넣으세요'),()=>toast('복사 실패'));}
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('on');setTimeout(()=>t.classList.remove('on'),1600);}

function renderFilters(){const t0=state.type;state.type='all';const{res}=search();state.type=t0;const cnt={};res.forEach(r=>cnt[r.it.type]=(cnt[r.it.type]||0)+1);const has=!!state.q.trim();
  let h=`<button class="chip${state.type==='all'?' on':''}" data-type="all">전체${has?`<span class="c">${res.length}</span>`:''}</button>`;
  TYPES.forEach(([k,n])=>h+=`<button class="chip${state.type===k?' on':''}" data-type="${k}">${n}${has?`<span class="c">${cnt[k]||0}</span>`:''}</button>`);
  h+='<span class="fsep"></span>';for(let w=1;w<=7;w++)h+=`<button class="chip wk${state.weeks.has(w)?' on':''}" data-week="${w}">${w}주</button>`;
  h+='<span class="fsep"></span>';for(let c=1;c<=3;c++)h+=`<button class="chip wk${state.chasis.has(c)?' on':''}" data-chasi="${c}">${c}차시</button>`;
  $('#filters').innerHTML=h;}
function refresh(){state.expanded={};renderFilters();showResults();}

function renderPage(){const C=D.course,E=D.exam;document.title=`${C.name} ${E.name} 검색`;
  $('#hbadge').textContent=`${C.prof} 교수님 · ${C.name}`;$('#htitle').textContent=`${E.name} 검색`;$('#ename').textContent=`${C.name} ${E.name}`;
  $('#hsub').textContent=`📚 ${RANGE} · 교안 퀴즈 · 교안 원문 · 강의 발화 · 정리`;$('#wrange').textContent=RANGE;
  $('#foot').textContent=`${C.name} · ${E.name} 검색 · 정리: ${C.author}`;
  $('#hmeta').textContent=`${E.date.slice(5).replace('-','/')}(${E.weekday}) ${E.time} · ${E.format} · AI ${E.ai}`;
  $('#qcnt').textContent=D.quizzes.filter(q=>q.n).length+'개';$('#icnt').textContent=D.index.length+'개';
  $('#sched').innerHTML=[['일시',`${E.date.slice(5).replace('-','/')} (${E.weekday}) ${E.time}`],['방식',E.format],['범위',RANGE],['AI',E.ai]].map(([a,b])=>`<div><b>${a}</b><span>${b}</span></div>`).join('');
  $('#wgrid').innerHTML=D.weeks.map(w=>{const ss=D.slides.filter(s=>s.week===w.week);const byC={};ss.forEach(s=>{(byC[s.chasi]=byC[s.chasi]||[]).push(s);});
    const secs=[1,2,3].map(c=>`<li><button data-open="slide" data-w="${w.week}" data-c="${c}"><span class="no">${c}차시</span><span>${esc((byC[c]&&byC[c][0]&&byC[c][0].title)||'')} 외 ${byC[c]?byC[c].length:0}쪽</span></button></li>`).join('');
    return `<div class="wcard"><div class="wnum">${pad(w.week)}<small>주차</small></div><div class="wtitle">${esc(w.title)}</div><div class="wdate">3차시 · 교안+녹취</div>
      <ul class="wsecs">${secs}</ul><div class="wlinks">${w.hasNotes?`<a href="${w.notes}" target="_blank">📖 정리 페이지</a>`:''}<a class="pdf" href="../week${pad(w.week)}/" target="_blank">📑 교안 폴더</a></div></div>`;}).join('');
  $('#toc').innerHTML=D.weeks.map(w=>`<h4>${w.week}주차 · ${esc(w.title)}</h4>`+[1,2,3].map(c=>`<button data-open="slide" data-w="${w.week}" data-c="${c}"><span class="no">${c}차시</span>교안·발화</button>`).join('')).join('');
  const card=([n,e,sub,r])=>`<a class="lf" href="${n}" download><span class="e">${e}</span><span class="m"><div class="n">${n}</div><div class="s">${sub}</div></span><span class="r">${r}</span></a>`;
  const kb=n=>FILES[n]?Math.round(new Blob([FILES[n]]).size/1024)+' KB':'';
  $('#lgrid1').innerHTML=[['00-PROMPT.md','📋','첫 메시지 · 규칙과 답 양식','시작'],['01-RESUME.md','🔁','새 세션에서 이어가기','이어가기'],['EXAM-LOG.md','📝','문제·답 누적 기록','기록']].map(card).join('');
  $('#lgrid2').innerHTML=[['0-INDEX.md','🔎','개념 → 주차·위치',kb('0-INDEX.md')],['1-QUESTIONS.md','🎯','교안 퀴즈 63문제 · A',kb('1-QUESTIONS.md')],['4-NOTES.md','📚','오류·함정 23개 · C~D',kb('4-NOTES.md')]].map(card).join('');
  $('#lgrid3').innerHTML=D.weeks.map(w=>[`week0${w.week}.md`,'📦',`${w.week}주차 ${w.title}`,kb(`week0${w.week}.md`)]).map(card).join('');
  $('#lgrid4').innerHTML=[['2-SLIDES.md','📑','교안 원문 626쪽 · A',kb('2-SLIDES.md')],['3-TRANSCRIPT.md','🎙️','강의 발화 4,609줄 · B',kb('3-TRANSCRIPT.md')]].map(card).join('');
  $('#zipSize').textContent=Math.round(Object.values(FILES).reduce((a,t)=>a+new Blob([t]).size,0)/1024)+' KB';
  renderQ();}
let qWeek=0;
function renderQ(){const qs=D.quizzes.filter(q=>q.n&&(!qWeek||q.week===qWeek));$('#qsecCnt').textContent=qs.length+'개';
  $('#qfilter').innerHTML=[0,1,2,3,4,5,6,7].map(w=>`<button class="chip${qWeek===w?' on':''}" data-qw="${w}">${w?w+'주차':'전체'}</button>`).join('');
  $('#qwrap').innerHTML=qs.map(q=>`<div class="qcard"><div class="qmeta"><span class="k">${q.week}주차 ${q.chasi}차시</span><span>${q.n?'퀴즈 '+q.n+' · ':''}p.${q.page}</span></div>
    <div class="qq">${esc(q.q)}</div>${q.opts.length?`<div class="qopts">${q.opts.map(o=>`<div>${inlB(o)}</div>`).join('')}</div>`:''}<div class="qa"><b>답</b>${esc(q.a||'(정답 확인)')}</div>${q.detail?`<div class="qd">${esc(q.detail)}</div>`:''}
    <button class="qopen" data-open="qfind" data-w="${q.week}" data-c="${q.chasi}" data-n="${q.n}">본문에서 열기 →</button></div>`).join('');}

let tmr;
$('#q').addEventListener('input',e=>{state.q=e.target.value;$('#sbox').classList.toggle('has',!!state.q);closeReader();if(state.q)pin();clearTimeout(tmr);tmr=setTimeout(refresh,110);});
$('#q').addEventListener('focus',()=>{if(state.list.length&&!document.body.classList.contains('reading'))$('#results').classList.add('active');});
$('#clr').onclick=()=>{$('#q').value='';state.q='';$('#sbox').classList.remove('has');state.type='all';refresh();closeReader();$('#q').focus();};
$('#filters').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;if(b.dataset.type)state.type=b.dataset.type;if(b.dataset.week){const w=+b.dataset.week;state.weeks.has(w)?state.weeks.delete(w):state.weeks.add(w);}if(b.dataset.chasi){const c=+b.dataset.chasi;state.chasis.has(c)?state.chasis.delete(c):state.chasis.add(c);}closeReader();refresh();});
$('#results').addEventListener('click',e=>{const m=e.target.closest('.more');if(m){state.expanded[m.dataset.more]=true;showResults();return;}const it=e.target.closest('.ritem');if(it)go(+it.dataset.i);});
function openSlideWC(w,c){state.list=[];state.at=-1;showPos();const it=items.find(x=>x.type==='slide'&&x.week===w&&x.chasi===c);if(it)openItem(it);}
document.addEventListener('click',e=>{
  const o=e.target.closest('[data-open]');if(o){const w=+o.dataset.w,c=+o.dataset.c;
    if(o.dataset.open==='slide'){openSlideWC(w,c);}else if(o.dataset.open==='qfind'){state.list=[];state.at=-1;showPos();const it=items.find(x=>x.type==='q'&&x.week===w&&x.chasi===c&&x.ref.n==+o.dataset.n);if(it)openItem(it);}return;}
  const wc=e.target.closest('[data-wc]');if(wc){const[w,c]=wc.dataset.wc.split('-').map(Number);openSlideWC(w,c);return;}
  const qw=e.target.closest('[data-qw]');if(qw){qWeek=+qw.dataset.qw;renderQ();return;}
  if(!e.target.closest('.search-section')&&!e.target.closest('.reader'))$('#results').classList.remove('active');});
$('#goQ').onclick=()=>$('#qsec').scrollIntoView({behavior:'smooth',block:'start'});
$('#goIdx').onclick=()=>{state.type='idx';refresh();window.scrollTo({top:0,behavior:'smooth'});$('#q').focus();};
$('#tocBtn').onclick=()=>{pin();setTop();closeReader();document.body.classList.toggle('toc-on');};
$('#closeR').onclick=closeReader;$('#prevR').onclick=()=>go(state.at-1);$('#nextR').onclick=()=>go(state.at+1);
$('#listR').onclick=()=>{closeReader();$('#results').classList.add('active');$('#q').focus();};
document.addEventListener('keydown',e=>{const inQ=document.activeElement===$('#q');
  if((e.key==='/'&&!inQ)||((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k')){e.preventDefault();$('#q').focus();$('#q').select();return;}
  if(e.key==='Escape'){if(document.body.classList.contains('reading'))closeReader();else if(document.body.classList.contains('toc-on'))document.body.classList.remove('toc-on');else if(state.q)$('#clr').click();else $('#results').classList.remove('active');return;}
  if(!inQ)return;
  if(e.key==='Enter'){e.preventDefault();if(!state.list.length)return;go(state.at<0?0:state.at+(e.shiftKey?-1:1));}
  else if(e.key==='ArrowDown'&&$('#results').classList.contains('active')){e.preventDefault();state.at=Math.min(state.list.length-1,state.at+1);mark(state.at);showPos();}
  else if(e.key==='ArrowUp'&&$('#results').classList.contains('active')){e.preventDefault();state.at=Math.max(0,state.at-1);mark(state.at);showPos();}});
window.addEventListener('resize',setTop);window.addEventListener('scroll',setTop,{passive:true});
const FILES=JSON.parse(document.getElementById('files').textContent);
// ---- ZIP(압축 없이 저장만) 직접 생성: 외부 라이브러리 없이 전부 한 번에 내려받기 ----
const CRC_T=(()=>{const t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0;}return t;})();
function crc32(u8){let c=0xFFFFFFFF;for(let i=0;i<u8.length;i++)c=CRC_T[(c^u8[i])&0xFF]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
function makeZip(files){ // files: [[name, text]]
  const enc=new TextEncoder(),parts=[],cd=[];let off=0;
  const d=new Date(),dt=((d.getHours()<<11)|(d.getMinutes()<<5)|(d.getSeconds()>>1))&0xFFFF,dd=(((d.getFullYear()-1980)<<9)|((d.getMonth()+1)<<5)|d.getDate())&0xFFFF;
  const u16=v=>[v&255,(v>>8)&255],u32=v=>[v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255];
  for(const [name,text] of files){const nm=enc.encode(name),data=enc.encode(text),crc=crc32(data);
    const lh=new Uint8Array([...u32(0x04034b50),...u16(20),...u16(0x0800),...u16(0),...u16(dt),...u16(dd),...u32(crc),...u32(data.length),...u32(data.length),...u16(nm.length),...u16(0),...nm]);
    parts.push(lh,data);
    cd.push(new Uint8Array([...u32(0x02014b50),...u16(20),...u16(20),...u16(0x0800),...u16(0),...u16(dt),...u16(dd),...u32(crc),...u32(data.length),...u32(data.length),...u16(nm.length),...u16(0),...u16(0),...u16(0),...u16(0),...u32(0),...u32(off),...nm]));
    off+=lh.length+data.length;}
  const cdLen=cd.reduce((a,x)=>a+x.length,0);
  const eocd=new Uint8Array([...u32(0x06054b50),...u16(0),...u16(0),...u16(files.length),...u16(files.length),...u32(cdLen),...u32(off),...u16(0)]);
  return new Blob([...parts,...cd,eocd],{type:'application/zip'});}
function saveBlob(blob,name){const url=URL.createObjectURL(blob);const t=document.createElement('a');t.href=url;t.download=name;document.body.append(t);t.click();t.remove();setTimeout(()=>URL.revokeObjectURL(url),4000);}
$('#zipAll').addEventListener('click',e=>{e.preventDefault();saveBlob(makeZip(Object.entries(FILES)),'secure-coding-midterm.zip');toast('secure-coding-midterm.zip 저장');});
document.querySelectorAll('.fbq').forEach(b=>b.addEventListener('click',()=>navigator.clipboard.writeText(b.dataset.copy).then(()=>toast('복사했습니다 — AI에 붙여넣으세요'),()=>toast('복사 실패'))));
document.addEventListener('click',e=>{const a=e.target.closest('a.lf');if(!a)return;const name=a.getAttribute('href'),txt=FILES[name];if(txt==null)return;e.preventDefault();saveBlob(new Blob([txt],{type:'application/octet-stream'}),name);toast(name+' 저장');}); // 카드는 나중에 그려지므로 위임 방식
renderPage();refresh();setTop();
</script>
</body>
</html>'''

body = BODY_JS.replace('/*DATA*/', jss(DATA)).replace('/*FILES*/', jss(FILES))
html = head + '\n' + body
open(OUT, 'w', encoding='utf-8').write(html)
print('index.html', round(len(html.encode())/1024), 'KB')
