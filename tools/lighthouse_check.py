"""Run an informational Lighthouse audit of the locally served home page.

Usage: python tools/lighthouse_check.py
Requirements: npm ci --ignore-scripts; Chrome/Chromium installed.
"""
import argparse
import json
import os
import shutil
import subprocess
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from site_tools import ROOT, Site, handler_for


LABELS = {
    'performance': 'Desempenho',
    'accessibility': 'Acessibilidade',
    'best-practices': 'Boas praticas',
    'seo': 'SEO',
}
ALLOWED_ROUTES = ('/', '/servicos', '/contato')


def lighthouse_output_name(route, device):
    if route not in ALLOWED_ROUTES:
        raise ValueError(f'Rota Lighthouse nao suportada: {route}')
    if device not in ('mobile', 'desktop'):
        raise ValueError(f'Dispositivo Lighthouse invalido: {device}')
    slug = 'home' if route == '/' else route.strip('/').replace('/', '-')
    return f'lighthouse-{slug}-{device}.json'


def extract_lab_metrics(report):
    audits = report.get('audits', {}) if isinstance(report, dict) else {}
    lcp = audits.get('largest-contentful-paint', {})
    cls = audits.get('cumulative-layout-shift', {})
    inp = audits.get('interaction-to-next-paint', {})
    return {
        'lcp': lcp.get('displayValue') or 'indisponível',
        'cls': cls.get('displayValue') or 'indisponível',
        'inp': inp.get('displayValue') or 'indisponível (laboratório sem interação)',
    }


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


def main(argv=None):
    parser = argparse.ArgumentParser(description='Executa auditoria laboratorial Lighthouse.')
    parser.add_argument('--routes', nargs='+', help='Rotas a auditar (/, /servicos, /contato)')
    parser.add_argument('--device', choices=('mobile', 'desktop'), default='mobile')
    parser.add_argument('--output-dir', help='Diretorio de saida para os JSONs')
    args = parser.parse_args(argv)

    lighthouse = ROOT / 'node_modules' / '.bin' / 'lighthouse'
    if not lighthouse.is_file():
        raise SystemExit('Lighthouse ausente. Execute npm ci --ignore-scripts.')

    custom_mode = bool(args.routes or args.output_dir or args.device != 'mobile')
    routes = tuple(args.routes) if args.routes else ('/',)
    for route in routes:
        if route not in ALLOWED_ROUTES:
            raise SystemExit(f'Rota nao suportada: {route}')

    out_dir = Path(args.output_dir) if args.output_dir else (ROOT / 'test-results')
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(Site()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        env = os.environ.copy()
        env['CHROME_PATH'] = find_chrome()
        for route in routes:
            filename = lighthouse_output_name(route, args.device) if custom_mode else 'lighthouse-home.json'
            output = out_dir / filename
            command = [
                str(lighthouse), f'http://127.0.0.1:{server.server_port}{route}',
                '--quiet', '--output=json', f'--output-path={output}',
                '--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage',
            ]
            if args.device == 'desktop':
                command.append('--preset=desktop')
            subprocess.run(command, cwd=ROOT, env=env, check=True, timeout=180)
            report = json.loads(output.read_text(encoding='utf-8'))
            metrics = extract_lab_metrics(report)
            print(f'Lighthouse ({route} [{args.device}]): {summarize_lighthouse(report)}', flush=True)
            print(
                f"Metricas de laboratorio ({route} [{args.device}]): "
                f"LCP={metrics['lcp']} | CLS={metrics['cls']} | INP={metrics['inp']}",
                flush=True,
            )
            print(f'Relatorio JSON: {output.relative_to(ROOT)}', flush=True)
        print('Pontuacoes informativas (laboratorio): sem nota minima bloqueante; CWV de campo indisponivel.', flush=True)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
