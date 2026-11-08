"""Run an informational Lighthouse audit of the locally served home page.

Usage: python tools/lighthouse_check.py
Requirements: npm ci --ignore-scripts; Chrome/Chromium installed.
"""
import json
import os
import shutil
import subprocess
import threading
from http.server import ThreadingHTTPServer

from site_tools import ROOT, Site, handler_for


LABELS = {
    'performance': 'Desempenho',
    'accessibility': 'Acessibilidade',
    'best-practices': 'Boas praticas',
    'seo': 'SEO',
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


def main():
    lighthouse = ROOT / 'node_modules' / '.bin' / 'lighthouse'
    if not lighthouse.is_file():
        raise SystemExit('Lighthouse ausente. Execute npm ci --ignore-scripts.')
    results = ROOT / 'test-results'
    results.mkdir(exist_ok=True)
    output = results / 'lighthouse-home.json'
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(Site()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        env = os.environ.copy()
        env['CHROME_PATH'] = find_chrome()
        command = [
            str(lighthouse), f'http://127.0.0.1:{server.server_port}/',
            '--quiet', '--output=json', f'--output-path={output}',
            '--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage',
        ]
        subprocess.run(command, cwd=ROOT, env=env, check=True, timeout=180)
        report = json.loads(output.read_text(encoding='utf-8'))
        print(f'Lighthouse: {summarize_lighthouse(report)}', flush=True)
        print(f'Relatorio JSON: {output.relative_to(ROOT)}', flush=True)
        print('Pontuacoes informativas: sem nota minima bloqueante.', flush=True)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
