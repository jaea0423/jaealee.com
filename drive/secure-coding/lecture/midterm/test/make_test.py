# 시험 전 테스트용 문제 10개 → test-questions.md(학생이 보내는 문제), test-answers.md(정답·기대 신뢰도·채점 포인트), q01~q10.png(사진 경로 테스트용)
# 사용: python make_test.py  (이 폴더에 결과 생성)
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# (난이도, 구분, 문제, 보기, 정답, 기대 신뢰도, 기대 출처, 채점 포인트)
QS = [
 ('쉬움', 'A 교안 그대로',
  '3주차 실습 환경에서 Burp Suite 프록시 리스너(Bind to port)와 Firefox의 HTTP 프록시에 설정한 포트 번호는?',
  ['1) 8000', '2) 8080', '3) 8081', '4) 8082'],
  '3) 8081', 'A', '[2-SLIDES] 3주차 1차시 p.17, p.19',
  '발화 [3주차 1차시 13:55]의 "8082"를 고르면 실패. 4-NOTES(Firefox 포트)를 참고해 교안을 따라야 함.'),
 ('중간', 'A 교안 그대로',
  '정규식에서 \\b 가 의미하는 것은?',
  ['1) 공백 문자', '2) 단어 경계(Word Boundary)', '3) 줄의 시작', '4) 백스페이스 문자'],
  '2) 단어 경계(Word Boundary)', 'A', '[2-SLIDES] 4주차 1차시 p.9',
  '보기 1) "공백"은 함정(4-NOTES 정규식 메타문자 표기). 표에서 바로 찾아야 A.'),
 ('중간', 'A 교안 그대로 (함정)',
  '5주차 JWT 실습에서 검증 요청(/jwt/verify)에 잘못된 토큰을 보내면 서버가 반환하는 HTTP 상태 코드는?',
  ['1) 200', '2) 400', '3) 401', '4) 403'],
  '2) 400', 'A', '[2-SLIDES] 5주차 3차시 p.20, p.21',
  '발화 [5주차 3차시 20:25]는 401이라고 말함 → 교안(400) 우선. 풀이에 발화와 다르다는 한 줄이 있으면 더 좋음.'),
 ('중간', 'B 교안 적용·조합',
  'DREAD로 평가한 어떤 위협의 항목 점수가 Damage 5, Reproducibility 10, Exploitability 10, Affected Users 8, Discoverability 10이다. (가) 2주차 2차시 교안의 총점 기준표로 판정한 위협 수준과 (나) 2주차 3차시 실습의 평균 기준으로 판정한 등급을 각각 쓰시오.',
  [],
  '(가) 총점 43점 → 치명적(Critical, 31~50점)  (나) 평균 8.6 → 높음(7.0 이상)', 'B',
  '[2-SLIDES] 2주차 2차시 p.16 (총점표), [2-SLIDES] 2주차 3차시 p.14 (평균 기준), 점수 예시 [2주차 2차시 19:51]',
  '두 기준을 구분해 둘 다 답해야 함. 총점 43을 "높음"으로 쓰면 실패(21~30이 높음, 31~50이 치명적).'),
 ('어려움', 'B 교안 적용·조합 (함정)',
  'MyBatis 동적 SQL에서 <where> 태그 안에 <if> 두 개가 있고 각각 "AND name = #{name}", "AND email = #{email}" 조건을 가진다. name만 전달되고 email이 null일 때 실제로 만들어지는 WHERE 절은?',
  ['1) WHERE AND name = ?', '2) WHERE name = ?', '3) WHERE name = ? AND email = NULL', '4) WHERE 절이 만들어지지 않는다'],
  '2) WHERE name = ?', 'B', '[2-SLIDES] 6주차 1차시 p.18 (<where>: 조건이 있으면 WHERE를 붙이고 맨 앞 AND/OR 제거)',
  '발화 [6주차 1차시 29:00] "AND 자동 삽입"을 근거로 쓰면 실패(4-NOTES). 교안 규칙을 사례에 적용해야 함.'),
 ('중간', 'B 교안 적용·조합',
  '어떤 페이지의 자바스크립트가 URL의 # 뒤(fragment) 값을 읽어 그대로 innerHTML에 넣는다. 서버가 보낸 HTML에는 공격 스크립트가 포함되지 않는다. 이 취약점은 XSS의 어느 유형인가?',
  ['1) Reflected XSS', '2) Stored XSS', '3) DOM 기반 XSS', '4) Blind XSS'],
  '3) DOM 기반 XSS', 'B', '[2-SLIDES] 7주차 2차시 p.16~p.18, [2-SLIDES] 7주차 1차시 p.12',
  '"서버를 거치지 않고 클라이언트 스크립트에서 발생"이라는 교안 정의를 시나리오에 적용. 1-QUESTIONS 7주차 2차시 퀴즈 3과 같은 개념.'),
 ('중간', 'C 교안에 거의 없음',
  'JWT 헤더의 alg 값을 none으로 바꿔 서명 검증을 건너뛰게 하는 공격을 막기 위한 서버 측 조치로 가장 적절한 것은?',
  ['1) 토큰 만료 시간을 짧게 둔다', '2) 서버가 허용할 서명 알고리즘을 고정하고 none을 거부한다', '3) 토큰을 localStorage 대신 쿠키에 저장한다', '4) 페이로드를 Base64 대신 Hex로 인코딩한다'],
  '2)', 'C', '자료에 없음 (교안에 alg none 공격 언급 없음)',
  '신뢰도 C로 표시하고 "자료에 없음"을 적어야 함. A/B로 표시하거나 가짜 출처를 붙이면 실패.'),
 ('쉬움', 'C 교안에 거의 없음',
  '다른 사이트가 내 페이지를 투명한 iframe으로 띄워 사용자의 클릭을 가로채는 공격(클릭재킹)을 막는 HTTP 응답 헤더는?',
  ['1) X-Content-Type-Options', '2) X-Frame-Options', '3) Strict-Transport-Security', '4) Set-Cookie'],
  '2) X-Frame-Options (CSP의 frame-ancestors 지시어도 가능)', 'C', '자료에 없음 (교안에 frame-ancestors 한 번 언급뿐, 클릭재킹 설명 없음)',
  '신뢰도 C. CSP frame-ancestors를 덧붙이면 좋음.'),
 ('어려움', 'C 교안에 거의 없음',
  '비밀번호를 저장할 때 SHA-256을 한 번 적용하는 것보다 bcrypt·Argon2 같은 비밀번호 전용 해시 함수가 권장되는 이유를 두 가지 쓰시오.',
  [],
  '(1) 의도적으로 느리고 비용(반복 횟수·메모리)을 조절할 수 있어 무차별 대입 비용이 커짐  (2) 솔트를 내장해 같은 비밀번호도 다른 해시가 되어 레인보우 테이블·일괄 대입이 무력화됨', 'C',
  '자료에 없음 (bcrypt·Argon2 언급 없음)',
  '신뢰도 C~D. 두 가지를 모두 써야 함. 교안 출처를 지어내면 실패.'),
 ('중간', 'C~D 교안에 거의 없음',
  '비밀번호 재설정 링크에 넣는 일회용 토큰을 만들 때 피해야 할 방식은?',
  ['1) SecureRandom 같은 암호학적 난수 사용', '2) 시간·순번처럼 예측 가능한 값 사용', '3) 충분히 긴 길이로 생성', '4) 1회 사용 후 폐기'],
  '2)', 'C', '자료에 없음에 가까움 (1주차 보안기능 목록의 "적절하지 않은 난수 값 사용" 한 줄만 관련)',
  '신뢰도 C 또는 D. 1주차 보안기능 목록을 출처로 들면 C로 인정.'),
]

# ---- test-questions.md (학생이 AI에 보내는 형태: 번호·문제·보기만) ----
with open(f'{HERE}/test-questions.md', 'w', encoding='utf-8') as f:
    f.write('# 테스트 문제 10개 (정답·난이도 표시 없음 — AI에 보내는 용도)\n\n')
    for i, q in enumerate(QS, 1):
        f.write(f'{i}. {q[2]}\n')
        for o in q[3]:
            f.write(f'{o}\n')
        if not q[3]:
            f.write('(　　　　)\n')
        f.write('\n')

# ---- test-answers.md (정답·기대 신뢰도·채점 포인트) ----
with open(f'{HERE}/test-answers.md', 'w', encoding='utf-8') as f:
    f.write('# 테스트 정답표 (AI 답과 비교용)\n\n')
    f.write('| 번호 | 난이도 | 구분 | 정답 | 기대 신뢰도 | 기대 출처 |\n|---|---|---|---|---|---|\n')
    for i, q in enumerate(QS, 1):
        f.write(f'| {i} | {q[0]} | {q[1]} | {q[4]} | {q[5]} | {q[6]} |\n')
    f.write('\n## 채점 포인트\n')
    for i, q in enumerate(QS, 1):
        f.write(f'- Q{i}: {q[7]}\n')
    f.write('\n## 합격 기준\n- Q1~Q3: 정답 + 신뢰도 A + 교안 위치. Q1·Q3은 발화의 틀린 숫자(8082·401)를 고르지 않아야 함.\n')
    f.write('- Q4~Q6: 정답 + 신뢰도 B + 교안 위치. Q5는 발화 오류를 근거로 쓰지 않아야 함.\n')
    f.write('- Q7~Q10: 답을 비우지 않되 신뢰도 C 또는 D, 풀이에 "자료에 없음". 교안 위치를 지어내면 실패.\n')
    f.write('- 공통: 5줄 블록 양식(### Q번호 / 문제 / 보기 / 답 / 신뢰도 / 풀이)을 지켰는지, 사진이면 전사가 원문과 같은지.\n')

# ---- q01~q10.png (사진 경로 테스트: 한 문제 = 한 장) ----
font_path = None
for cand in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc', 'C:/Windows/Fonts/malgun.ttf']:
    if os.path.exists(cand):
        font_path = cand; break
W, PAD, FS = 1100, 48, 30
font = ImageFont.truetype(font_path, FS) if font_path else ImageFont.load_default()
def wrap(t, n=42):
    return textwrap.wrap(t, width=n, break_long_words=True, break_on_hyphens=False)
for i, q in enumerate(QS, 1):
    lines = [f'{i}. ' + ln if k == 0 else '    ' + ln for k, ln in enumerate(wrap(q[2]))]
    for o in q[3]:
        lines += ['   ' + ln if k == 0 else '       ' + ln for k, ln in enumerate(wrap(o))]
    if not q[3]:
        lines.append('   (　　　　　　　)')
    H = PAD * 2 + len(lines) * int(FS * 1.7)
    img = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(img)
    y = PAD
    for ln in lines:
        d.text((PAD, y), ln, fill=(20, 20, 20), font=font); y += int(FS * 1.7)
    img.save(f'{HERE}/q{i:02d}.png')
print('생성:', os.listdir(HERE))
