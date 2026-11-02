"""Pavement Enforcement site server: serves the generated public/ folder only.

Never receives leads (forms are front-end only). Answers POST with 405.
Clean URLs: /services -> 301 /services/ (query string kept); /services/ -> services/index.html.
Run: PORT=8080 python3 server.py
"""
import mimetypes
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
for _ext, _type in {".webp": "image/webp", ".svg": "image/svg+xml", ".js": "application/javascript", ".txt": "text/plain",
                    ".xml": "application/xml", ".webm": "video/webm", ".mp4": "video/mp4", ".woff2": "font/woff2"}.items():
    mimetypes.add_type(_type, _ext)
PORT = int(os.environ.get("PORT", "8080"))


class Handler(SimpleHTTPRequestHandler):
    server_version = "PE"
    sys_version = ""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        if os.environ.get("ACCESS_LOG"):
            print(self.address_string(), fmt % args, file=sys.stderr, flush=True)

    def _headers(self, path, ctype):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        if ctype.startswith("text/html"):
            self.send_header("Cache-Control", "no-cache, must-revalidate")
        elif "?v=" in self.path:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "public, max-age=86400")

    def _send(self, rel, status=200, head=False):
        full = os.path.join(ROOT, rel)
        with open(full, "rb") as f:
            data = f.read()
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "image/svg+xml", "application/xml"):
            ctype += "; charset=utf-8"
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", "").strip()) if status == 200 else None
        if m and (m.group(1) or m.group(2)):   # Safari/iOS need 206 for <video>
            size = len(data)
            start = int(m.group(1)) if m.group(1) else max(0, size - int(m.group(2)))
            end = min(int(m.group(2)) if m.group(1) and m.group(2) else size - 1, size - 1)
            if start > end:
                self.send_response(416); self.send_header("Content-Range", f"bytes */{size}"); self.send_header("Content-Length", "0")
                return self.end_headers()
            data = data[start:end + 1]
            self.send_response(206); self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(status)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self._headers(rel, ctype)
        self.end_headers()
        if not head:
            self.wfile.write(data)

    def _static(self, head=False):
        path, _, query = self.path.partition("?")
        path = path.split("#", 1)[0]
        rel = path.lstrip("/")
        if ".." in rel or any(part.startswith(".") for part in rel.split("/")):
            return self._send("404.html", 404, head)
        if rel == "" or rel.endswith("/"):
            idx = os.path.join(rel, "index.html")
            if os.path.isfile(os.path.join(ROOT, idx)):
                return self._send(idx, head=head)
        elif os.path.isfile(os.path.join(ROOT, rel)):
            return self._send(rel, head=head)
        elif os.path.isfile(os.path.join(ROOT, rel, "index.html")):   # one direction only: /x -> /x/
            self.send_response(301)
            self.send_header("Location", "/" + rel + "/" + ("?" + query if query else ""))
            self.send_header("Content-Length", "0")
            return self.end_headers()
        return self._send("404.html", 404, head)

    def do_GET(self):
        self._static()

    def do_HEAD(self):
        self._static(head=True)

    def do_POST(self):
        self.send_response(405); self.send_header("Allow", "GET, HEAD"); self.send_header("Content-Length", "0"); self.end_headers()


if __name__ == "__main__":
    print(f"serving {ROOT} on :{PORT}", file=sys.stderr, flush=True)
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
