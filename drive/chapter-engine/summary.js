/* 정리노트 A4 인쇄판 배치기 — drive/chapter-engine/summary.js
   개념노트(chapter.js)와 같은 부품을 쓰되: 2단, 검은 띠 머리말, 오른쪽 탭, 첫 쪽 위쪽에 제목·목차, 쪽 번호 "정리 n".
   #src 의 장(div[data-title][data-ref]) 안 .unit 을 단 단위로 배치 — unit 은 단 하나 안에 들어가야 하며 자르지 않는다. */
document.fonts.ready.then(() => {
const B = document.body.dataset, src = document.getElementById('src'), root = document.getElementById('pages');
const NOTES = JSON.parse(document.getElementById('fn-data').textContent);
let page = 0;
function sheet(chap){
  const s = document.createElement('section'); s.className = 'sheet snote';
  s.innerHTML = '<div class="band"><span>정리노트 | ' + B.unit + '</span><span>' + chap + '</span></div><div class="tab">정리</div>'
    + '<div class="body"><div class="cols"></div></div><div class="fns"></div>'
    + '<div class="foot"><span>' + B.footL + '</span><span>정리 ' + (++page) + '</span><span>' + B.footR + '</span></div>';
  root.appendChild(s); return s;
}
function notes(s){
  const box = s.querySelector('.fns'); box.innerHTML = '';
  s.querySelectorAll('.body sup.fr').forEach(r => { const [k, t] = NOTES[r.dataset.fn]; const d = document.createElement('div');
    d.innerHTML = '<span class="n">[0]</span><span><span class="kd">' + k + '</span>' + t + '</span>'; box.appendChild(d); });
}
const over = s => { notes(s); const c = s.querySelector('.cols'); return c.scrollWidth > c.clientWidth + 1 || c.scrollHeight > c.clientHeight + 1; };
const toc = [];
let s = sheet('');
s.querySelector('.body').insertAdjacentHTML('afterbegin', document.getElementById('cover-src').innerHTML);
[...src.children].forEach(ch => {
  const units = [...ch.querySelectorAll(':scope > .unit')];
  units.forEach((u, i) => {
    let cols = s.querySelector('.cols'); cols.appendChild(u);
    if (over(s) && cols.children.length > 1) { u.remove(); s = sheet(ch.dataset.title); s.querySelector('.cols').appendChild(u); }
    if (i === 0) toc.push({ t: ch.dataset.title, p: page, r: ch.dataset.ref });
    if (!s.querySelector('.band span:last-child').textContent) s.querySelector('.band span:last-child').textContent = ch.dataset.title;
  });
});
let num = 0;
document.querySelectorAll('.sheet').forEach(sh => { notes(sh); const ds = sh.querySelectorAll('.fns .n');
  sh.querySelectorAll('.body sup.fr').forEach((r, i) => { num++; r.textContent = '[' + num + ']'; ds[i].textContent = '[' + num + ']'; }); });
const tb = document.querySelector('.shead tbody');
toc.forEach(e => tb.insertAdjacentHTML('beforeend', '<tr><td>' + e.t + '</td><td class="c">' + e.p + '</td><td class="c">' + e.r + '</td></tr>'));
document.getElementById('total').textContent = page + '쪽';
document.documentElement.dataset.ready = '1';
});
