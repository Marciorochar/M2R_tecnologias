"""Local routing and validation for the static rules in vercel.json."""
import argparse
import base64
import hashlib
import json
import mimetypes
import re
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://m2rtecnologias.vercel.app"


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.scripts = [], set(), []
        self.script = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get("srcset"):
            self.links.extend(item.strip().split()[0] for item in attrs["srcset"].split(",") if item.strip())
        if tag == "script" and not attrs.get("src"):
            self.script = [attrs.get("type", ""), ""]

    def handle_data(self, data):
        if self.script is not None:
            self.script[1] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None


class Site:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.config = json.loads((self.root / "vercel.json").read_text(encoding="utf-8"))

    @staticmethod
    def match(rule, pathname):
        source = rule["source"]
        if source.endswith("(.*)"):
            prefix = source[:-4]
            if pathname.startswith(prefix):
                return rule["destination"].replace("$1", pathname[len(prefix):])
        elif source == pathname:
            return rule["destination"]
        return None

    def redirect(self, pathname):
        for rule in self.config.get("redirects", []):
            destination = self.match(rule, pathname)
            if destination is not None:
                return destination, 308 if rule.get("permanent") else 307
        return None

    def file(self, pathname):
        pathname = unquote(pathname)
        for rule in self.config["rewrites"]:
            destination = self.match(rule, pathname)
            if destination is not None:
                target = (self.root / destination.lstrip("/")).resolve()
                if target.is_relative_to(self.root / "frontend") and target.is_file():
                    return target
                return None
        return None

    def resolve(self, url):
        seen = set()
        while url not in seen:
            seen.add(url)
            parsed = urlsplit(url)
            if parsed.scheme not in ("http", "https") or parsed.netloc != urlsplit(ORIGIN).netloc:
                return None, None
            redirect = self.redirect(parsed.path)
            if not redirect:
                return self.file(parsed.path), unquote(parsed.fragment)
            target = urljoin(url, redirect[0])
            if "#" not in redirect[0] and parsed.fragment:
                target += "#" + parsed.fragment
            url = target
        raise ValueError(f"Ciclo de redirects: {url}")

    def check_link(self, reference, public_url):
        url = urljoin(public_url, reference)
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or parsed.netloc != urlsplit(ORIGIN).netloc:
            return
        file, fragment = self.resolve(url)
        if not file:
            raise ValueError(f"Destino inexistente: {url}")
        if fragment and file.suffix == ".html":
            if fragment not in Document(file.read_text(encoding="utf-8")).ids:
                raise ValueError(f"Fragmento inexistente: {url}")

    def check(self):
        count = 0
        for rule in self.config["rewrites"]:
            if "(.*)" in rule["source"]:
                directory = self.root / rule["destination"].split("$1")[0].lstrip("/")
                if not directory.is_dir():
                    raise ValueError(f"Diretorio inexistente: {directory}")
                continue
            file = self.file(rule["source"])
            if not file:
                raise ValueError(f"Rewrite sem arquivo: {rule}")
            if file.suffix == ".html":
                for reference in Document(file.read_text(encoding="utf-8")).links:
                    self.check_link(reference, ORIGIN + rule["source"])
                count += 1
        for rule in self.config.get("redirects", []):
            self.check_link(rule["source"], ORIGIN)
        for file in (self.root / "frontend/assets").rglob("*.css"):
            public_url = ORIGIN + "/" + file.relative_to(self.root / "frontend").as_posix()
            for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", file.read_text(encoding="utf-8")):
                self.check_link(match[1].strip(), public_url)
        error_document = Document((self.root / "404.html").read_text(encoding="utf-8"))
        for reference in error_document.links:
            if reference.startswith("#"):
                if unquote(reference[1:]) not in error_document.ids:
                    raise ValueError(f"Fragmento inexistente na pagina 404: {reference}")
            else:
                self.check_link(reference, ORIGIN + "/missing/nested/path")
        print(f"Links, assets, fragments e destinos OK: {count} paginas")

    def security(self, write=False):
        inline_count = 0
        for file in (self.root / "frontend").rglob("*.html"):
            for kind, content in Document(file.read_text(encoding="utf-8")).scripts:
                if kind != "application/ld+json":
                    raise ValueError(f"Script executavel inline: {file}")
                json.loads(content)
                inline_count += 1
        csp_groups = 0
        for group in self.config.get("headers", []):
            for header in group["headers"]:
                if header["key"] != "Content-Security-Policy":
                    continue
                csp_groups += 1
                directives = {}
                for item in header["value"].split(";"):
                    parts = item.strip().split()
                    if parts: directives[parts[0].lower()] = {token.lower() for token in parts[1:]}
                if "script-src" not in directives: raise ValueError("CSP deve definir script-src")
                for name in ("script-src", "script-src-elem", "script-src-attr"):
                    if "'unsafe-inline'" in directives.get(name, set()): raise ValueError(f"CSP nao pode permitir unsafe-inline em {name}")
        if not csp_groups: raise ValueError("Content-Security-Policy ausente nos headers")
        print(f"CSP e JSON-LD OK: {inline_count} blocos estruturados")


def handler_for(site):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond()

        def do_HEAD(self):
            self.respond(head=True)

        def respond(self, head=False):
            parsed = urlsplit(self.path)
            redirect = site.redirect(parsed.path)
            if redirect:
                self.send_response(redirect[1])
                self.send_header("Location", redirect[0] + ("?" + parsed.query if parsed.query else ""))
                self.end_headers()
                return
            file = site.file(parsed.path)
            self.send_response(200 if file else 404)
            file = file or site.root / "404.html"
            data = file.read_bytes()
            self.send_header("Content-Type", mimetypes.guess_type(file.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            headers = {}
            for group in site.config["headers"]:
                if site.match({"source": group["source"], "destination": "match"}, parsed.path):
                    headers.update({item["key"]: item["value"] for item in group["headers"]})
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()
            if not head:
                self.wfile.write(data)
    return Handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check", "serve", "security"])
    parser.add_argument("--port", type=int, default=5500)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    site = Site()
    if args.command == "check":
        site.check()
    elif args.command == "security":
        site.security(args.write)
    else:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(site))
        print(f"Frontend local: http://127.0.0.1:{args.port}/", flush=True)
        server.serve_forever()
