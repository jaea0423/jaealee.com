# 시험용 검색 마크다운 빌더
# 교안 md / 녹취 txt(기존 파일)을 읽어 출처별 파일로 합친다. 공격 문자열은 이 스크립트를 거쳐
# 출력 파일로만 흐르고, 사람이 읽는 응답에는 나오지 않는다.
import re, os, glob

U = '/mnt/user-data/uploads'
R = '/root/.claude/uploads/d2c4c9a7-3ca2-5b07-84a4-2be84f4df9d9'
OUT = '/home/claude/sc/exam'
os.makedirs(OUT, exist_ok=True)

# 주차·차시 → 교안 md 경로
SLIDES = {
    (1,1): f'{U}/securecoding_w1_1.md', (1,2): f'{U}/securecoding_w1_2.md', (1,3): f'{U}/securecoding_w1_3.md',
    (2,1): f'{U}/securecoding_w2_1.md', (2,2): f'{U}/securecoding_w2_2.md', (2,3): f'{U}/securecoding_w2_3.md',
    (3,1): f'{U}/securecoding_w3_1.md', (3,2): f'{U}/securecoding_w3_2.md', (3,3): f'{U}/securecoding_w3_3.md',
    (4,1): f'{R}/53ea7327-securecoding_w4_1.md', (4,2): f'{R}/51137ae2-securecoding_w4_2.md', (4,3): f'{R}/2b5cf389-securecoding_w4_3.md',
    (5,1): f'{R}/7d3bedd5-2025___________5___1___vF.md', (5,2): f'{R}/b601dd7a-2025___________5___2___vF.md', (5,3): f'{R}/95de2aad-2025___________5___3___vF.md',
    (6,1): f'{U}/secure-coding/lecture/week06/06-1-slides1.md', (6,2): f'{U}/secure-coding/lecture/week06/06-2-slides1.md', (6,3): f'{U}/secure-coding/lecture/week06/06-3-slides1.md',
    (7,1): f'{U}/secure-coding/lecture/week07/07-1-slides1.md', (7,2): f'{U}/secure-coding/lecture/week07/07-2-slides1.md', (7,3): f'{U}/secure-coding/lecture/week07/07-3-slides1.md',
}

# 주차별 주제(머리말용)
WEEK_TITLE = {
    1: '보안약점과 시큐어코딩 개요', 2: 'SW개발보안 방법론·위협 모델링',
    3: 'Spring Boot 개발 환경·실습', 4: '정규식과 입력값 검증·XSS 필터',
    5: '인증과 인가 · OAuth2 · JWT', 6: 'ORM·MyBatis / SQL 인젝션 / Command 인젝션',
    7: '프론트엔드 데이터 처리 / XSS / CSRF',
}

# 동의어 표: 대표어 → 검색에 쓰일 표기들(영문·한글·음성인식 표기). 공격 문자열 없음.
SYN = {
    '보안약점': ['보안약점', 'Weakness', 'CWE', '취약점', 'Vulnerability'],
    'SQL 인젝션': ['SQL Injection', 'SQL 인젝션', 'SQL 삽입', '에스큐엘 인젝션', '에스큐엘', 'SQLi', 'CWE-89'],
    'PreparedStatement': ['PreparedStatement', '프리페어드 스테이트먼트', '파라미터 바인딩', '바인딩', 'setString'],
    'XSS': ['XSS', 'Cross-Site Scripting', '크로스사이트 스크립팅', '크로스 사이트 스크립팅', '크로스사이트스크립팅', 'CWE-79'],
    'Reflected XSS': ['Reflected XSS', '반사형 XSS', '리플렉티드'],
    'Stored XSS': ['Stored XSS', '저장형 XSS', '스토어드'],
    'DOM XSS': ['DOM XSS', 'DOM 기반 XSS', '돔 기반', 'document.write', 'innerHTML'],
    'CSRF': ['CSRF', 'Cross-Site Request Forgery', '크로스사이트 요청 위조', '크로스 사이트 요청 위조', 'XSRF', 'CWE-352'],
    'Command 인젝션': ['Command Injection', '커맨드 인젝션', '명령어 삽입', '명령 삽입', 'OS Command', 'CWE-78'],
    'CSP': ['CSP', 'Content Security Policy', '콘텐츠 보안 정책', '컨텐츠 시큐리티 폴리시'],
    'SameSite': ['SameSite', '세임사이트', 'Strict', 'Lax', 'None'],
    'HTML 인코딩': ['HTML Encoding', 'HTML 인코딩', '이스케이프', 'Escape', '엔티티', 'Entity', 'escapeHtml', 'textContent'],
    '화이트리스트': ['화이트리스트', 'Whitelist', '최소 허용', '허용 목록'],
    'ORM': ['ORM', 'Object-Relational Mapping', '객체 관계 매핑', 'JPA', 'Hibernate', '하이버네이트'],
    'MyBatis': ['MyBatis', '마이바티스', 'Mapper', '매퍼', '#{}', '${}', '동적 SQL'],
    'Dirty Checking': ['Dirty Checking', '더티 체킹', '변경 감지'],
    'Mass Assignment': ['Mass Assignment', '대량 할당', 'DTO', 'isAdmin'],
    '인증': ['Authentication', '인증', '로그인'],
    '인가': ['Authorization', '인가', '권한', 'RBAC', 'ABAC', 'PBAC', '최소 권한'],
    '세션': ['Session', '세션', 'JSESSIONID', '세션 쿠키', '쿠키', 'HttpOnly', 'Secure'],
    '토큰': ['Token', '토큰', 'Bearer', '베어러'],
    'OAuth2': ['OAuth2', 'OAuth 2.0', '오아스', '권한 위임', 'Authorization Code', '인가 코드', 'PKCE', 'state'],
    'JWT': ['JWT', 'JSON Web Token', '제이더블유티', 'Claims', '클레임', 'HS256', 'RS256', 'Refresh Token', '리프레시 토큰'],
    'Refresh Token': ['Refresh Token', '리프레시 토큰', '토큰 회전', 'Rotation'],
    'MFA': ['MFA', 'Multi-Factor', '다중 인증', '다중 매체 인증', 'OTP', 'FIDO2', 'WebAuthn'],
    'HSTS': ['HSTS', 'HTTP Strict-Transport-Security', '스트릭트 트랜스포트'],
    'IDOR': ['IDOR', 'Insecure Direct Object References', '직접 객체 참조', '수평 권한', '수직 권한', '권한 상승'],
    '정규식': ['Regex', '정규식', 'Regular Expression', 'Pattern', 'Matcher', '정규 표현식'],
    'ReDoS': ['ReDoS', '레도스', '백트래킹', 'Backtracking'],
    'Filter': ['Filter', '필터', 'Interceptor', '인터셉터', 'Servlet', 'DispatcherServlet'],
    '위협 모델링': ['Threat Modeling', '위협 모델링', 'STRIDE', '스트라이드', 'DREAD', '드레드', 'MS-SDL', 'MTMT'],
    'SSR/CSR': ['SSR', 'CSR', 'Server-Side Rendering', 'Client-Side Rendering', '서버 사이드 렌더링', '클라이언트 사이드 렌더링'],
    '로컬 저장소': ['localStorage', 'sessionStorage', '로컬 저장소', '로컬 스토리지', 'Same-Origin'],
    'CORS': ['CORS', '코어스', 'Cross-Origin', '교차 출처'],
    'SQLMap': ['SQLMap', '에스큐엘맵'],
    'ZAP': ['ZAP', 'OWASP ZAP', 'Active Scan', 'Burp', '버프스위트', '버프 스위트'],
    '코드 리뷰': ['코드 리뷰', 'Code Review', 'SAST', 'DAST', '정적 분석', '동적 분석', 'SonarQube', 'Fortify'],
}

def strip_html(t):
    # <!-- ... --> 주석 구분자 제거, <br> 계열은 구분자로 바꿔 검색이 끊기지 않게 함.
    # <script>/<img>/<form> 등 코드 예시 태그는 실제 내용이라 그대로 둔다.
    # 변환기가 남긴 메모 주석("아래는 … 내용")은 쪽 제목으로 잡히지 않게 표준 메모 줄로 바꾼다.
    t = re.sub(r'<!--\s*아래는 슬라이드 이미지·도표에서 판독한 내용\s*-->', '(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)', t)
    t = re.sub(r'<!--\s*아래는 [^>]*?다시 옮긴 내용\s*-->', '(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)', t)
    t = t.replace('<!--', '').replace('-->', '')
    t = re.sub(r'<br\s*/?>', ' / ', t)
    return t

def read(path):
    return open(path, encoding='utf-8').read()

def deck_title(md):
    m = re.search(r'^#\s*(.+)$', md, re.M)
    return m.group(1).strip() if m else ''

def keywords_for(text):
    found = []
    low = text.lower()
    for rep, syns in SYN.items():
        if any(s.lower() in low for s in syns):
            found.append('/'.join(syns))
    return found

def pages(md):
    # (페이지번호, 본문) 리스트
    parts = re.split(r'<!--\s*p\.(\d+)\s*-->', md)
    out = []
    # parts[0]는 서문, 이후 (번호, 내용) 쌍
    for i in range(1, len(parts), 2):
        num = parts[i]; body = parts[i+1] if i+1 < len(parts) else ''
        out.append((num, body))
    return out

def first_heading(body):
    for ln in body.splitlines():
        s = ln.strip()
        if not s or s.startswith('(') or s.startswith('그림') or s.startswith('출처'):
            continue
        s = re.sub(r'^#+\s*', '', s).replace('**','').strip()
        if s and not s.startswith('<'):
            return s[:40]
    return ''

def tag_inner_headings(body, tag, w, c, num, title):
    # 본문 안의 소제목(#, ##, ###)에도 위치 태그를 붙인다("모든 제목 줄에 위치 표기" 규칙).
    # 쪽 제목과 같은 줄은 이미 ## 제목에 있으므로 지운다. 코드 블록 안의 #은 건드리지 않는다.
    out, in_code = [], False
    for ln in body.splitlines():
        if ln.strip().startswith('```'):
            in_code = not in_code; out.append(ln); continue
        m = re.match(r'^#{1,6}\s+(.*?)\s*$', ln)
        if in_code or not m:
            out.append(ln); continue
        text = m.group(1).replace('**', '').strip()
        if title and text[:40] == title:
            continue  # 쪽 제목과 중복
        out.append(f'### [{tag}] {w}주차 {c}차시 p.{num} · {text}')
    if in_code:
        out.append('```')   # 원본에 닫는 펜스가 빠진 쪽(5-2 p.25 등) → 닫아서 다음 쪽까지 코드로 번지지 않게 함
    return '\n'.join(out)

def is_quiz_page(body):
    # 짧은 줄이 '퀴즈'/'Quiz'로 시작하면 퀴즈(또는 정답) 쪽. 본문 중 언급("p.32 퀴즈에서는")은 제외.
    for ln in body.splitlines():
        s = re.sub(r'^[#>\-\*\s]+', '', ln).replace('**', '').strip()
        if re.match(r'^(퀴즈|퀴 즈|Quiz)\b', s, re.I) and len(s) <= 12:
            return s
    return None

NOTE_PAT = re.compile(r'^(※|\(※|\(정답 표시|\[정답 표시|-?\s*정답 보기|아래는 슬라이드|아래는 다단|\(변환 메모)')

def _lines(body):
    # 퀴즈 쪽 본문을 정규화: 굵게/목록 기호 제거, 빈 줄·구분선·'퀴즈' 표식 제거
    out = []
    for ln in strip_html(body).splitlines():
        s = ln.strip()
        if not s or s == '---':
            continue
        s = re.sub(r'^[#>]+\s*', '', s)
        s = re.sub(r'^-\s+', '', s)
        s = s.replace('**', '').strip()
        if re.match(r'^(퀴즈|퀴 즈|Quiz)\b', s, re.I) and len(s) <= 12:
            continue
        out.append(s)
    return out

def _blocks(lines):
    # 'N. ' 로 시작하는 줄을 경계로 문제 블록을 나눈다. 비고 줄(※ 등)은 따로 모은다.
    blocks, notes, cur = {}, [], None
    for s in lines:
        if NOTE_PAT.match(s):
            notes.append(s); continue
        m = re.match(r'^(\d{1,2})\.\s*(.*)$', s)
        if m:
            cur = int(m.group(1)); blocks[cur] = [m.group(2).strip()]
        elif cur is not None:
            blocks[cur].append(s)
        else:
            notes.append(s)
    return blocks, notes

OPT_SPLIT = re.compile(r'(?:^|\s|　)(?=\d\)\s*)')

def _split_opts(s):
    # "1) a　2) b　3) c" 한 줄 → ["1) a", "2) b", "3) c"]. 보기 번호가 2개 이상일 때만 나눈다.
    parts = [p.strip() for p in OPT_SPLIT.split(s) if p and p.strip()]
    return parts if len(parts) >= 2 and all(re.match(r'^\d\)', p) for p in parts) else None

HINT_PAT = re.compile(r'글자|영문|영어|소문자|대문자|숫자|한글')

# 원본 md 변환이 2단 배치를 뒤섞어 보기가 깨진 쪽 → PDF 쪽을 직접 보고 옮긴 보기 (1주차 3차시 p.49)
QUIZ_FIX = {
    (1, 3): {
        1: ['1) 인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능', '2) 손쉬운 암호 설정으로 인해 부루트포스 공격 가능',
            '3) 없는 주소를 입력하였을 때 에러 메시지와 함께 서버 정보 노출', '4) 틀린 암호를 무제한으로 시도 가능'],
        2: ['1) 악성 코드를 삽입하는 공격이다.', '2) 사용자 입력값을 검증하고 필터링하면 방어할 수 있다.',
            '3) 커맨드 인젝션 방어를 위해 Prepared Statement를 사용해야 한다.', '4) 주로 사용자의 입력값을 그대로 파라미터로 사용할 때 발생한다.'],
        3: ['1) CVE는 소프트웨어와 하드웨어 보안 취약점을 공개한 시스템이다.', '2) 보안 연구원, 기업, 기관이 발견한 취약점은 CNA에 보고된다.',
            '3) CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한 목록이다.', '4) 특정제품에서 발견된 취약점은 CVE 목록에서 찾을 수 있다.'],
    },
}

def parse_quiz(qbody, abody, key=None):
    # 문제 쪽 + 정답 쪽 → [{'n','q','opts','a','detail'}], notes
    qb, qnotes = _blocks(_lines(qbody))
    ab, anotes = _blocks(_lines(abody))
    out = []
    for n in sorted(set(qb) | set(ab)):
        q, opts = '', []
        for i, s in enumerate(qb.get(n, [])):
            if i == 0:
                q = s; continue
            sp = _split_opts(s)
            if sp: opts += sp
            elif re.match(r'^\d\)', s): opts.append(s)
            elif re.match(r'^\(\s*[　\s]*\)$', s): q += ' ( )'       # 단답 빈칸
            elif re.match(r'^\(.+\)$', s) and HINT_PAT.search(s): q += ' ' + s   # "(영문 3글자)" 힌트
            elif not opts: q += ' ' + s                              # 여러 줄 질문
            else: opts[-1] += ' ' + s                                # 여러 줄 보기
        if n in QUIZ_FIX.get(key, {}):            # 원본 변환이 깨진 보기는 PDF를 보고 적은 값으로 교체
            opts = QUIZ_FIX[key][n]
        a, detail = '', []
        for i, s in enumerate(ab.get(n, [])):
            m = re.match(r'^(\d\)\s*.*?)\s+[—–-]\s+(.*)$', s)       # "3) 답 — 해설" 한 줄형
            if not a and m:
                a = m.group(1).strip(); detail.append(m.group(2).strip()); continue
            if not a and re.match(r'^\(.+\)$', s) and HINT_PAT.search(s):
                continue   # "(영문 3글자)" 같은 힌트 괄호는 정답이 아님
            if not a and (re.match(r'^\d\)', s) or re.match(r'^\(.+\)$', s)):
                a = s; continue
            if not a:
                continue   # 정답 앞의 줄 = 문제 문장 반복
            if re.match(r'^\d\)\s*$', a):                            # "1)" 만 있고 보기 문장이 다음 줄인 형식
                a = a + ' ' + s; continue
            detail.append(s)
        if not a and ab.get(n):
            # 정답 표기가 보기 번호/괄호가 아닌 경우: 첫 줄을 정답으로 둔다(검수 대상)
            a = ab[n][0]; detail = ab[n][1:]
        out.append({'n': n, 'q': q.strip(), 'opts': opts, 'a': a.strip(), 'detail': ' '.join(detail).strip()})
    return out, qnotes + anotes

# ---------- 2-SLIDES.md ----------
slide_text_by_wc = {}
with open(f'{OUT}/2-SLIDES.md', 'w', encoding='utf-8') as f:
    f.write('# 2-SLIDES — 교안 원문 (신뢰도 A)\n\n')
    f.write('> 출처: 이동재 교수님 강의교안 PDF를 마크다운으로 변환한 원문. 1~7주차. 검색 시 이 파일이 가장 신뢰도 높음.\n')
    f.write('> 위치 표기: `[2-SLIDES] N주차 M차시 p.X`\n\n')
    for (w, c), path in sorted(SLIDES.items()):
        md = read(path)
        slide_text_by_wc[(w,c)] = md
        kws = keywords_for(md)
        f.write(f'\n# [2-SLIDES] {w}주차 {c}차시 — {WEEK_TITLE[w]}\n')
        if kws:
            f.write('키워드: ' + ' · '.join(kws) + '\n')
        for num, body in pages(md):
            body = strip_html(body).strip('\n')
            if not body:
                continue
            fh = first_heading(body)
            f.write(f'\n## [2-SLIDES] {w}주차 {c}차시 p.{num}' + (f' · {fh}' if fh else '') + '\n')
            f.write(tag_inner_headings(body, '2-SLIDES', w, c, num, fh) + '\n')
print('2-SLIDES done')

# ---------- 1-QUESTIONS.md (교안 퀴즈) ----------
with open(f'{OUT}/1-QUESTIONS.md', 'w', encoding='utf-8') as f:
    f.write('# 1-QUESTIONS — 교안 퀴즈 (신뢰도 A)\n\n')
    f.write('> 각 차시 교안 끝의 퀴즈와 정답·해설. 교수님이 고른 문제라 시험 1순위 참고. 문제 하나 = 섹션 하나.\n')
    f.write('> 위치 표기: `[1-QUESTIONS] N주차 M차시 p.X · 퀴즈 K` (p.X = 문제 쪽). 각 섹션의 `출처:` 줄에 문제 쪽·정답 쪽 번호.\n\n')
    QUIZ_CHECK = []   # 검수용: 정답이 보기 번호/괄호 형식이 아닌 항목
    for (w, c), md in sorted(slide_text_by_wc.items()):
        ps = pages(md)
        quiz = [(n, b, is_quiz_page(b)) for n, b in ps if is_quiz_page(b)]
        if not quiz:
            continue
        qpages = [(n, b) for n, b, lab in quiz if '정답' not in lab]
        apages = [(n, b) for n, b, lab in quiz if '정답' in lab]
        qbody = '\n'.join(b for _, b in qpages); abody = '\n'.join(b for _, b in apages)
        qp = ', '.join(f'p.{n}' for n, _ in qpages) or '없음'; ap = ', '.join(f'p.{n}' for n, _ in apages) or '없음'
        qnum = qpages[0][0] if qpages else apages[0][0]
        items, notes = parse_quiz(qbody, abody, (w, c))
        kws = keywords_for(md)
        f.write(f'\n# [1-QUESTIONS] {w}주차 {c}차시 — {WEEK_TITLE[w]}\n')
        if kws:
            f.write('키워드: ' + ' · '.join(kws) + '\n')
        for it in items:
            f.write(f'\n## [1-QUESTIONS] {w}주차 {c}차시 p.{qnum} · 퀴즈 {it["n"]}\n')
            f.write(f'문제: {it["q"]}\n')
            for o in it['opts']:
                f.write(o + '\n')
            f.write(f'정답: {it["a"] or "(원문 확인)"}\n')
            if it['detail']:
                f.write(f'해설: {it["detail"]}\n')
            f.write(f'출처: [2-SLIDES] {w}주차 {c}차시 {qp} (문제) · {ap} (정답)\n')
            if not re.match(r'^(\d\)|\()', it['a']):
                QUIZ_CHECK.append((w, c, it['n'], it['a'][:40]))
        if notes:
            f.write(f'\n## [1-QUESTIONS] {w}주차 {c}차시 p.{qnum} · 비고\n')
            for s in notes:
                if s.startswith('(변환 메모'):
                    continue   # 변환기 메모는 퀴즈 비고에 불필요
                f.write(s + '\n')
print('1-QUESTIONS done; 검수 대상(정답 형식 특이):', QUIZ_CHECK)

# ---------- 3-TRANSCRIPT.md (강사 발화) ----------
def w15_utts(full_txt):
    t = read(full_txt)
    out = {}  # 차시 -> [(mmss, text)]
    cur = None
    for ln in t.splitlines():
        m = re.match(r'SDU 시큐어코딩 \d+주차 (\d)차시 \|', ln)
        if m:
            cur = int(m.group(1)); out.setdefault(cur, [])
            continue
        m = re.match(r'강사 발화 \((\d+):([\d.]+)[–\-]', ln)
        if m and cur:
            mm, ss = m.group(1), m.group(2)
            txt = ln.split('):', 1)[1].strip() if '):' in ln else ''
            out[cur].append((f'{int(mm):02d}:{ss.split(".")[0]:0>2}', txt))
    return out

def w67_utts(path):
    out = []
    for ln in read(path).splitlines():
        m = re.match(r'\[(\d+):(\d+)\]\s*(.*)', ln)
        if m:
            out.append((f'{int(m.group(1)):02d}:{m.group(2)}', m.group(3)))
    return out

with open(f'{OUT}/3-TRANSCRIPT.md', 'w', encoding='utf-8') as f:
    f.write('# 3-TRANSCRIPT — 강의 발화 (신뢰도 B)\n\n')
    f.write('> 강사 발화만 시각 순으로 추출(화면 묘사 제외). 자동 전사라 숫자·영문·용어에 오인식 가능.\n')
    f.write('> 위치 표기: `[N주차 M차시 mm:ss]`\n\n')
    for w in range(1, 8):
        for c in (1, 2, 3):
            if w <= 5:
                utts = w15_utts(f'/home/claude/sc/tr/w{w}_full.txt').get(c, [])
            else:
                utts = w67_utts(f'/home/claude/sc/tr/w{w}_{c}.txt')
            if not utts:
                continue
            kws = keywords_for(' '.join(x[1] for x in utts))
            f.write(f'\n# [3-TRANSCRIPT] {w}주차 {c}차시 — {WEEK_TITLE[w]}\n')
            if kws:
                f.write('키워드: ' + ' · '.join(kws) + '\n\n')
            for mmss, txt in utts:
                if txt:
                    f.write(f'[{w}주차 {c}차시 {mmss}] {txt}\n')
print('3-TRANSCRIPT done')

# ---------- 0-INDEX.md (보안약점/주제 → 위치) ----------
def locate(syns):
    s_hits, t_hits = [], []
    low = [x.lower() for x in syns]
    for (w, c), md in sorted(slide_text_by_wc.items()):
        if any(x in md.lower() for x in low):
            s_hits.append(f'{w}-{c}')
    for w in range(1, 8):
        for c in (1, 2, 3):
            tp = f'/home/claude/sc/tr/w{w}_full.txt' if w <= 5 else f'/home/claude/sc/tr/w{w}_{c}.txt'
            if not os.path.exists(tp):
                continue
            txt = read(tp).lower()
            if w <= 5:
                # 해당 차시 구간만
                segs = re.split(r'SDU 시큐어코딩 \d+주차 \d차시 \|', read(tp))
            if any(x in txt for x in low):
                t_hits.append(f'{w}-{c}')
    # 녹취는 주차 단위로 압축
    tw = sorted(set(h.split('-')[0] for h in t_hits), key=int)
    return s_hits, tw

with open(f'{OUT}/0-INDEX.md', 'w', encoding='utf-8') as f:
    f.write('# 0-INDEX — 찾아보기 (먼저 여기를 본다)\n\n')
    f.write('> 개념 → 어느 파일/주차에 있는지. 표에서 위치를 확인한 뒤 해당 파일을 검색하면 빠름.\n')
    f.write('> 파일 신뢰도: 1-QUESTIONS(A·퀴즈) · 2-SLIDES(A·교안) · 3-TRANSCRIPT(B·발화) · 4-NOTES(C~D·AI정리)\n\n')
    f.write('주차 요약: ' + ' / '.join(f'{w}주차 {t}' for w, t in WEEK_TITLE.items()) + '\n\n')
    f.write('| 개념 | 검색 표기 | 교안(2-SLIDES) 주차-차시 | 발화(3-TRANSCRIPT) 주차 |\n')
    f.write('|---|---|---|---|\n')
    for rep, syns in SYN.items():
        s_hits, tw = locate(syns)
        if not s_hits and not tw:
            continue
        f.write(f'| {rep} | {", ".join(syns[:4])} | {", ".join(s_hits) or "-"} | {", ".join(tw) or "-"} |\n')

    # ---- 교안 쪽 제목 전체 목록: "자료에 있는데 못 찾는" 경우를 줄이기 위한 목차 ----
    f.write('\n## [0-INDEX] 교안 쪽 제목 목록 (626쪽 전체) — 문제의 핵심어를 여기서 먼저 찾는다\n')
    f.write('> 같은 제목이 이어지면 쪽 범위로 묶음. 제목에 없어도 본문에 있을 수 있으니, 여기 없으면 2-SLIDES 본문을 핵심어로 다시 검색한다.\n')
    S2 = read(f'{OUT}/2-SLIDES.md')
    cur = None; rows = []
    for m in re.finditer(r'^## \[2-SLIDES\] (\d)주차 (\d)차시 p\.(\d+)(?: · ([^\n]*))?$', S2, re.M):
        w, c, pg, t = int(m.group(1)), int(m.group(2)), int(m.group(3)), (m.group(4) or '').strip()
        if cur != (w, c):
            cur = (w, c); rows.append(('H', w, c)); last = None
        if last and last[0] == t and last[2] == pg - 1:
            last[2] = pg
        else:
            last = [t, pg, pg]; rows.append(('R', last))
    for r in rows:
        if r[0] == 'H':
            f.write(f'\n### [0-INDEX] {r[1]}주차 {r[2]}차시 교안 제목 — {WEEK_TITLE[r[1]]}\n')
        else:
            t, a, b = r[1]
            f.write((f'p.{a}' if a == b else f'p.{a}~{b}') + f' {t}\n')

    # ---- 퀴즈 문항 목록: 시험 보기와 겹치는 퀴즈를 한눈에 ----
    f.write('\n## [0-INDEX] 교안 퀴즈 문항 목록 (63문제) — 시험 문제와 겹치는지 먼저 본다\n')
    Q2 = read(f'{OUT}/1-QUESTIONS.md')
    for m in re.finditer(r'^## \[1-QUESTIONS\] (\d주차 \d차시) p\.(\d+) · 퀴즈 (\d+)\n문제: ([^\n]*)\n(.*?)^정답: ([^\n]*)$', Q2, re.S | re.M):
        q = m.group(4).strip(); q = q if len(q) <= 90 else q[:88] + '…'
        f.write(f'- [1-QUESTIONS] {m.group(1)} 퀴즈 {m.group(3)} — {q} → 정답 {m.group(6).strip()[:40]}\n')
print('0-INDEX done')

for fn in ['0-INDEX', '1-QUESTIONS', '2-SLIDES', '3-TRANSCRIPT']:
    p = f'{OUT}/{fn}.md'
    print(fn, os.path.getsize(p), 'bytes')
