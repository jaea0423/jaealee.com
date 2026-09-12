// Render the existing website, pinning its data request to the saved edition.
const fs = require('node:fs');
const path = require('node:path');

async function capture(input) {
  const {chromium} = require(input.playwright);
  const browser = await chromium.launch({executablePath: input.chrome, headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}, deviceScaleFactor: 2});
    const {kind, day, data} = input;
    await page.route(`**/${kind}/data/*.json*`, route => {
      const requested = new URL(route.request().url()).pathname;
      if (requested !== `/${kind}/data/${day}.json`) return route.fulfill({status: 404, body: ''});
      return route.fulfill({json: data});
    });
    await page.goto(`https://jaealee.com/home/#${kind}/${day}`, {waitUntil: 'networkidle', timeout: 60000});
    const selector = kind === 'news' ? '.news-section' : '.knowledge-article';
    await page.locator(selector).first().waitFor();
    await page.addStyleTag({content: '.news-controls {display:none !important} .site-header, .utility-row {visibility:hidden !important}'});
    await page.evaluate(async () => {
      document.querySelectorAll('#news-content details').forEach(el => el.open = true);
      document.querySelectorAll('.news-keyword-description').forEach(el => el.hidden = false);
      document.querySelectorAll('.news-keyword-list button').forEach(el => el.setAttribute('aria-expanded', 'true'));
      await document.fonts.ready;
      window.scrollTo(0, 0);
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    });
    const panel = page.locator(`#panel-${kind}`);
    const text = await panel.innerText();
    const expected = [];
    if (kind === 'news') {
      if (await page.locator('#paper-date').innerText() !== day) throw Error('Wrong edition');
      for (const section of data.sections) {
        expected.push(section.labelKr, section.desc);
        for (const card of section.cards || []) expected.push(card.title, card.summary, card.source);
        for (const keyword of section.keywords || []) expected.push(keyword.word, keyword.desc);
        if (section.forYou) expected.push(section.forYou.sub, section.forYou.body);
      }
      expected.push(data.market?.note, data.market?.oneliner);
      for (const tile of data.market?.tiles || []) expected.push(tile.name, tile.value, tile.change, tile.fx, tile.asof);
    } else {
      if (await page.locator('#knowledge-edition').innerText() !== day.replaceAll('-', '.')) throw Error('Wrong edition');
      for (const article of data.articles) {
        expected.push(article.label, article.title, article.quote || article.summary, article.attribution || article.author, article.takeaway);
        for (const block of article.blocks || []) {
          expected.push(block.text, block.caption);
          if (block.type === 'table') expected.push(...block.headers, ...block.rows.flat());
          if (block.type === 'fraction') expected.push(block.numerator, block.denominator, block.result);
        }
        for (const source of article.sources || []) expected.push(source.title);
      }
    }
    const normalize = value => String(value).replace(/\s+/g, ' ').trim();
    if (expected.filter(Boolean).some(value => !normalize(text).includes(normalize(value)))) throw Error('Missing rendered text');
    const overflow = await panel.evaluate(el => [...el.querySelectorAll('p,td,h3,h4,math')].some(x => x.scrollWidth > x.clientWidth + 2));
    if (overflow) throw Error('Clipped content');
    const box = await panel.boundingBox();
    const clips = [];
    if (kind === 'news') {
      const sections = page.locator('.news-section');
      if (await sections.count() !== 5) throw Error('Expected five news sections');
      const starts = [box.y];
      for (let i = 0; i < 5; i++) starts.push((await sections.nth(i).boundingBox()).y - 20);
      starts.push(box.y + box.height);
      for (let i = 0; i < 6; i++) clips.push({x: box.x, y: starts[i], width: box.width, height: starts[i + 1] - starts[i]});
    } else {
      if (await page.locator('.knowledge-article').count() !== 3) throw Error('Expected three knowledge sections');
      for (const section of ['basic', 'deep', 'sentence']) {
        const rect = await page.locator(`#knowledge-${section}`).boundingBox();
        clips.push({x: box.x, y: rect.y, width: box.width, height: rect.height});
      }
    }
    for (let i = 0; i < clips.length; i++) {
      await page.screenshot({path: path.join(input.folder, `${day}-${kind}-${i + 1}.png`), fullPage: true, clip: clips[i], animations: 'disabled'});
    }
    console.log(JSON.stringify({count: clips.length}));
  } finally {
    await browser.close();
  }
}

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => raw += chunk);
process.stdin.on('end', () => capture(JSON.parse(raw)).catch(() => {
  console.error('Digest capture failed');
  process.exitCode = 1;
}));
