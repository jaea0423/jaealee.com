#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RED — Routine Every Day
─────────────────────────────────────────────────────────
하루 기록 텔레그램 봇.
맥에서 24시간 켜두고 쓰는 상주 프로그램이다. 하는 일은 넷뿐이다.

  1. 밤 23:00   → 내일 날짜가 채워진 '입력 틀'을 보낸다
  2. 아침 07:00 → 오늘 시간표 페이지 링크를 보낸다
  3. 아침 07:30 → 오늘 뉴스 링크를 보낸다
  4. 아무 때나  → /help 같은 명령어에 답한다

설계 원칙
  · 표준 라이브러리만 쓴다. pip install 필요 없음.
  · 틀과 규칙 문구를 이 파일에 넣지 않는다.
    https://jaealee.com/schedule/template.txt 를 그때그때 받아온다.
    → 저장소의 template.txt만 고치면 봇 메시지도 같이 바뀐다.
  · 토큰은 이 파일에 절대 넣지 않는다. 설정 파일이나 환경변수로 받는다.
"""

import html
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ══════════════════════════════════════════════════════
# 기본값 — 설정 파일에서 덮어쓸 수 있다
# ══════════════════════════════════════════════════════
TZ = ZoneInfo("Asia/Seoul")

DEFAULTS = {
    "MORNING_TIME": "07:00",                                        # 시간표 링크 보낼 시각
    "NEWS_TIME":    "07:30",                                        # 뉴스 링크 보낼 시각
    "EVENING_TIME": "23:00",                                        # 내일 틀 보낼 시각
    "TEMPLATE_URL": "https://jaealee.com/schedule/template.txt",    # 틀·규칙 원본
    "SCHEDULE_URL": "https://jaealee.com/schedule/",                # 시간표 뷰어
    "DATA_URL":     "https://jaealee.com/schedule/data/",           # 시간표 JSON 폴더
    "NEWS_URL":     "https://jaealee.com/news/view.html",           # 뉴스 뷰어
    "NEWS_DATA_URL":"https://jaealee.com/news/data/",               # 뉴스 JSON 폴더
}

API = "https://api.telegram.org/bot{token}/{method}"

# 틀 구간을 잘라낼 때 쓰는 표시. template.txt 안에 그대로 들어있다.
MARK_START = "### 여기부터 복사 ###"
MARK_END   = "### 여기까지 복사 ###"
MARK_RULES = "규칙 요약"


# ══════════════════════════════════════════════════════
# 설정 읽기
# ══════════════════════════════════════════════════════
def load_config():
    """
    설정을 읽는다. 우선순위는 '환경변수 > 설정파일 > 기본값'.

    설정 파일 위치는 아래 순서로 찾는다.
      1) 실행할 때 준 인자        python3 red.py /경로/config.env
      2) 환경변수 RED_CONFIG
      3) ~/.config/red/config.env
    """
    cfg = dict(DEFAULTS)

    if len(sys.argv) > 1:
        path = sys.argv[1]
    elif os.environ.get("RED_CONFIG"):
        path = os.environ["RED_CONFIG"]
    else:
        path = os.path.expanduser("~/.config/red/config.env")

    # 설정 파일이 있으면 KEY=VALUE 형식으로 한 줄씩 읽는다
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")

    # 환경변수가 있으면 그게 이긴다
    for k in list(cfg) + ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]:
        if os.environ.get(k):
            cfg[k] = os.environ[k]

    # 토큰과 대화방 번호는 없으면 아예 시작할 수 없다
    for need in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        if not cfg.get(need):
            sys.exit(
                f"[RED 설정 오류] {need} 가 없습니다.\n"
                f"  설정 파일: {path}\n"
                f"  config.example.env 를 복사해서 채우세요."
            )
    return cfg


def state_path():
    """'오늘 이미 보냈는지' 기억해두는 파일 경로."""
    d = os.path.expanduser("~/.local/state/red")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "state.json")


def load_state():
    try:
        with open(state_path(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(st):
    with open(state_path(), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


# ══════════════════════════════════════════════════════
# 텔레그램 API
# ══════════════════════════════════════════════════════
def api_call(cfg, method, params=None, timeout=60):
    """텔레그램 API를 부른다. 실패하면 None을 돌려주고 죽지 않는다."""
    url = API.format(token=cfg["TELEGRAM_BOT_TOKEN"], method=method)
    data = urllib.parse.urlencode(params or {}).encode()
    try:
        with urllib.request.urlopen(url, data=data, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        log(f"HTTP {e.code} ({method}): {body}")
    except Exception as e:
        log(f"통신 실패 ({method}): {e}")
    return None


def send(cfg, text, preview=False):
    """
    메시지를 보낸다. 4096자 제한이 있어서 길면 잘라서 여러 번 보낸다.
    parse_mode=HTML 이므로 넘기는 text는 이미 이스케이프돼 있어야 한다.
    """
    LIMIT = 3900          # 여유를 두고 자른다
    chunks, buf = [], ""
    for line in text.split("\n"):
        if len(buf) + len(line) + 1 > LIMIT:
            chunks.append(buf)
            buf = line
        else:
            buf = (buf + "\n" + line) if buf else line
    if buf:
        chunks.append(buf)

    for c in chunks:
        api_call(cfg, "sendMessage", {
            "chat_id": cfg["TELEGRAM_CHAT_ID"],
            "text": c,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false" if preview else "true",
        })


def code_block(s):
    """텔레그램에서 '탭하면 전체 복사'가 되는 코드 블록으로 감싼다."""
    return "<pre>" + html.escape(s) + "</pre>"


# ══════════════════════════════════════════════════════
# template.txt 가져오기 + 구간 잘라내기
# ══════════════════════════════════════════════════════
_cache = {"text": None, "at": 0}


def fetch_template(cfg, force=False):
    """
    template.txt를 받아온다. 10분간은 받아둔 걸 재사용한다.
    실패하면 마지막으로 성공했던 내용을 쓰고, 그것도 없으면 None.
    """
    now = time.time()
    if not force and _cache["text"] and now - _cache["at"] < 600:
        return _cache["text"]
    try:
        req = urllib.request.Request(
            cfg["TEMPLATE_URL"],
            headers={"Cache-Control": "no-cache"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            _cache["text"] = r.read().decode("utf-8")
            _cache["at"] = now
    except Exception as e:
        log(f"틀 가져오기 실패: {e}")
    return _cache["text"]


def cut_form(text, which=0):
    """
    '### 여기부터 복사 ###' ~ '### 여기까지 복사 ###' 사이를 잘라낸다.
    which=0 이면 첫 번째(틀 A), 1이면 두 번째(틀 B).
    """
    if not text:
        return None
    parts, pos = [], 0
    while True:
        s = text.find(MARK_START, pos)
        if s < 0:
            break
        e = text.find(MARK_END, s)
        if e < 0:
            break
        parts.append(text[s + len(MARK_START):e].strip("\n"))
        pos = e + len(MARK_END)
    return parts[which] if which < len(parts) else None


def cut_rules(text):
    """맨 아래 '규칙 요약' 부분만 잘라낸다."""
    if not text:
        return None
    i = text.find(MARK_RULES)
    if i < 0:
        return None
    # 제목 줄 다음부터 끝까지. 바로 아래 '=====' 줄은 버린다.
    rest = text[i + len(MARK_RULES):]
    lines = [ln for ln in rest.split("\n")]
    while lines and (not lines[0].strip() or set(lines[0].strip()) <= {"=", "←", " "}
                     or lines[0].strip().startswith("←")):
        lines.pop(0)
    return "\n".join(lines).strip()


def fill_date(form, day):
    """틀의 비어 있는 [날짜] 칸에 날짜를 채워 넣는다."""
    if not form:
        return form
    out, hit = [], False
    for line in form.split("\n"):
        out.append(line)
        if line.strip() == "[날짜]" and not hit:
            hit = True
            # [날짜] 바로 다음의 빈 줄 하나를 날짜로 바꾼다
            out.append(day)
    if not hit:
        return form
    # [날짜] 다음에 원래 있던 빈 줄 하나를 지운다 (중복 방지)
    txt = "\n".join(out)
    return txt.replace(f"[날짜]\n{day}\n\n", f"[날짜]\n{day}\n", 1)


# ══════════════════════════════════════════════════════
# 날짜 유틸
# ══════════════════════════════════════════════════════
def now_kst():
    return datetime.now(TZ)


def ymd(d):
    return d.strftime("%Y-%m-%d")


def url_exists(url):
    """주소가 실제로 열리는지 확인한다. 파일을 받지 않고 머리만 물어본다."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def has_record(cfg, day):
    """그날 시간표 JSON이 올라와 있는지 확인한다."""
    return url_exists(cfg["DATA_URL"] + day + ".json")


def has_news(cfg, day):
    """그날 뉴스 JSON이 발행됐는지 확인한다."""
    return url_exists(cfg["NEWS_DATA_URL"] + day + ".json")


def log(msg):
    print(f"[{now_kst():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


# ══════════════════════════════════════════════════════
# 실제로 보내는 메시지들
# ══════════════════════════════════════════════════════
def send_evening(cfg):
    """저녁: 내일 날짜가 채워진 틀."""
    tomorrow = ymd(now_kst() + timedelta(days=1))
    form = fill_date(cut_form(fetch_template(cfg, force=True), 0), tomorrow)
    if not form:
        send(cfg, "⚠️ 틀을 가져오지 못했습니다. template.txt 를 확인하세요.")
        return
    send(cfg,
         f"🌙 <b>내일({tomorrow}) 시간표</b>\n"
         f"아래를 눌러 복사한 뒤 채워서 보내세요.\n\n"
         + code_block(form) +
         "\n간단한 틀은 /simple · 규칙은 /help")
    log(f"저녁 틀 발송 ({tomorrow})")


def send_morning(cfg):
    """아침: 오늘 시간표 링크."""
    today = ymd(now_kst())
    link = f"{cfg['SCHEDULE_URL']}?date={today}"
    if has_record(cfg, today):
        body = f"☀️ <b>오늘({today}) 시간표</b>\n{link}"
    else:
        body = (f"☀️ <b>오늘({today})</b>\n"
                f"기록이 아직 없습니다.\n{link}")
    send(cfg, body, preview=True)
    log(f"아침 링크 발송 ({today})")


def send_news(cfg):
    """아침: 오늘 뉴스 링크. 아직 발행 전이어도 링크는 그대로 보낸다."""
    today = ymd(now_kst())
    link = f"{cfg['NEWS_URL']}?date={today}"
    tail = "" if has_news(cfg, today) else "\n<i>아직 발행 전일 수 있습니다.</i>"
    send(cfg, f"📰 <b>오늘({today}) 뉴스</b>\n{link}{tail}", preview=True)
    log(f"뉴스 링크 발송 ({today})")


HELP_HEAD = (
    "🔴 <b>RED</b> — Routine Every Day\n\n"
    "<b>/help</b>  이 도움말 + 입력 규칙\n"
    "<b>/template</b>  전체 칸 틀 (내일 날짜)\n"
    "<b>/simple</b>  간단 틀 (내일 날짜)\n"
    "<b>/today</b>  오늘 시간표 링크\n"
    "<b>/news</b>  오늘 뉴스 링크\n"
    "<b>/date 2026-08-19</b>  그날 시간표 링크\n"
    "<b>/status</b>  봇 상태 확인\n"
)


def handle(cfg, text):
    """명령어 하나를 처리한다."""
    cmd, _, arg = text.strip().partition(" ")
    cmd = cmd.split("@")[0].lower()      # /help@내봇이름 형태도 받아준다
    arg = arg.strip()

    if cmd in ("/start", "/help", "/rules"):
        rules = cut_rules(fetch_template(cfg))
        send(cfg, HELP_HEAD + ("\n" + code_block(rules) if rules else ""))

    elif cmd in ("/template", "/form"):
        day = arg or ymd(now_kst() + timedelta(days=1))
        form = fill_date(cut_form(fetch_template(cfg, force=True), 0), day)
        send(cfg, code_block(form) if form else "⚠️ 틀을 가져오지 못했습니다.")

    elif cmd == "/simple":
        day = arg or ymd(now_kst() + timedelta(days=1))
        form = fill_date(cut_form(fetch_template(cfg, force=True), 1), day)
        send(cfg, code_block(form) if form else "⚠️ 간단 틀을 가져오지 못했습니다.")

    elif cmd == "/today":
        send_morning(cfg)

    elif cmd == "/news":
        send_news(cfg)

    elif cmd == "/date":
        try:
            datetime.strptime(arg, "%Y-%m-%d")
        except ValueError:
            send(cfg, "날짜 형식이 다릅니다. 예) <code>/date 2026-08-19</code>")
            return
        mark = "" if has_record(cfg, arg) else "  (기록 없음)"
        send(cfg, f"{arg}{mark}\n{cfg['SCHEDULE_URL']}?date={arg}", preview=True)

    elif cmd == "/status":
        st = load_state()
        send(cfg,
             f"현재 시각 {now_kst():%Y-%m-%d %H:%M} (KST)\n\n"
             f"시간표 {cfg['MORNING_TIME']}  ·  마지막 {st.get('morning', '-')}\n"
             f"뉴스 {cfg['NEWS_TIME']}  ·  마지막 {st.get('news', '-')}\n"
             f"틀 {cfg['EVENING_TIME']}  ·  마지막 {st.get('evening', '-')}")

    else:
        send(cfg, "모르는 명령어입니다. /help 를 눌러보세요.")


# ══════════════════════════════════════════════════════
# 정시 발송 판정
# ══════════════════════════════════════════════════════
def due(cfg, st, job, hhmm):
    """
    지금이 job(morning/evening)을 보낼 때인지 본다.

    · 정한 시각을 지났고
    · 오늘 아직 안 보냈으면  → 보낸다

    '지났으면 보낸다'로 만든 이유: 맥이 잠깐 잠들었다 깨어나
    정확한 시각을 놓쳐도 그날 안에 한 번은 나가게 하려는 것이다.
    단, 6시간 넘게 지난 건 이미 늦었으니 건너뛴다.
    """
    now = now_kst()
    today = ymd(now)
    if st.get(job) == today:
        return False
    try:
        h, m = [int(x) for x in hhmm.split(":")]
    except ValueError:
        return False
    target = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if now < target:
        return False
    if (now - target).total_seconds() > 6 * 3600:
        st[job] = today          # 너무 늦음 — 오늘 건 보낸 셈 치고 넘어간다
        save_state(st)
        log(f"{job} 건너뜀 (예정 시각에서 6시간 초과)")
        return False
    return True


# ══════════════════════════════════════════════════════
# 메인 루프
# ══════════════════════════════════════════════════════
def main():
    cfg = load_config()
    st = load_state()
    offset = None

    log("RED 시작 — Routine Every Day")
    log(f"시간표 {cfg['MORNING_TIME']} · 뉴스 {cfg['NEWS_TIME']} "
        f"· 틀 {cfg['EVENING_TIME']} (KST)")

    # 시작할 때 쌓여 있던 옛날 메시지는 버린다 (껐다 켤 때 폭주 방지)
    first = api_call(cfg, "getUpdates", {"timeout": 0, "offset": -1}, timeout=20)
    if first and first.get("result"):
        offset = first["result"][-1]["update_id"] + 1

    while True:
        # ── 1. 정시 발송 확인 ──
        # (작업 이름, 설정 키, 보낼 함수) 세 쌍만 늘리면 발송이 하나 추가된다
        JOBS = [
            ("morning", "MORNING_TIME", send_morning),
            ("news",    "NEWS_TIME",    send_news),
            ("evening", "EVENING_TIME", send_evening),
        ]
        for job, key, fn in JOBS:
            try:
                if due(cfg, st, job, cfg[key]):
                    fn(cfg)
                    st[job] = ymd(now_kst())
                    save_state(st)
            except Exception as e:
                log(f"{job} 발송 중 오류: {e}")

        # ── 2. 새 메시지 확인 (최대 30초 기다린다) ──
        res = api_call(cfg, "getUpdates",
                       {"timeout": 30, "offset": offset or ""}, timeout=45)
        if not res or not res.get("ok"):
            time.sleep(5)          # 인터넷이 끊겼을 수 있다. 쉬었다 다시.
            continue

        for up in res.get("result", []):
            offset = up["update_id"] + 1
            msg = up.get("message") or up.get("edited_message")
            if not msg:
                continue
            # 내 대화방에서 온 것만 받는다. 남이 봇을 찾아내도 무시된다.
            if str(msg.get("chat", {}).get("id")) != str(cfg["TELEGRAM_CHAT_ID"]):
                continue
            text = msg.get("text", "")
            if not text.startswith("/"):
                continue
            try:
                log(f"명령어: {text}")
                handle(cfg, text)
            except Exception as e:
                log(f"명령어 처리 중 오류: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("종료")
