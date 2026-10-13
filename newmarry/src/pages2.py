# -*- coding: utf-8 -*-
# 새 화면: 요청(신랑신부 → 축의대 담당자), 준비(축의대 담당자 가이드), 개발용 목록
from pages import COUPLE_CAP, BRAND_CAP

# ---------------------------------------------------------------- 요청서 (축의대 담당자가 받는 화면)
# ---------------------------------------------------------------- 준비 가이드 (축의대 담당자용)
def sec(id_, eb, title, desc, inner):
    return '''
    <section class="card gsec" id="%s">
      <div class="eb">%s</div>
      <div class="ch" style="margin-top:4px"><div><h3>%s</h3>%s</div></div>%s
    </section>''' % (id_, eb, title, ('<p>%s</p>' % desc) if desc else '', inner)

def qa(items):
    return '<div class="qa">' + ''.join('<div><b>%s</b><p>%s</p></div>' % (q, a) for q, a in items) + '</div>'

GUIDE_BODY = '''
    <div class="top"><span class="role">축의대 담당자용</span><span class="chip">읽는 데 5분</span><span class="sp"></span><a class="btn2 rose" href="../desk/index.html" style="display:inline-grid;place-items:center;text-decoration:none">화면 연습해 보기</a></div>

    <section class="card hero">
      <div class="eb">BEFORE THE DAY</div>
      <h1>축의대 준비 가이드</h1>
      <p>예식 당일 당황하지 않도록 순서와 예외 상황을 정리했습니다. 처음 해 보는 분도 이것만 읽으면 충분합니다.</p>
      <div class="toc" id="toc">
        <a href="#g-time">하루 흐름</a><a href="#g-role">역할 나누기</a><a href="#g-flow">봉투 받는 순서</a><a href="#g-ticket">식권 주기</a><a href="#g-short">식권이 모자랄 때</a><a href="#g-more">더 달라고 할 때</a><a href="#g-odd">이럴 땐 이렇게</a><a href="#g-close">정산과 인계</a><a href="#g-keys">화면 사용법</a>
      </div>
    </section>
''' + sec('g-time', 'TIMELINE', '하루 흐름', '예식 오후 1시 기준입니다. 예식 시간에 맞춰 앞뒤로 옮기면 됩니다.', '''
      <div class="steps">
        <div><span class="k">12:10</span><span><b>도착</b><small>혼주께 인사하고 식권과 봉투 가방을 받습니다</small></span><span></span></div>
        <div><span class="k">12:20</span><span><b>노트북 켜기</b><small>축의대 화면에 들어가 구분(신랑측/신부측)을 고르고, 받은 식권 장수가 맞는지 셉니다</small></span><span></span></div>
        <div><span class="k">12:30</span><span><b>하객 몰림</b><small>예식 30분 전부터 시작 직후까지 가장 바쁩니다. 이때는 속도가 우선입니다</small></span><span></span></div>
        <div><span class="k">13:00</span><span><b>예식 시작</b><small>늦게 오는 하객이 계속 있으니 자리를 비우지 않습니다</small></span><span></span></div>
        <div><span class="k">14:20</span><span><b>명부 마감 · 정산</b><small>식사가 시작되고 하객이 뜸해지면 마감합니다</small></span><span></span></div>
        <div><span class="k">14:30</span><span><b>인계</b><small>봉투 가방, 남은 식권을 혼주께 직접 드립니다</small></span><span></span></div>
      </div>''') + sec('g-role', 'ROLES', '역할 나누기', '두 명이 가장 편합니다. 한 명이어도 할 수 있습니다.', '''
      <div class="grid3">
        <div class="sidecard"><h4>받는 사람</h4><p class="gp">인사하고 봉투를 받습니다. 성함과 식권 장수를 여쭤 입력하는 사람에게 말해 주고, 화면에 나온 순번을 봉투 뒤에 적어 가방에 넣습니다.</p></div>
        <div class="sidecard"><h4>입력하는 사람</h4><p class="gp">노트북 앞에서 이름, 금액, 식권 장수를 넣고 저장합니다. 저장되면 순번을 받는 사람에게 불러 줍니다.</p></div>
        <div class="sidecard"><h4>혼자일 때</h4><p class="gp">봉투를 받고 바로 입력합니다. 하객이 줄을 서면 금액 입력은 뒤로 미루고 이름과 식권만 먼저 넣어도 됩니다.</p></div>
      </div>
      <p class="gp" style="margin-top:12px">한 구분(신랑측 또는 신부측)에는 노트북 한 대만 씁니다. 입력하는 사람이 바뀌면 화면의 "입력자 교체"를 누릅니다.</p>''') + sec('g-flow', 'STEP BY STEP', '봉투 받는 순서', '', '''
      <div class="steps">
        <div><span class="k paid">1</span><span><b>인사하고 봉투 받기</b><small>"와 주셔서 감사합니다"</small></span><span></span></div>
        <div><span class="k paid">2</span><span><b>성함 확인</b><small>봉투에 이름이 없으면 여쭤봅니다. 끝내 모르면 무기명으로 둡니다</small></span><span></span></div>
        <div><span class="k paid">3</span><span><b>식권 장수 여쭙기</b><small>"식사하실 분 몇 분이세요?"</small></span><span></span></div>
        <div><span class="k paid">4</span><span><b>식권 드리고 입력</b><small>이름 → Tab → 금액 → Enter. 식권은 + 키로 늘립니다</small></span><span></span></div>
        <div><span class="k paid">5</span><span><b>봉투에 순번 적기</b><small>화면에 뜬 번호를 봉투 뒷면에 적습니다. 정산이 안 맞을 때 하나씩 대조하는 기준입니다</small></span><span></span></div>
        <div><span class="k paid">6</span><span><b>봉투는 가방으로</b><small>축의대 위에 봉투를 쌓아 두지 않습니다</small></span><span></span></div>
      </div>
      <p class="gp" style="margin-top:10px">금액은 하객이 자리를 뜬 뒤에 봉투를 열어 확인합니다. 하객 앞에서 봉투를 열지 않습니다.</p>''') + sec('g-ticket', 'MEAL TICKETS', '식권 주기', '', qa([
        ('기본은 한 분에 한 장', '봉투 하나에 식사하실 인원만큼 드립니다. 부부나 가족이 함께 오면 인원 수를 여쭤봅니다.'),
        ('화면에 꼭 적기', '봉투와 함께 드린 식권은 접수 화면의 식권 칸에 적습니다. 정산 때 남은 식권과 맞춰 봅니다.'),
        ('봉투 없이 식권만 드릴 때', '부조 없이 식사만 하시는 분, 혼주 가족, 사회자·사진 기사 같은 진행팀은 화면 위 "식권 추가·따로 지급" → "봉투 없이 드림"에 적습니다.'),
      ])) + sec('g-short', 'RUNNING LOW', '식권이 모자랄 때', '', qa([
        ('30장 아래로 떨어지면', '화면의 "식권 남음" 숫자가 빨갛게 바뀝니다. 이때 바로 혼주께 알립니다. 다 떨어진 뒤에 알리면 하객이 기다리게 됩니다.'),
        ('추가 식권을 받았을 때', '혼주가 가져다주거나, 직접 받아 오거나, 예식장에서 도장을 더 찍어 주면 "식권 추가·따로 지급" → "추가로 받음"에 장수와 방법을 적습니다.'),
        ('식권이 다 떨어졌을 때', '하객께 "식당 입구에서 성함 말씀해 주시면 됩니다"처럼 혼주와 미리 정한 방법으로 안내하고, 메모에 남깁니다.'),
      ])) + sec('g-more', 'EXTRA REQUESTS', '더 달라고 할 때', '', qa([
        ('일행 수만큼은 드립니다', '함께 온 인원이 확인되면 그만큼 드리고 식권 칸에 적습니다.'),
        ('애매하면 혼주께', '"나중에 올 사람 몫"처럼 확인이 어려운 요청은 정중히 "혼주께 여쭤보고 드릴게요"라고 하고 혼주 판단을 따릅니다.'),
        ('이미 받은 분이 더 달라고 하면', '명부에서 그분을 찾아 "수정"에서 식권 장수를 늘립니다. 고친 기록은 시각과 함께 남습니다.'),
        ('남은 식권을 돌려주면', '"식권 추가·따로 지급" → "돌려받음"에 적습니다.'),
      ])) + sec('g-odd', 'EXCEPTIONS', '이럴 땐 이렇게', '', qa([
        ('이름 없는 봉투', '"무기명"에 체크하고 금액만 넣습니다.'),
        ('같은 이름이 이미 있을 때', '화면이 한 번 더 묻습니다. 다른 분이면 저장하고 메모에 구분(예: 회사 동료)을 남깁니다.'),
        ('잘못 저장했을 때', '최근 봉투나 명부에서 "수정"을 눌러 고칩니다. 아예 잘못 들어간 봉투는 수정 창의 "봉투 취소"를 누릅니다. 기록은 지워지지 않고 줄이 그어집니다.'),
        ('계좌로 보냈다는 하객', '축의대에서는 적지 않습니다. 신랑신부가 나중에 따로 적습니다.'),
        ('인터넷이 끊겼을 때', '그대로 계속 입력합니다. 노트북에 저장해 두었다가 다시 연결되면 자동으로 올라갑니다.'),
      ])) + sec('g-close', 'CLOSING', '정산과 인계', '', '''
      <div class="steps">
        <div><span class="k paid">1</span><span><b>명부 마감하고 정산하기</b><small>하객이 뜸해지면 누릅니다. 잘못 눌렀으면 접수로 돌아갈 수 있습니다</small></span><span></span></div>
        <div><span class="k paid">2</span><span><b>현금을 권종별로 세기</b><small>5만·1만·5천·1천 원권 장수와 수표(금액 합계)를 넣으면 명부 합계와 바로 비교합니다</small></span><span></span></div>
        <div><span class="k paid">3</span><span><b>남은 식권 세기</b><small>받은 식권에서 남은 장수를 빼 기록과 맞춰 봅니다</small></span><span></span></div>
        <div><span class="k paid">4</span><span><b>차이가 나면 사유 적기</b><small>순번을 적어 둔 봉투와 명부를 하나씩 대조해 보고, 그래도 다르면 이유를 적습니다</small></span><span></span></div>
        <div><span class="k paid">5</span><span><b>최종 제출 · 인계</b><small>제출하면 더 고칠 수 없습니다. 봉투 가방과 남은 식권을 혼주께 직접 드립니다</small></span><span></span></div>
      </div>''') + sec('g-keys', 'KEYBOARD', '화면 사용법', '마우스 없이 키보드만으로 할 수 있습니다.', '''
      <div class="grid3">
        <div class="sidecard"><h4><span><kbd>Tab</kbd></span></h4><p class="gp">다음 칸으로 (성함 → 금액 → 식권 → 저장). 저장에서 Enter</p></div>
        <div class="sidecard"><h4><span><kbd>Enter</kbd></span></h4><p class="gp">저장. 성함 칸에서는 금액 칸으로</p></div>
        <div class="sidecard"><h4><span><kbd>+</kbd> <kbd>−</kbd></span></h4><p class="gp">식권 한 장 늘리기·줄이기</p></div>
      </div>
      <p class="gp" style="margin-top:12px">금액은 만 원 단위입니다. 5를 넣으면 5만 원, 3.5는 3만 5천 원, 1000은 1천만 원입니다.</p>
      <a class="save" href="../desk/index.html" style="display:grid;place-items:center;text-decoration:none">화면 연습해 보기</a>''')

GUIDE = dict(title='축의지기 준비 가이드', cap=COUPLE_CAP, body=GUIDE_BODY, script='''
  /* 목차: 누르면 오른쪽 영역 안에서 해당 절로 스크롤 */
  $('#toc').addEventListener('click', function (e) {
    var a = e.target.closest('a'); if (!a) return; e.preventDefault();
    var t = document.querySelector(a.getAttribute('href')); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
''')

# ---------------------------------------------------------------- 개발용 목록
PAGES = [
    ('register', '등록', '신랑신부', '예식 정보를 넣고 예식을 만듭니다.', '시안'),
    ('setup', '설정', '신랑신부', '축의대 담당(4명까지), 당일 정보, 식권 장수, 배경 그림, 혼주 열람, 결제. 미정으로 두면 진행 전까지 채웁니다.', '시안'),
    ('request', '요청', '축의대 담당자', '신랑신부가 보낸 부탁: 언제·어디서·누구와·무엇을. 미정과 변동이 표시됩니다.', '시안'),
    ('guide', '준비', '축의대 담당자', '식권 주는 법, 모자랄 때, 더 달라고 할 때, 역할 분담, 정산 순서 가이드.', '시안'),
    ('desk', '진행', '축의대 담당자', '예식 당일 봉투 접수, 식권, 수정, 정산, 제출.', '시안'),
    ('status', '현황', '신랑신부 · 혼주', '접수 상황을 실시간으로 봅니다.', '시안'),
    ('result', '결과', '신랑신부', '명부 확인, 계좌이체 추가, 정산 기록, 내려받기.', '시안'),
]
TODO = [
    ('로그인 · 계정', '신랑신부 공용 계정. 개발 마지막에 붙입니다.'),
    ('축의대 PIN 입장', '진행 화면 들어갈 때 PIN 확인. 개발 마지막에 붙입니다.'),
    ('혼주 열람 입장', '혼주가 현황을 볼 때 쓰는 입장 화면.'),
    ('후정산 금액 입력', '"금액은 나중에" 방식일 때 예식 뒤 봉투를 열어 금액만 넣는 화면.'),
    ('결제', '토스페이먼츠 등 결제 연동, 영수증.'),
    ('서비스 소개', '처음 오는 신랑신부에게 보여 줄 첫 화면.'),
    ('약관 · 개인정보 처리방침', '명부(하객 이름·금액) 저장에 필요한 문서.'),
    ('만료 · 오류 안내', '3개월이 지나 지워진 예식, 잘못된 링크 등.'),
]
NAV_BODY = '''
    <div class="top"><span class="chip">개발용 화면 목록</span><span class="sp"></span><button type="button" class="btn2 shopbtn" data-shop="shop/">축의대 용품</button></div>
    <section class="card">
      <div class="ch"><div><h3>만든 화면</h3><p>예식 흐름 순서입니다. 각 화면은 폴더 하나에 index.html로 들어 있습니다.</p></div></div>
      <div class="navlist">''' + ''.join('''
        <a class="navitem" href="%s/index.html"><span class="k paid">%d</span><span><b>%s</b> <span class="who2">%s</span><small>%s</small><code>/%s/</code></span><span class="pill ok">%s</span></a>''' % (f, i + 1, n, w, d, f, st) for i, (f, n, w, d, st) in enumerate(PAGES)) + '''
      </div>
    </section>
    <section class="card">
      <div class="ch"><div><h3>아직 없는 화면</h3><p>만들어야 할 화면입니다. 순서는 정해지지 않았습니다.</p></div></div>
      <div class="todolist">''' + ''.join('<div><b>%s</b><small>%s</small></div>' % (n, d) for n, d in TODO) + '''
      </div>
    </section>
'''
NAV = dict(title='축의지기 개발 목록', cap=BRAND_CAP, body=NAV_BODY, script='')
