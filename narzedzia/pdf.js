// Generuje PDF-y z wersji do druku (Chromium/Playwright).
// Użycie: node narzedzia/pdf.js [katalog_wyjściowy]
// Bez argumentu zapisuje do materialy/pdf/.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const out = path.resolve(process.argv[2] || path.join(root, 'materialy', 'pdf'));

// Źródło HTML → nazwa PDF.
const jobs = [];
for (const f of fs.readdirSync(path.join(root, 'materialy', 'druk'))) {
  if (f.endsWith('.html')) jobs.push([`materialy/druk/${f}`, f.replace(/\.html$/, '.pdf')]);
}
for (const f of fs.readdirSync(path.join(root, 'materialy', 'arkusze'))) {
  if (f.endsWith('.html')) jobs.push([`materialy/arkusze/${f}`, `arkusze-${f.replace(/-wzory\.html$/, '').replace(/^wszystkie-arkusze\.html$/, 'wszystkie')}.pdf`]);
}
for (const f of fs.readdirSync(path.join(root, 'materialy', 'ankiety'))) {
  if (f.endsWith('.html')) jobs.push([`materialy/ankiety/${f}`, f.replace(/\.html$/, '.pdf')]);
}
jobs.push(['materialy/specyfikacja-grafik-dobowy.html', 'specyfikacja-grafik-dobowy.pdf']);
for (let i = 1; i <= 6; i++) jobs.push([`modul-${i}.html`, `scenariusz-modul-${i}.pdf`]);
jobs.push(['prowadzacy.html', 'przewodnik-prowadzacego.pdf']);
jobs.push(['uczestnik.html', 'informacje-dla-uczestnikow.pdf']);
jobs.push(['ewaluacja.html', 'ewaluacja-programu.pdf']);
jobs.push(['bibliografia.html', 'bibliografia.pdf']);
for (const p of (process.env.EXTRA_PAGES || '').split(',').filter(Boolean)) {
  const [src, dst] = p.split(':');
  jobs.push([src, dst]);
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch(fs.existsSync('/opt/pw-browsers/chromium')
    ? { executablePath: '/opt/pw-browsers/chromium' } : {});
  const page = await browser.newPage();
  for (const [src, dst] of jobs) {
    const file = path.join(root, src);
    if (!fs.existsSync(file)) continue;
    await page.goto('file://' + file, { waitUntil: 'networkidle' });
    await page.emulateMedia({ media: 'print' });
    await page.pdf({
      path: path.join(out, dst),
      format: 'A4',
      preferCSSPageSize: true,
      printBackground: true,
      margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
    });
    console.log(`${src} -> ${dst}`);
  }
  await browser.close();
})();
