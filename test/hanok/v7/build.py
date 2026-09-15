"""
한옥반점 예약 시스템 — 빌드 스크립트 (v7)

  결과물은 v5 폴더 안에만 만들어집니다. 원본(상위 폴더)은 절대 건드리지 않습니다.

  python build.py        prod — supabase.prod.json 을 끼워 dist/ · index.html · screen/index.html
  python build.py dev    dev  — supabase.dev.json  을 끼워 dev/index.html · dev/screen/index.html

  Supabase 접속 설정(__SUPA_CFG__): 설정 파일이 없으면 null 을 넣습니다 → 앱은 지금처럼 브라우저 안에서만(seedDemo) 돕니다.
  그래서 설정 파일 없이도 빌드가 깨지지 않습니다. anon 키만 넣습니다 — service_role 은 어떤 파일에도 쓰지 않습니다.

폴더를 어떻게 두든 알아서 파일을 찾습니다.
전부 한 폴더에 넣어도 되고, src/assets/dist 로 나눠도 됩니다.

  [한 폴더에 다 넣는 경우]        [나누는 경우]
  hanok/                         hanok/
  ├── build.py                   ├── build.py
  ├── index.html                 ├── src/index.html
  ├── hanok.b64                  ├── assets/hanok.b64
  ├── anjip.b64                  ├── assets/anjip.b64
  ├── bg1.b64 ~ bg7.b64          ├── assets/bg1.b64 ~ bg7.b64
  └── (결과물이 여기 생김)        └── dist/(결과물)

주의: 만들어진 hanok-admin.html 을 직접 고치지 마세요.
     이미지가 들어가 1.3MB라 편집이 사실상 불가능합니다.
     항상 원본(index.html)을 고치고 이 스크립트를 다시 돌리세요.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

SRC_CANDIDATES = [
    "src/page.html",
    "src/index.html",
    "index.html",
    "src/hanok-admin.html",
    "hanok-admin-src.html",
    "v3.html",
]
# 이미지는 원본(../assets), 글꼴은 v4(../v4/assets) 것을 그대로 씁니다 — 복사해 두면 나중에 갈라집니다.
ASSET_DIRS = ["assets", "../v4/assets", "../assets", ".", "src", "img", "images"]

SUBS = [("__ANJIP_B64__", "anjip.b64"), ("__HANOK_B64__", "hanok.b64")] + \
       [("__BG%d_B64__" % i, "bg%d.b64" % i) for i in range(1, 8)] + \
       [# 글꼴 — 한글 2,350자(KS X 1001)+영문+기호로 서브셋한 woff2 를 base64 로.
        # 외부에서 불러오지 않는 이유: 오프라인·구형 TV 에서도 떠야 합니다.
        # 원본: Pretendard 1.3.9 (OFL), Noto Serif KR (OFL). 만드는 법은 v4/work/fonts.md
        ("__FONT_PT_R__", "font-Pretendard-Regular.b64"),
        ("__FONT_PT_B__", "font-Pretendard-Bold.b64"),
        ("__FONT_PT_S__", "font-Pretendard-SemiBold.b64"),
        ("__FONT_NS_7__", "font-NotoSerifKR-700.b64"),
        ("__FONT_NS_9__", "font-NotoSerifKR-900.b64")]


def find_source():
    """원본 HTML 찾기. 정해진 이름이 없으면 자리표시자가 든 파일을 뒤집니다."""
    for rel in SRC_CANDIDATES:
        path = os.path.join(BASE, rel)
        if os.path.exists(path):
            return path
    for root, _dirs, files in os.walk(BASE):
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(root, f)
            try:
                head = open(path, encoding="utf-8").read(400000)
            except Exception:
                continue
            if "__HANOK_B64__" in head:
                return path
    return None


def find_asset(name):
    """이미지 파일 찾기."""
    for d in ASSET_DIRS:
        path = os.path.join(BASE, d, name)
        if os.path.exists(path):
            return path
    for root, _dirs, files in os.walk(BASE):
        if name in files:
            return os.path.join(root, name)
    return None


def pick_output(src_path):
    """결과물 위치. dist 폴더가 있거나 src/ 구조면 dist 에, 아니면 옆에."""
    if os.path.isdir(os.path.join(BASE, "dist")) or \
       os.path.basename(os.path.dirname(src_path)) == "src":
        out_dir = os.path.join(BASE, "dist")
    else:
        out_dir = BASE
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "hanok-admin.html")


def supa_cfg(mode):
    """Supabase 접속 설정을 JSON 문자열로. 파일이 없으면 'null'.
       키 검사: anon 키(JWT 의 role 이 anon)만 허용 — service_role 이 실수로 들어오면 빌드를 멈춥니다."""
    path = os.path.join(BASE, "supabase.%s.json" % mode)
    if not os.path.exists(path) and mode == "prod" and os.path.exists(os.path.join(BASE, "supabase.dev.json")):
        # 실서비스 프로젝트가 아직 없으면 사이트(index.html)도 dev DB 에 붙입니다 — 설정 없는 빌드는 아무 PIN 이나 통과해서 사이트에 올리면 안 됩니다
        print("supabase.prod.json 없음 → 사이트 빌드에 supabase.dev.json 을 씁니다 (실서비스 프로젝트를 만들면 prod 로 바뀝니다)")
        path = os.path.join(BASE, "supabase.dev.json"); mode = "dev"
    if not os.path.exists(path):
        print("Supabase 설정 없음: %s → 브라우저 안에서만 도는(예시 데이터) 빌드. 잠금 화면에서 들어갈 수 없습니다 — 사이트에 올리지 마세요" % os.path.relpath(path, BASE))
        return "null"
    cfg = json.load(open(path, encoding="utf-8"))
    for k in ("url", "anonKey", "staffEmail", "adminEmail"):
        if not cfg.get(k):
            print("Supabase 설정에 %s 가 없습니다: %s" % (k, path)); sys.exit(1)
    try:
        import base64
        payload = cfg["anonKey"].split(".")[1]
        payload += "=" * (-len(payload) % 4)
        role = json.loads(base64.urlsafe_b64decode(payload)).get("role")
    except Exception:
        role = None
    if role == "service_role":
        print("!! service_role 키가 들어 있습니다. 이 키는 파일에 넣으면 안 됩니다(전체 DB 권한). anon public 키로 바꾸세요."); sys.exit(1)
    cfg["mode"] = mode
    cfg["demo"] = bool(cfg.get("demo")) and mode == "dev"   # 예시 데이터 버튼은 dev 에서만 (prod 에서는 코드상 없음)
    print("Supabase 설정: %s (%s, role=%s, demo=%s)" % (os.path.relpath(path, BASE), cfg["url"], role, cfg["demo"]))
    return json.dumps(cfg, ensure_ascii=False)


def assemble(src_path):
    """v7: 원본은 src/page.html + src/css/*.css + src/js/*.js 로 나뉘어 있습니다(이름 순서대로 이어 붙임).
       나눈 이유: 한 파일 1만 줄은 찾기도 고치기도 어려웠습니다. 배포 형태(HTML 하나)는 그대로입니다.
       옛 방식(src/index.html 한 파일)도 그대로 받습니다."""
    html = open(src_path, encoding="utf-8").read()
    if "__CSS__" not in html and "__JS__" not in html:
        return html
    src_dir = os.path.dirname(src_path)
    def cat(sub, ext):
        d = os.path.join(src_dir, sub)
        names = sorted(f for f in os.listdir(d) if f.endswith(ext))
        return "\n".join(open(os.path.join(d, f), encoding="utf-8").read().rstrip("\n") for f in names)
    return html.replace("__CSS__", cat("css", ".css")).replace("__JS__", cat("js", ".js"))


def main():
    mode = "dev" if "dev" in sys.argv[1:] else "prod"
    src_path = find_source()
    if not src_path:
        print("원본 HTML 을 찾지 못했습니다.")
        print("index.html 또는 src/index.html 을 build.py 와 같은 폴더에 두세요.")
        print("현재 폴더:", BASE)
        sys.exit(1)

    print("원본:", os.path.relpath(src_path, BASE))
    html = assemble(src_path)

    missing = []
    for key, fname in SUBS:
        if key not in html:
            continue
        path = find_asset(fname)
        if not path:
            missing.append(fname)
            continue
        html = html.replace(key, open(path, encoding="utf-8").read().strip())

    if missing:
        print("이미지를 찾지 못했습니다:", ", ".join(missing))
        print("이 파일들을 build.py 와 같은 폴더나 assets 폴더에 두세요.")
        sys.exit(1)

    # Supabase 접속 설정. src 에 `var SUPA_CFG = __SUPA_CFG__;` 한 줄이 있어야 합니다(7차 묶음 B 에서 넣음). 없으면 그냥 지나갑니다
    if "__SUPA_CFG__" in html:
        html = html.replace("__SUPA_CFG__", supa_cfg(mode))

    left = set(re.findall(r"__[A-Z0-9_]+__", html))
    if left:
        print("채워지지 않은 자리표시자:", ", ".join(sorted(left)))

    m = re.search(r"<script>(.*)</script>", html, re.S)
    if m:
        js = m.group(1)
        bad = [
            ("옵셔널 체이닝 ?.", r"\?\."),
            ("널 병합 ??", r"\?\?[^=]"),
            ("structuredClone", r"structuredClone\("),
            (".flat()", r"\.flat\("),
            (".replaceAll()", r"\.replaceAll\("),
        ]
        hit = False
        for name, pat in bad:
            n = len(re.findall(pat, js))
            if n:
                print("경고: 구형 브라우저 미지원 문법 — %s %d건" % (name, n))
                hit = True
        if hit:
            print("      스마트TV 에서 흰 화면이 뜹니다. 고친 뒤 다시 빌드하세요.")
        else:
            print("구형 브라우저 문법 검사 통과")

    # dev 빌드는 dev/ 폴더에만 씁니다 (jaealee.com/test/hanok/v6/dev/). 실서비스 파일은 건드리지 않습니다
    if mode == "dev":
        dev_dir = os.path.join(BASE, "dev"); dev_screen = os.path.join(dev_dir, "screen")
        for d in (dev_dir, dev_screen):
            if not os.path.isdir(d): os.makedirs(d)
        open(os.path.join(dev_dir, "index.html"), "w", encoding="utf-8").write(html)
        open(os.path.join(dev_screen, "index.html"), "w", encoding="utf-8").write(html)
        print("생성 완료: dev/index.html · dev/screen/index.html (%dKB) — 개발용. 광고 영상은 dev/screen/ 에 없어 사진으로 대신 나옵니다" % (len(html.encode("utf-8")) // 1024))
        return

    out = pick_output(src_path)
    open(out, "w", encoding="utf-8").write(html)
    print("생성 완료: %s (%dKB)" % (os.path.relpath(out, BASE), os.path.getsize(out) // 1024))

    # 이 폴더는 jaealee.com/test/hanok 주소로 그대로 올라갑니다.
    # 그 주소가 여는 파일은 루트 index.html 이라, 같이 갱신해야 사이트가 실제로 바뀝니다.
    # 단, 한 폴더에 다 넣은 경우에는 index.html 이 원본이므로 덮어쓰면 안 됩니다.
    site = os.path.join(BASE, "index.html")
    if os.path.abspath(site) != os.path.abspath(src_path):
        open(site, "w", encoding="utf-8").write(html)
        print("생성 완료: index.html (사이트 배포용 · 위 파일과 같은 내용)")

    # 손님용 TV 화면은 screen/ 폴더로 엽니다 (jaealee.com/test/hanok/v6/screen/).
    # 같은 파일입니다 — 주소에 screen 이 있으면 스스로 디스플레이 모드로 들어갑니다(readRoute).
    # 따로 두는 이유: TV 에는 이 주소만 알려 주면 되고, 광고 영상(ad.mp4)도 이 폴더에 함께 둡니다.
    screen_dir = os.path.join(BASE, "screen")
    if os.path.abspath(site) != os.path.abspath(src_path):
        if not os.path.isdir(screen_dir): os.makedirs(screen_dir)
        open(os.path.join(screen_dir, "index.html"), "w", encoding="utf-8").write(html)
        print("생성 완료: screen/index.html (손님용 TV · 같은 내용)")


if __name__ == "__main__":
    main()
