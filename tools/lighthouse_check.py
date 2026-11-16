"""Run informational Lighthouse audits of locally served M2R routes.

Usage: python tools/lighthouse_check.py [--routes / /servicos /contato] [--device mobile|desktop]
Requirements: npm ci --ignore-scripts; Chrome/Chromium installed.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
import sys

from site_tools import ROOT, Site, handler_for


LABELS = {
    'performance': 'Desempenho',
    'accessibility': 'Acessibilidade',
    'best-practices': 'Boas praticas',
    'seo': 'SEO',
}
KNOWN_ROUTES = ('/', '/servicos', '/contato')
ROUTE_SLUGS = {'/': 'home', '/servicos': 'servicos', '/contato': 'contato'}


def lighthouse_binary_path(root=ROOT, windows=None):
    """Resolve the platform-specific npm shim for Lighthouse."""
    if windows is None:
        windows = os.name == 'nt'
    binary = Path(root) / 'node_modules' / '.bin' / 'lighthouse'
    return binary.with_name('lighthouse.cmd') if windows else binary


def validate_routes(routes):
    """Return known routes in input order or reject unknown/duplicate paths."""
    routes = list(routes)
    unknown = [route for route in routes if route not in ROUTE_SLUGS]
    if unknown:
        raise ValueError('Rota Lighthouse desconhecida: ' + ', '.join(unknown))
    if len(routes) != len(set(routes)):
        raise ValueError('Rotas Lighthouse duplicadas')
    if not routes:
        raise ValueError('Informe pelo menos uma rota')
    return routes


def lighthouse_output_path(output_dir, route, device, legacy_default=False):
    """Select a stable report path; preserve the no-argument CI filename."""
    if route not in ROUTE_SLUGS:
        raise ValueError(f'Rota Lighthouse desconhecida: {route}')
    if device not in ('mobile', 'desktop'):
        raise ValueError(f'Perfil Lighthouse invalido: {device}')
    output_dir = Path(output_dir)
    filename = 'lighthouse-home.json' if legacy_default else f'{ROUTE_SLUGS[route]}-{device}.json'
    return output_dir / filename


def extract_lab_metrics(report):
    """Read laboratory audit values only when Lighthouse provides numeric values."""
    audits = report.get('audits', {}) if isinstance(report, dict) else {}

    def numeric_value(audit_id):
        audit = audits.get(audit_id) if isinstance(audits, dict) else None
        value = audit.get('numericValue') if isinstance(audit, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return None
        return value

    return {
        'lcp_ms': numeric_value('largest-contentful-paint'),
        'cls': numeric_value('cumulative-layout-shift'),
        'inp_ms': numeric_value('interaction-to-next-paint'),
    }


def format_lab_metrics(metrics):
    """Render lab-only metrics, marking absent values as unavailable."""
    def fmt(key, unit=''):
        value = metrics[key]
        return 'indisponível' if value is None else f'{value:g}{unit}'

    return f"LCP: {fmt('lcp_ms', ' ms')} | CLS: {fmt('cls')} | INP: {fmt('inp_ms', ' ms')}"


def summarize_lighthouse(report):
    """Summarize four scores; fail for missing or malformed categories only."""
    categories = report.get('categories', {})
    summary = []
    for category, label in LABELS.items():
        item = categories.get(category)
        score = item.get('score') if isinstance(item, dict) else None
        if isinstance(score, bool) or not isinstance(score, (float, int)) or not 0 <= score <= 1:
            raise ValueError(f'Lighthouse retornou nota ausente ou invalida para {category}')
        summary.append(f'{label}: {round(score * 100)}/100')
    return ' | '.join(summary)


def find_chrome():
    explicit = os.environ.get('CHROME_PATH')
    if explicit:
        return explicit
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            candidate = playwright.chromium.executable_path
            if os.path.isfile(candidate):
                return candidate
    except ImportError:
        pass
    for name in ('chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable'):
        candidate = shutil.which(name)
        if candidate:
            return candidate
    raise RuntimeError('Chromium nao encontrado. Instale via Playwright ou configure CHROME_PATH.')


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--routes', nargs='+', default=['/'], metavar='ROUTE')
    parser.add_argument('--device', choices=('mobile', 'desktop'), default='mobile')
    parser.add_argument('--output-dir', type=Path)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        routes = validate_routes(args.routes)
    except ValueError as error:
        parser.error(str(error))
    lighthouse = lighthouse_binary_path()
    if not lighthouse.is_file():
        raise SystemExit('Lighthouse ausente. Execute npm ci --ignore-scripts.')
    default_invocation = argv is None and len(sys.argv) == 1
    results = ROOT / (args.output_dir if args.output_dir else 'test-results')
    results.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(Site()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        env = os.environ.copy()
        env['CHROME_PATH'] = find_chrome()
        for route in routes:
            output = lighthouse_output_path(results, route, args.device, legacy_default=default_invocation)
            command = [
                str(lighthouse), f'http://127.0.0.1:{server.server_port}{route}',
                '--quiet', '--output=json', f'--output-path={output}',
                '--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage',
            ]
            if args.device == 'desktop':
                command.append('--preset=desktop')
            else:
                command.append('--form-factor=mobile')
            subprocess.run(command, cwd=ROOT, env=env, check=True, timeout=180)
            report = json.loads(output.read_text(encoding='utf-8'))
            print(f'Lighthouse ({args.device} {route}): {summarize_lighthouse(report)}', flush=True)
            print(f'Métricas de laboratório: {format_lab_metrics(extract_lab_metrics(report))}', flush=True)
            print(f'Relatório JSON: {output.relative_to(ROOT)}', flush=True)
        print('Pontuacoes informativas: sem nota minima bloqueante.', flush=True)
        print('Dados de laboratório; métricas de campo (CrUX/RUM) não incluídas.', flush=True)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
