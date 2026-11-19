/* 암기노트 A4 인쇄판 배치기 — drive/chapter-engine/memorize.js
   #src 의 범위(div[data-title][data-ref]) → 범위마다 새 쪽 (첫 범위는 첫 쪽 목록 아래에서 시작).
   .unit(소제목 + 질문|답 표)은 자르지 않고, 한 쪽보다 길 때만 표의 행 경계에서 나눔 (머리 행 반복). */
// 웹 글꼴(본문·수식·코드)을 먼저 불러온 뒤 배치 — 늦게 불러오면 쪽 높이 계산이 어긋남
Promise.all(['16px "Pretendard Variable"', 'italic 500 16px "STIX Two Text"', '16px "JetBrains Mono"'].map(f => document.fonts.load(f, '가a1'))).catch(() => {}).then(() => document.fonts.ready).then(() => {
const B = document.body.dataset, src = document.getElementById('src'), root = document.getElementById('pages');
const NOTES = JSON.parse(document.getElementById('fn-data').textContent);
let page = 0;
function sheet(title){
  const s = document.createElement('section'); s.className = 'sheet mnote';
  s.innerHTML = '<div class="band"><span>암기노트 | ' + B.subject + '</span><span>' + title + '</span></div><div class="tab">암기</div>'
    + '<div class="body"></div><div class="fns"></div>'
    + '<div class="foot"><span>' + B.footL + '</span><span>암기 ' + (++page) + '</span><span>' + B.footR + '</span></div>';
  root.appendChild(s); return s;
}
function notes(s){
  const box = s.querySelector('.fns'); box.innerHTML = '';
  s.querySelectorAll('.body sup.fr').forEach(r => { const [k, t] = NOTES[r.dataset.fn]; const d = document.createElement('div');
    d.innerHTML = '<span class="n">[0]</span><span><span class="kd">' + k + '</span>' + t + '</span>'; box.appendChild(d); });
}
const over = s => { notes(s); const b = s.querySelector('.body'); return b.scrollHeight > b.clientHeight + 1; };
const toc = [];
const tocRows = () => { const tb = document.querySelector('.mhead tbody'); if (!tb) return;
  [...src.children].forEach(c => tb.insertAdjacentHTML('beforeend', '<tr class="toc-row"><td>' + c.dataset.title + '</td><td class="c">·</td><td class="c">' + c.dataset.ref + '</td></tr>')); };
let s = sheet('');
s.querySelector('.body').innerHTML = document.getElementById('cover-src').innerHTML;
tocRows();
[...src.children].forEach((rg, ri) => {
  if (ri > 0) s = sheet(rg.dataset.title); else s.querySelector('.band span:last-child').textContent = rg.dataset.title;
  toc.push({ t: rg.dataset.title, p: page, r: rg.dataset.ref });
  const head = rg.querySelector('.mrange'); s.querySelector('.body').appendChild(head);
  [...rg.querySelectorAll(':scope > .unit')].forEach(u => {
    let body = s.querySelector('.body'); body.appendChild(u);
    const lone = () => [...s.querySelector('.body').children].every(c => c === u || c.classList.contains('mrange') || c.classList.contains('mhead'));
    if (over(s) && !lone()) { u.remove(); s = sheet(rg.dataset.title); s.querySelector('.body').appendChild(u); }
    if (over(s)) {   // 한 쪽보다 긴 표: 행 경계에서 나눔
      const tb = u.querySelector('tbody'); const rows = [...tb.children]; tb.innerHTML = '';
      let curU = u, curTb = tb;
      rows.forEach(r => {
        curTb.appendChild(r);
        if (over(s)) { r.remove(); s = sheet(rg.dataset.title); curU = u.cloneNode(true); curU.querySelector('tbody').innerHTML = '';
          const h = curU.querySelector('h3'); if (h) h.insertAdjacentHTML('beforeend', ' <small style="font-weight:500;font-size:8.5pt;color:#5E5E5E">(이어짐)</small>');
          s.querySelector('.body').appendChild(curU); curTb = curU.querySelector('tbody'); curTb.appendChild(r); }
      });
    }
  });
});
// 마무리 점검: 글꼴이 늦게 적용돼 넘친 쪽이 있으면 마지막 묶음을 다음 쪽 맨 앞으로 넘김
for (let i = 0; i < root.children.length; i++) {
  const sh = root.children[i];
  while (over(sh)) {
    const units = [...sh.querySelectorAll('.body > .unit')]; if (units.length < 2) break;
    const last = units[units.length - 1];
    let nx = root.children[i + 1];
    const title = sh.querySelector('.band span:last-child').textContent;
    if (!nx || nx.querySelector('.band span:last-child').textContent !== title) {
      nx = sheet(title); if (root.children[i + 1] !== nx) root.insertBefore(nx, root.children[i + 1]);
    }
    const nb = nx.querySelector('.body'); nb.insertBefore(last, nb.firstChild);
  }
}
[...root.children].forEach((sh, i) => { sh.querySelector('.foot span:nth-child(2)').textContent = '암기 ' + (i + 1); });
page = root.children.length;
let num = 0;
document.querySelectorAll('.sheet').forEach(sh => { notes(sh); const ds = sh.querySelectorAll('.fns .n');
  sh.querySelectorAll('.body sup.fr').forEach((r, i) => { num++; r.textContent = '[' + num + ']'; ds[i].textContent = '[' + num + ']'; }); });
document.querySelectorAll('.toc-row').forEach((tr, i) => { if (toc[i]) tr.children[1].textContent = toc[i].p; });
document.getElementById('total').textContent = page + '쪽';
document.documentElement.dataset.ready = '1';
});
