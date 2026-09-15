# -*- coding: utf-8 -*-
"""패치 스크립트 공용 — 함수 통째 교체 + JS 문법 검사 (node --check)"""
import io, os, re, subprocess, sys, tempfile

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "index.html")

def load():
    return io.open(P, encoding="utf-8").read()

def save(s):
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)

def rep(s, old, new, cnt=1):
    n = s.count(old)
    assert n == cnt, ("치환 개수 불일치", n, cnt, old[:90])
    return s.replace(old, new)

def _fn_span(s, name):
    """`function name(` (또는 async) 시작 위치와, 중괄호를 맞춰 찾은 끝 위치(닫는 } 다음)를 돌려줍니다.
       문자열·템플릿·주석 안의 중괄호는 세지 않습니다."""
    m = re.search(r"\n(async )?function " + re.escape(name) + r"\(", s)
    assert m, "함수 없음: " + name
    start = m.start() + 1
    i = s.index("{", m.end())
    depth = 0; n = len(s)
    mode = None; tpl = []   # mode: None | "'" | '"' | "`" | "//" | "/*"
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
                if depth == 0:
                    return start, i + 1
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
                # ${ ... } 안은 코드 — 중괄호 깊이를 따로 셉니다
                i += 2; d = 1; sub = None
                while i < n and d > 0:
                    ch = s[i]; nh = s[i+1] if i+1 < n else ""
                    if sub is None:
                        if ch in "'\"": sub = ch
                        elif ch == "`":
                            # 중첩 템플릿 — 짝을 찾아 건너뜀 (재귀 대신 단순 스캔)
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
    # 앞의 주석 블록은 남겨 둡니다(설명이 남아도 무해). 뒤 개행 하나 정리
    tail = s[b:]
    if tail.startswith("\n"): tail = tail[1:]
    return s[:a] + tail

def fn_src(s, name):
    a, b = _fn_span(s, name)
    return s[a:b]

def js_check(s):
    m = re.search(r"<script>(.*)</script>", s, re.S)
    js = m.group(1)
    fd, path = tempfile.mkstemp(suffix=".js"); os.close(fd)
    io.open(path, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
    os.remove(path)
    if r.returncode != 0:
        err = r.stderr.strip().splitlines()
        # 줄 번호를 html 기준으로 환산
        head = s[:m.start(1)].count("\n")
        out = []
        for line in err[:12]:
            mm = re.search(r":(\d+)$", line) or re.search(r"\.js:(\d+)", line)
            if mm: line += "   (html %d행)" % (int(mm.group(1)) + head)
            out.append(line)
        raise SystemExit("JS 문법 오류:\n" + "\n".join(out))
    return True
