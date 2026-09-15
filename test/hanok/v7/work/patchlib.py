# -*- coding: utf-8 -*-
"""패치 스크립트 공용(v7) — 원본이 src/css/*.css · src/js/*.js 로 나뉘어 있습니다.

  import patchlib as L
  s = L.load("js/16-wizard.js"); s = L.rep(s, old, new); L.save("js/16-wizard.js", s)
  L.where("function wzStepSeat(")   # 어느 조각에 있는지
  L.js_check()                       # js 조각 전부 이어 붙여 node --check
"""
import io, os, re, subprocess, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "src")

def path(name):
    return os.path.join(SRC, name.replace("/", os.sep))

def load(name):
    return io.open(path(name), encoding="utf-8").read()

def save(name, s):
    io.open(path(name), "w", encoding="utf-8", newline="\n").write(s)

def parts(kind):
    d = os.path.join(SRC, kind)
    return sorted(kind + "/" + f for f in os.listdir(d) if f.endswith("." + kind))

def where(snippet):
    """snippet 이 든 조각 이름 목록"""
    out = []
    for kind in ("css", "js"):
        for name in parts(kind):
            if snippet in load(name): out.append(name)
    return out

def rep(s, old, new, cnt=1):
    n = s.count(old)
    assert n == cnt, ("치환 개수 불일치", n, cnt, old[:90])
    return s.replace(old, new)

def rep_in(name, old, new, cnt=1):
    """조각을 열어 치환하고 바로 저장"""
    save(name, rep(load(name), old, new, cnt))

def _fn_span(s, name):
    m = re.search(r"(^|\n)(async )?function " + re.escape(name) + r"\(", s)
    assert m, "함수 없음: " + name
    start = m.start() + (1 if m.group(1) == "\n" else 0)
    i = s.index("{", m.end())
    depth = 0; n = len(s); mode = None
    while i < n:
        c = s[i]; nx = s[i+1] if i+1 < n else ""
        if mode is None:
            if c == "/" and nx == "/": mode = "//"; i += 2; continue
            if c == "/" and nx == "*": mode = "/*"; i += 2; continue
            if c in "'\"": mode = c; i += 1; continue
            if c == "`": mode = "`"; i += 1; continue
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: return start, i + 1
            i += 1; continue
        if mode == "//":
            if c == "\n": mode = None
            i += 1; continue
        if mode == "/*":
            if c == "*" and nx == "/": mode = None; i += 2; continue
            i += 1; continue
        if mode in ("'", '"'):
            if c == "\\": i += 2; continue
            if c == mode or c == "\n": mode = None
            i += 1; continue
        if mode == "`":
            if c == "\\": i += 2; continue
            if c == "$" and nx == "{":
                i += 2; d = 1; sub = None
                while i < n and d > 0:
                    ch = s[i]
                    if sub is None:
                        if ch in "'\"": sub = ch
                        elif ch == "`":
                            j = i + 1
                            while j < n and s[j] != "`":
                                if s[j] == "\\": j += 1
                                j += 1
                            i = j + 1; continue
                        elif ch == "{": d += 1
                        elif ch == "}": d -= 1
                    else:
                        if ch == "\\": i += 2; continue
                        if ch == sub: sub = None
                    i += 1
                continue
            if c == "`": mode = None
            i += 1; continue
    raise AssertionError("함수 끝을 못 찾음: " + name)

def replace_fn(s, name, new_src):
    a, b = _fn_span(s, name)
    return s[:a] + new_src.strip("\n") + s[b:]

def remove_fn(s, name):
    a, b = _fn_span(s, name)
    tail = s[b:]
    if tail.startswith("\n"): tail = tail[1:]
    return s[:a] + tail

def fn_src(s, name):
    a, b = _fn_span(s, name)
    return s[a:b]

def js_all():
    return "\n".join(load(n).rstrip("\n") for n in parts("js"))

def js_check():
    js = js_all()
    fd, p = tempfile.mkstemp(suffix=".js"); os.close(fd)
    io.open(p, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    os.remove(p)
    if r.returncode != 0:
        raise SystemExit("JS 문법 오류:\n" + "\n".join(r.stderr.strip().splitlines()[:12]))
    return True
