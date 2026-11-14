const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const CHECK_MODE = process.argv.includes('--check');
const ROOT = path.resolve(__dirname, '..');
const ASSETS = [
    ['style.css', path.join(ROOT, 'frontend', 'assets', 'css', 'style.css')],
    ['script.js', path.join(ROOT, 'frontend', 'assets', 'js', 'script.js')],
    ['hero-circuits.js', path.join(ROOT, 'frontend', 'assets', 'js', 'hero-circuits.js')],
    ['internal-hero.css', path.join(ROOT, 'frontend', 'assets', 'css', 'internal-hero.css')],
    ['internal-hero.js', path.join(ROOT, 'frontend', 'assets', 'js', 'internal-hero.js')],
];

const walkHtml = (directory) => fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) return walkHtml(fullPath);
    return entry.isFile() && entry.name.endsWith('.html') ? [fullPath] : [];
});

const htmlFiles = [...walkHtml(path.join(ROOT, 'frontend')), path.join(ROOT, '404.html')];
let stale = false;

for (const [name, assetPath] of ASSETS) {
    // Git may materialize text assets with CRLF on Windows and LF on Linux.
    // Hash canonical UTF-8 text so generated URLs are identical on every runner.
    const source = fs.readFileSync(assetPath, 'utf8').replace(/\r\n?/g, '\n');
    const hash = crypto.createHash('sha256').update(source, 'utf8').digest('hex').slice(0, 10);
    const pattern = new RegExp(`${name.replace('.', '\\.')}(?:\\?v=[A-Za-z0-9._-]+)?`, 'g');
    for (const htmlPath of htmlFiles) {
        const current = fs.readFileSync(htmlPath, 'utf8');
        if (!current.includes(name)) continue;
        const updated = current.replace(pattern, `${name}?v=${hash}`);
        if (updated !== current) {
            stale = true;
            if (!CHECK_MODE) fs.writeFileSync(htmlPath, updated, 'utf8');
        }
    }
}

if (CHECK_MODE && stale) {
    throw new Error('Referencias de CSS ou JavaScript estao sem o hash de conteudo atual. Rode: node tools/version-assets.js');
}

console.log(CHECK_MODE ? 'versoes dos assets atualizadas' : 'versoes dos assets geradas');
