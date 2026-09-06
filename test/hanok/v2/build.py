"""
한옥반점 예약 시스템 — 빌드 스크립트 (v2 전용)

  결과물은 v2 폴더 안에만 만들어집니다. 원본(상위 폴더)은 절대 건드리지 않습니다.

  python3 build.py

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
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

SRC_CANDIDATES = [
    "src/index.html",
    "index.html",
    "src/hanok-admin.html",
    "hanok-admin-src.html",
    "v2.html",
]
# v2 는 이미지(assets)를 원본과 함께 씁니다 — 1.1MB 를 복사해 두면 나중에 갈라집니다.
# "../assets" 하나만 추가한 것 외에는 원본 build.py 와 같습니다.
ASSET_DIRS = ["assets", "../assets", ".", "src", "img", "images"]

SUBS = [("__ANJIP_B64__", "anjip.b64"), ("__HANOK_B64__", "hanok.b64")] + \
       [("__BG%d_B64__" % i, "bg%d.b64" % i) for i in range(1, 8)]


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


def main():
    src_path = find_source()
    if not src_path:
        print("원본 HTML 을 찾지 못했습니다.")
        print("index.html 또는 src/index.html 을 build.py 와 같은 폴더에 두세요.")
        print("현재 폴더:", BASE)
        sys.exit(1)

    print("원본:", os.path.relpath(src_path, BASE))
    html = open(src_path, encoding="utf-8").read()

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


if __name__ == "__main__":
    main()
