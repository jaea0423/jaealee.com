"""정적 서버 + 결과 저장 (헤드리스 크롬 스크린샷·클래스 조합 수집용)
GET  /...            → 프로젝트 루트(hanok/) 기준 파일. v2 는 /v2/... 로
POST /save?name=X    → 본문을 v2/work/snaps/X.json 으로 저장
실행: python v2/work/serve.py 8766
"""
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

WORK = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(WORK))          # hanok/
os.makedirs(os.path.join(WORK, "snaps"), exist_ok=True)

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=PROJ, **k)
    def do_POST(self):
        u = urlparse(self.path)
        if u.path == "/save":
            name = parse_qs(u.query).get("name", ["x"])[0]
            name = "".join(c for c in name if c.isalnum() or c in "-_.")
            n = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            with open(os.path.join(WORK, "snaps", name + ".json"), "wb") as f:
                f.write(body)
            self.send_response(200); self.send_header("Content-Type", "text/plain")
            self.end_headers(); self.wfile.write(b"ok")
        else:
            self.send_response(404); self.end_headers()
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
