// 축의지기 시안 자동 점검.
//   npm install  (playwright 설치)  →  npx playwright install chromium  →  npm run check
// 하는 일: 8개 화면을 노트북(1366×768, 1440×900)·휴대폰(400px) 폭으로 열어
//   1) 스크립트 오류가 없는지  2) 가로 스크롤이 없는지  3) 진행 화면이 한 화면에 들어가는지
//   4) 목록 → 등록 → 설정 → 요청 → 준비 → 진행 흐름이 이어지는지 확인하고, shots/ 폴더에 화면을 찍어 둔다.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

const ROOT = path.resolve(__dirname, '..', '..');
const SHOTS = path.join(__dirname, 'shots');
const url = (p) => pathToFileURL(path.join(ROOT, p)).href;
const PAGES = ['index.html', 'register/index.html', 'setup/index.html', 'request/index.html', 'guide/index.html', 'desk/index.html', 'status/index.html', 'result/index.html'];
let fails = 0;
const bad = (msg) => { fails++; console.log('  ✗', msg); };

(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch();

  // 1·2·3) 화면별 점검
  for (const [w, h] of [[1366, 768], [1440, 900], [400, 860]]) {
    console.log(`\n[${w}×${h}]`);
    for (const p of PAGES) {
      const page = await browser.newPage({ viewport: { width: w, height: h } });
      const errs = [];
      page.on('pageerror', (e) => errs.push(e.message));
      await page.goto(url(p)); await page.waitForLoadState('load'); await page.waitForTimeout(250);
      if (p.startsWith('desk')) { await page.keyboard.press('1'); await page.waitForTimeout(500); const ok = await page.$('#chgOk'); if (ok) await ok.click(); await page.waitForTimeout(150); }
      const sw = await page.evaluate(() => document.documentElement.scrollWidth);
      const over = await page.evaluate(() => { const x = document.querySelector('.work'); return x ? x.scrollHeight - x.clientHeight : 0; });
      const name = p.replace('/index.html', '').replace('.html', '');
      if (w === 1366) await page.screenshot({ path: path.join(SHOTS, `${name}.png`) });
      let line = `  ${name.padEnd(9)} 가로 ${sw}`;
      if (sw > w) bad(`${name}: 가로 스크롤 (${sw} > ${w})`);
      if (errs.length) bad(`${name}: 스크립트 오류 ${errs.join(' | ')}`);
      if (name === 'desk' && w >= 1366 && over > 0) bad(`desk: 한 화면에 안 들어감 (${over}px 넘침)`);
      if (sw <= w && !errs.length) console.log(line + ' · 오류 없음');
      await page.close();
    }
  }

  // 4) 흐름 점검
  console.log('\n[흐름]');
  const p = await browser.newPage({ viewport: { width: 1366, height: 768 } });
  const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  const where = () => p.url().split('/').slice(-2).join('/');
  await p.goto(url('index.html')); await p.waitForLoadState('load');
  await p.click('.navitem[href="register/index.html"]'); await p.waitForLoadState('load');
  await p.fill('#rMail', 'a@b.c'); await p.check('#rAgree'); await p.click('#reqForm .save'); await p.click('#modal a.save'); await p.waitForLoadState('load'); await p.waitForTimeout(150);
  console.log('  등록 → ' + where());
  await p.click('[data-add="B"]'); await p.keyboard.type('최유리'); await p.click('.tbd[data-f="tkB"]'); await p.fill('#tkB', '180'); await p.click('.tbd[data-f="spot"]'); await p.fill('#spot', '영빈관 1층');
  console.log('  설정 체크 → ' + await p.textContent('#readyPill') + ' / 결제 버튼 ' + (await p.isDisabled('#payBtn') ? '잠김' : '열림'));
  await p.click('a[href="../request/index.html"]'); await p.waitForLoadState('load'); console.log('  설정 → ' + where());
  await p.click('.closing a.save'); await p.waitForLoadState('load'); console.log('  요청 → ' + where());
  await p.click('.work .save[href="../desk/index.html"]'); await p.waitForLoadState('load'); await p.waitForTimeout(200); console.log('  준비 → ' + where());
  await p.keyboard.press('1'); await p.waitForTimeout(600);
  if (!(await p.isVisible('#scrim'))) bad('진행: 변동 안내가 자동으로 뜨지 않음');
  await p.click('#chgOk'); await p.waitForTimeout(150);
  await p.keyboard.type('김하객'); await p.keyboard.press('Tab'); await p.keyboard.type('5'); await p.keyboard.press('Equal'); await p.keyboard.press('Enter'); await p.waitForTimeout(200);
  const toast = await p.textContent('#toast'); console.log('  저장 → ' + toast);
  if (!/저장됨/.test(toast)) bad('진행: 저장 알림이 없음');
  // Tab: 성함 → 금액 → 식권 → 저장, 저장에서 Tab은 머묾, Enter = 저장
  await p.waitForTimeout(100); await p.focus('#name'); await p.keyboard.type('나탭키'); await p.keyboard.press('Tab'); await p.keyboard.type('3'); await p.keyboard.press('Tab'); await p.keyboard.press('Tab');
  const f1 = await p.evaluate(() => document.activeElement.id); await p.keyboard.press('Tab'); const f2 = await p.evaluate(() => document.activeElement.id);
  await p.keyboard.press('Enter'); await p.waitForTimeout(200); const t2 = await p.textContent('#toast');
  console.log('  Tab → ' + f1 + ' → ' + f2 + ' / Enter → ' + t2);
  if (f1 !== 'saveBtn' || f2 !== 'saveBtn' || !/14번 저장됨/.test(t2)) bad('진행: Tab으로 저장 버튼에 가서 Enter 저장이 안 됨');
  if (!/[0-9]/.test(await p.textContent('#stCash'))) bad('진행: 위쪽 현금 합계가 안 보임');
  await p.click('#toSettle'); await p.fill('#d0', '17'); await p.fill('#left', '186'); await p.waitForTimeout(100);
  console.log('  정산 → ' + await p.textContent('#cVerdict') + ' / ' + await p.textContent('#tVerdict'));
  await p.fill('#ckA', '10'); await p.waitForTimeout(100);
  console.log('  수표 10만 원 → ' + await p.textContent('#cCounted'));
  // 축의대 용품 팝업 · 현황 구분 스위치
  await p.goto(url('setup/index.html')); await p.click('[data-shop]'); await p.waitForTimeout(150);
  const prods = await p.$$eval('.prod', (x) => x.length); await p.click('.prod [data-q="4"]'); await p.waitForTimeout(100);
  console.log('  용품 → ' + prods + '개 · ' + (await p.textContent('#shopSum')).trim());
  if (prods !== 7) bad('용품: 7개가 아님');
  await p.screenshot({ path: path.join(SHOTS, 'shop.png') });
  await p.goto(url('status/index.html')); await p.click('#viewTabs [data-v="bride"]'); await p.waitForTimeout(100);
  const gHidden = await p.$eval('#cardG', (x) => x.hidden); const feedSides = await p.$$eval('#feed .sd', (x) => [...new Set(x.map((e) => e.textContent))].join(','));
  console.log('  현황 신부측 → 신랑 카드 숨김 ' + gHidden + ' · 목록 ' + feedSides);
  if (!gHidden || feedSides !== '신부측') bad('현황: 신부측만 보기가 안 됨');
  if (errs.length) bad('흐름 중 스크립트 오류: ' + errs.join(' | '));
  await browser.close();

  console.log(fails ? `\n실패 ${fails}건` : '\n모두 통과');
  process.exit(fails ? 1 : 0);
})();
