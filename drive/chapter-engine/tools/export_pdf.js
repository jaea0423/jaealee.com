// 단원 정리 HTML → 같은 폴더에 PDF 저장.  사용: node export_pdf.js <html 경로>
// 화면 배치(chapter.js)가 끝난 뒤 A4 로 인쇄하므로 화면과 PDF 쪽 나눔이 같다.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const html = path.resolve(process.argv[2]);
  const b = await chromium.launch(); const pg = await b.newPage();
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('file://' + html);
  await pg.waitForFunction(() => document.documentElement.dataset.ready === '1', null, { timeout: 30000 });
  const bad = await pg.evaluate(() => [...document.querySelectorAll('.sheet')].map((s, i) => { const b = s.querySelector('.body'); return b.scrollHeight - b.clientHeight > 1 ? i + 1 : 0; }).filter(Boolean));
  if (bad.length) console.log('넘침 쪽:', bad.join(', '));
  const out = html.replace(/\.html$/, '.pdf');
  await pg.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  console.log('PDF', out, await pg.evaluate(() => document.querySelectorAll('.sheet').length) + '쪽');
  await b.close();
})();
