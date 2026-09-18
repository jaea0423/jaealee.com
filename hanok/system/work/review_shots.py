# -*- coding: utf-8 -*-
"""전수 검토용 스크린샷 + 화면 글자 모음 (2026-09-17).
   시스템의 모든 화면·시트·마법사 단계·설정 묶음·홈페이지 관리 탭·TV 와 사이트 여섯 장·예약 창 7단계를
   태블릿(820)·폰(390)·PC(1440)·TV(1920) 폭으로 찍고, 각 화면에 보이는 글자를 옆에 뽑아 review/index.html 한 장으로 모읍니다.
   → 눈으로 훑기만 해도 '만든 게 맞나'(문구·디자인·빠진 것)를 잡으려고. '만든 대로 되나' 는 검토_시나리오.md 가 봅니다.

   python work/review_shots.py            (HANOK_PIN 필요 — dev 직원 계정으로 실제 데이터를 띄웁니다)
   python work/review_shots.py site       사이트만
   python work/review_shots.py sys        시스템만
   8767 서버(hanok/ 루트)가 떠 있어야 합니다. """
import io, json, os, sys, subprocess, time, urllib.request, urllib.parse, html, re
from PIL import Image

WORK = os.path.dirname(os.path.abspath(__file__)); SYS = os.path.dirname(WORK); ROOT = os.path.dirname(SYS)
OUT = os.path.join(WORK, "review"); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://127.0.0.1:8767"
PROFILE = os.path.join(WORK, ".chrome-profile")
cfg = json.load(io.open(os.path.join(SYS, "supabase.dev.json"), encoding="utf-8"))

def token():
    PIN = os.environ.get("HANOK_PIN")
    if not PIN: raise SystemExit("HANOK_PIN 환경변수가 필요합니다")
    req = urllib.request.Request(cfg["url"] + "/auth/v1/token?grant_type=password",
        data=json.dumps({"email": cfg["staffEmail"], "password": PIN + "00"}).encode(), headers={"apikey": cfg["anonKey"], "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())

def chrome(url, w, h, png, budget=14000, dump=False):
    ww = max(w, 500)
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--user-data-dir=" + PROFILE,
            "--window-size=%d,%d" % (ww, h), "--timeout=%d" % (budget + 4000), "--virtual-time-budget=%d" % budget]
    if dump: args.append("--dump-dom")
    else: args.append("--screenshot=" + png)
    args.append(url)
    r = subprocess.run(args, capture_output=True, timeout=180, text=True, encoding="utf-8", errors="replace")
    if not dump and ww != w and os.path.exists(png):
        im = Image.open(png); im.crop((0, 0, w, h)).save(png)
    return r.stdout if dump else None

def wrap_url(src, w, h, js):
    return "%s/system/work/shot.html?src=%s&w=%d&h=%d&js=%s" % (BASE, urllib.parse.quote(src, safe="/?="), w, h, urllib.parse.quote(js, safe=""))

def text_of_dump(dom):
    m = re.search(r'data-text="([^"]*)"', dom or "")
    return html.unescape(m.group(1)) if m else ""

# ---------- 시스템 화면 목록 ----------
def sys_jobs(tok):
    sess = json.dumps({"access_token": tok["access_token"], "refresh_token": tok["refresh_token"], "expires_at": int(time.time()) + 3000, "who": "staff"})
    login = ("SESSION=%s; sessionSave(); INTRO=null; view.storeKey='hanok'; REQ_SEEN_INIT=true; window.reqNotify=function(){}; window.reqNotifyPending=function(){}; "
             "enterStore().then(function(){ INTRO=null; try{clearIntro(true);}catch(e){} view.date=todayStr(); MODAL=null; render(); "
             "setTimeout(function(){ try{ %s }catch(e){ document.title='ERR '+e; } render(); "
             "setTimeout(function(){ if(typeof tlPlaceLabels==='function') tlPlaceLabels(); parent.document.body.setAttribute('data-text', document.body.innerText.slice(0,6000)); parent.document.title='ready'; }, 400); }, 1200); });") % (sess, "%s")
    T = "todayStr()"; TM = "shiftDate(todayStr(),1)"
    first_res = "store().reservations.filter(function(r){return r.date===todayStr()&&r.status==='확정'})[0]"
    un_res = "store().reservations.filter(function(r){return r.date>=todayStr()&&!r.roomId&&r.seatPref==='room-any'&&r.status==='확정'})[0]"
    jobs = [
      ("01 매장 선택",     "sessionClear(); AUTHED=false; view.storeKey=null;"),
      ("02 PIN 잠금",      "AUTHED=false; view.storeKey='hanok'; PIN_BUF='10';"),
      ("03 대시보드 목록(오늘)", "view.tab='dash'; view.mView='list'; view.mode='list'; view.open.list=true;"),
      ("04 대시보드 타임라인(오늘)", "view.tab='dash'; view.mView='graph'; view.mode='graph';"),
      ("05 타임라인 내일",  "view.tab='dash'; view.mView='graph'; view.mode='graph'; view.date=%s;" % TM),
      ("06 더보기 메뉴",    "view.tab='dash'; view.moreOpen=true;"),
      ("07 달력",           "openCal();"),
      ("08 예약 검색",      "openSearch(); setTimeout(function(){ var i=document.querySelector('.sheet input'); if(i){ i.value='장'; i.dispatchEvent(new Event('input')); } },100);"),
      ("09 영업시간 시트",  "openHours();"),
      ("10 예약률 추이",    "openRate();"),
      ("11 화면 보정",      "openZoomAdj();"),
      ("12 홈페이지 예약 목록", "openRequests();"),
      ("13 홈페이지 예약 상세", "openRequest(reqPending()[0].id);"),
      ("14 거절 시트",      "openReqReject(reqPending()[0].id);"),
      ("15 확인 목록",      "openCheck();"),
      ("16 확인 → 사용 중지 좌석", "openPick('blocked');"),
      ("17 확인 → 알러지",  "openPick('allergy');"),
      ("18 확인 → 단체",    "openPick('group');"),
      ("19 예약 상세·수정", "openRes(%s.id);" % first_res),
      ("20 예약 상태(방문·취소)", "openMark(%s.id);" % first_res),
      ("21 좌석 미배정 목록", "openUnassigned();"),
      ("22 마법사 0 경로",  "openWizard();"),
      ("23 마법사 1 날짜·시각", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.step=1;" % TM),
      ("24 마법사 1 경고(라스트오더 뒤)", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='21:30'; WZ.step=1;" % TM),
      ("25 마법사 2 인원",  "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.step=2; WZ.people=4; WZ.infants=1;" % TM),
      ("26 마법사 3 좌석(룸)", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.people=4; WZ.step=3; WZ.seatKind='room';" % TM),
      ("27 마법사 3 좌석(테이블)", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.people=4; WZ.step=3; WZ.seatKind='table';" % TM),
      ("28 마법사 3 경고(정원 초과)", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.people=9; WZ.step=3; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id;" % TM),
      ("29 마법사 4 메뉴",  "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=4; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.menuType='코스';" % TM),
      ("30 마법사 5 손님",  "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=5; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.name='홍길동'; WZ.phone='010-1234-5678';" % TM),
      ("31 마법사 6 알러지·요청", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.infants=1; WZ.step=6; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.name='홍길동'; WZ.phone='010-1234-5678';" % TM),
      ("32 네이버 가져오기", "openNaver();"),
      ("33 예정 설정 목록", "openScheduled();"),
      ("34 마법사 3 특정 테이블 지정", "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=3; WZ.seatKind='table'; WZ.tableAdv=true;" % TM),
      ("35 노쇼 관리", "openNoshow();"),
      ("36 설정 · 좌석 · 테이블", "view.adminOk=true; view.tab='settings'; Object.keys(view.open).forEach(function(k){view.open[k]=false;}); view.open['s_seats']=true; view.seatTab='table';"),
      ("37 설정 · 좌석 · 합침", "view.adminOk=true; view.tab='settings'; Object.keys(view.open).forEach(function(k){view.open[k]=false;}); view.open['s_seats']=true; view.seatTab='join';"),
      ("40 설정(접힘)",     "view.adminOk=true; view.tab='settings';"),
    ]
    for key, name in [("site","홈페이지"),("hours","운영시간"),("rules","예약 규칙"),("seats","좌석"),("course","코스·세트 구성"),("source","예약경로"),("sms","문자 안내"),("disp","디스플레이 배치"),("policy","운영 판단 기준"),("zoom","화면 크기"),("admin","관리자"),("etc","기타")]:
        jobs.append(("41 설정 · %s" % name, "view.adminOk=true; view.tab='settings'; Object.keys(view.open).forEach(function(k){view.open[k]=false;}); view.open['s_%s']=true;" % key))
    jobs += [
      ("50 사용 중지 시트", "view.adminOk=true; view.tab='settings'; openBlocks(roomsAt(todayStr()).filter(isRoom)[5].id);"),
      ("51 임시 영업·휴무", "view.adminOk=true; view.tab='settings'; openOverride();"),
      ("52 운영시간 수정",  "view.adminOk=true; view.tab='settings'; openSchedule(null);"),
      ("53 접속 기록",      "view.adminOk=true; view.tab='settings'; view.form={type:'logs'};"),
      ("54 설정 변경 내역", "view.adminOk=true; view.tab='settings'; view.form={type:'setlog'};"),
      ("55 PIN 관리",       "view.adminOk=true; view.tab='settings'; view.form={type:'pinlist'};"),
      ("56 PIN 변경",       "view.adminOk=true; view.tab='settings'; openPin();"),
      ("57 관리자 비밀번호 변경", "view.adminOk=true; view.tab='settings'; openAdminPw();"),
      ("58 문자 기록",      "view.adminOk=true; view.tab='settings'; openSmsLog();"),
      ("59 문자 직접 보내기", "view.adminOk=true; view.tab='settings'; openSmsFree();"),
      ("60 테이블 편집",    "view.adminOk=true; view.tab='settings'; openTableEdit(roomsAt(todayStr()).filter(isTable)[0].id);"),
    ]
    site_open = "view.adminOk=true; openSiteAdmin();"
    for key, name in [("online","홈페이지 예약"),("notices","팝업 공지"),("posts","소식"),("hours","영업시간·연락처"),("texts","글"),("menu","차림"),("images","사진"),("history","적용 기록")]:
        jobs.append(("61 홈페이지 관리 · %s" % name, site_open + " setTimeout(function(){ if(SA&&!SA.loading){ SA.tab='%s'; render(); } }, 2500);" % key))
    jobs.append(("61 홈페이지 관리 · 소식 글 고치기", site_open + " setTimeout(function(){ if(SA&&!SA.loading){ SA.tab='posts'; saPostsLoad().then(function(){ if(SA.posts&&SA.posts[0]) saPostEdit(SA.posts[0].id); }); } }, 2500);"))
    jobs.append(("64 단골 등급 · 목록", "view.tab='dash'; view.open.list=true; var bd={}; store().reservations.forEach(function(r){ if(r.date>=todayStr()&&r.status==='확정'&&custStat(r).tier) bd[r.date]=(bd[r.date]||0)+1; }); var best=Object.keys(bd).sort(function(a,b){return bd[b]-bd[a];})[0]; if(best){ view.date=best; view.calMonth=best.slice(0,7); }"))
    jobs.append(("64 단골 등급 · TV", "var t=store().reservations.filter(function(r){return r.date===todayStr()&&r.status==='확정';}); if(t[0]) t[0].tier='VVIP'; if(t[1]) t[1].tier='VIP'; view.display=true; store().settings.tvType='list';"))
    jobs.append(("65 워크시프트 · 주간표", "view.adminOk=true; openStaffPage();"))
    jobs.append(("66 워크시프트 · 칸 편집", "view.adminOk=true; openStaffPage().then(function(){ if(HR.staff[0]) hrCell(HR.staff[0].id, todayStr()); });"))
    jobs.append(("67 워크시프트 · 직원 편집", "view.adminOk=true; openStaffPage().then(function(){ if(HR.staff[0]) hrStaffEdit(HR.staff[0].id); });"))
    jobs.append(("68 워크시프트 · 급여", "view.adminOk=true; openStaffPage().then(function(){ HR.view='pay'; render(); });"))
    jobs.append(("68 워크시프트 · 급여계산서", "view.adminOk=true; openStaffPage().then(function(){ HR.view='pay'; HR.slip={id:HR.staff[0].id, month:HR.month}; render(); });"))
    jobs.append(("68 워크시프트 · 설정", "view.adminOk=true; openStaffPage().then(function(){ hrSetupOpen(); });"))
    jobs.append(("69 손님 관리", "view.adminOk=true; openGuestsPage();"))
    jobs.append(("69 손님 관리 · 상세", "view.adminOk=true; openGuestsPage().then(function(){ var l=gsList(); if(l[0]) gsOpen(l[0].phone); });"))
    jobs.append(("62 홈페이지 관리 · 적용 대화창", site_open + " setTimeout(function(){ if(SA&&!SA.loading){ view.saApply={mode:'at', date:shiftDate(todayStr(),1), time:'09:00', note:''}; render(); } }, 2500);"))
    jobs.append(("63 홈페이지 관리 · 미리보기", site_open + " setTimeout(function(){ if(SA&&!SA.loading){ view.saPreview='index'; render(); } }, 2500);"))
    return login, jobs

def site_jobs():
    pages = [("index","홈"),("about","이야기"),("space","공간"),("menu","차림"),("visit","오시는 길"),("reserve","예약")]
    jobs = [("S%02d 사이트 · %s" % (i+1, n), "/%s.html?shot=1" % p, 5200) for i, (p, n) in enumerate(pages)]
    jobs.append(("S07 사이트 · 팝업", "/index.html?shot=notice&notice=1", 1100))
    jobs.append(("S08 사이트 · 소식", "/news.html?shot=1", 2400))   # 14차. 첫 글을 펼친 채로 보려면 #post_… 를 붙임
    for k in range(1, 8):
        jobs.append(("S1%d 예약 창 %d단계" % (k, k), "/reserve.html?shot=1&rv=%d" % k, 1000))
    return jobs

def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    items = []   # (title, width, png, text)
    if what in ("all", "sys"):
        tok = token(); login, jobs = sys_jobs(tok)
        only = os.environ.get("REVIEW_ONLY")
        for title, js in jobs:
            if only and not any(title.startswith(x) for x in only.split(",")): continue   # REVIEW_ONLY="03,04,41 설정 · 좌석" 처럼 쉼표로 여럿
            # 폰(390)은 모바일 작업(2026-09-17)부터 전 화면. REVIEW_W=390 이면 폰만
            wenv = os.environ.get("REVIEW_W")
            widths = [int(wenv)] if wenv else [820, 390]
            for w in widths:
                h = 1180 if w == 820 else 900
                png = os.path.join(OUT, "%s_%d.png" % (re.sub(r"[^\w가-힣]+", "_", title), w))
                full = login % js.replace("'", "'")
                url = wrap_url("/system/dev/index.html?v=%d" % int(time.time()), w, h, full)
                chrome(url, w, h, png, budget=9000)
                dom = chrome(url, w, h, png, budget=9000, dump=True) if w == widths[0] else ""   # 글자는 폭이 달라도 같아 첫 폭만 뽑음(시간 절반)
                items.append((title, w, os.path.basename(png), text_of_dump(dom)))
                print("shot", os.path.basename(png), os.path.getsize(png) if os.path.exists(png) else 0)
        # TV
        for title, js, w, h in [("70 TV 목록형", "view.display=true; store().settings.tvType='list';", 1920, 1080), ("71 TV 좌석표", "view.display=true; store().settings.tvType='grid';", 1920, 1080)]:
            png = os.path.join(OUT, "%s_%d.png" % (re.sub(r"[^\w가-힣]+", "_", title), w))
            full = login % js
            url = wrap_url("/system/dev/index.html?v=%d" % int(time.time()), w, h, full)
            chrome(url, w, h, png); dom = chrome(url, w, h, png, dump=True)
            items.append((title, w, os.path.basename(png), text_of_dump(dom))); print("shot", os.path.basename(png))
    if what in ("all", "site"):
        for title, path, h in site_jobs():
            for w in (1440, 390):
                hh = h if w == 1440 else min(h, 8000)
                png = os.path.join(OUT, "%s_%d.png" % (re.sub(r"[^\w가-힣]+", "_", title), w))
                js = "setTimeout(function(){ parent.document.body.setAttribute('data-text', document.body.innerText.slice(0,6000)); parent.document.title='ready'; }, 2500);"
                url = wrap_url(path + "&v=%d" % int(time.time()), w, hh, js)
                chrome(url, w, hh, png, budget=9000); dom = chrome(url, w, hh, png, budget=9000, dump=True)
                items.append((title, w, os.path.basename(png), text_of_dump(dom))); print("shot", os.path.basename(png))
    # ---------- 한 장으로 ----------
    rows = []
    for title, w, png, txt in items:
        rows.append('<section class="it"><h3>%s <small>%dpx</small></h3><div class="row"><a href="%s" target="_blank"><img src="%s" loading="lazy"></a><pre>%s</pre></div></section>'
                    % (html.escape(title), w, png, png, html.escape(txt)))
    doc = ('<!doctype html><meta charset="utf-8"><title>한옥반점 검토 갤러리</title><style>body{font:14px/1.5 -apple-system,"Malgun Gothic",sans-serif;margin:0;padding:20px;background:#f4f3f0;color:#222}'
           'h1{font-size:20px} .it{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px;margin:0 0 16px} h3{margin:0 0 10px;font-size:15px} h3 small{color:#888;font-weight:400}'
           '.row{display:flex;gap:16px;align-items:flex-start} .row img{max-width:60%%;max-height:900px;border:1px solid #ccc;object-fit:contain;object-position:top} .row pre{flex:1;white-space:pre-wrap;font:12px/1.5 inherit;color:#444;background:#fafafa;padding:10px;border-radius:6px;max-height:900px;overflow:auto;margin:0}'
           '</style><h1>한옥반점 검토 갤러리 — %s</h1><p>왼쪽 그림·오른쪽 그 화면의 글자. 이상한 문구·빠진 것·깨진 것을 번호와 함께 적어 주세요.</p>%s' % (time.strftime("%Y-%m-%d %H:%M"), "".join(rows)))
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(doc)
    print("gallery:", os.path.join(OUT, "index.html"), len(items), "shots")

if __name__ == "__main__":
    main()
