const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const SITE_ORIGIN = 'https://m2rtecnologias.vercel.app';
const SITEMAP_PATH = path.join('frontend', 'sitemap.xml');
const CHECK_MODE = process.argv.includes('--check');

const formatPath = (route) => (route === '/' ? '/' : route.replace(/\/+$/, ''));

const destinationToFile = (destination) => {
    if (!destination.startsWith('/frontend/') || !destination.endsWith('.html')) {
        return null;
    }

    return destination.slice(1).replace(/\//g, path.sep);
};

const lastModifiedFor = (filePath) => {
    try {
        return execFileSync('git', ['log', '-1', '--format=%cs', '--', filePath], {
            encoding: 'utf8',
            stdio: ['ignore', 'pipe', 'ignore'],
        }).trim();
    } catch {
        return '';
    }
};

const buildSitemap = () => {
    const vercel = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    const routes = [];

    for (const rewrite of vercel.rewrites || []) {
        const source = formatPath(rewrite.source || '');
        const filePath = destinationToFile(rewrite.destination || '');

        if (!filePath || source === '/404') {
            continue;
        }

        if (!fs.existsSync(filePath)) {
            throw new Error(`Arquivo da rota ${source} nao encontrado: ${filePath}`);
        }

        const lastmod = lastModifiedFor(filePath);
        if (!lastmod && CHECK_MODE) {
            throw new Error(`Historico Git indisponivel para ${filePath}. Configure actions/checkout com fetch-depth: 0.`);
        }

        routes.push({
            loc: `${SITE_ORIGIN}${source === '/' ? '/' : source}`,
            lastmod: lastmod || new Date().toISOString().slice(0, 10),
        });
    }

    const urls = routes.map(({ loc, lastmod }) => [
        '  <url>',
        `    <loc>${loc}</loc>`,
        `    <lastmod>${lastmod}</lastmod>`,
        '  </url>',
    ].join('\n'));

    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ...urls,
        '</urlset>',
        '',
    ].join('\n');
};

const generated = buildSitemap();

if (CHECK_MODE) {
    const current = fs.readFileSync(SITEMAP_PATH, 'utf8');
    if (current.replace(/\r\n/g, '\n') !== generated.replace(/\r\n/g, '\n')) {
        throw new Error('frontend/sitemap.xml esta desatualizado. Rode: node tools/generate-sitemap.js');
    }
    console.log('sitemap atualizado');
} else {
    fs.writeFileSync(SITEMAP_PATH, generated, 'utf8');
    console.log(`sitemap gerado em ${SITEMAP_PATH}`);
}
