/* 단원 정리 A4 인쇄판 공통 배치기 — drive/chapter-engine/chapter.js
   #src 의 장(div[data-title]) → 쪽(.sheet) 으로 자동 배치, 각주 번호, 표지 목차 */
document.fonts.ready.then(() => {
const src = document.getElementById('src'), root = document.getElementById('pages');
const NOTES = JSON.parse(document.getElementById('fn-data').textContent);
let page = 0;
function sheet(chap){
  const s = document.createElement('section'); s.className = 'sheet';
  s.innerHTML = '<div class="run"><span>' + document.body.dataset.run + '</span><span>' + chap + '</span></div><div class="body"></div><div class="fns"></div><div class="foot"><span>' + document.body.dataset.footL + '</span><span>' + (++page) + '</span><span>' + document.body.dataset.footR + '</span></div>';
  root.appendChild(s); return s;
}
function notes(s){
  const box = s.querySelector('.fns'); box.innerHTML = '';
  s.querySelectorAll('.body sup.fr').forEach(r => {
    const [kind, text] = NOTES[r.dataset.fn]; const d = document.createElement('div');
    d.innerHTML = '<span class="n">[0]</span><span><span class="kd">' + kind + '</span>' + text + '</span>'; box.appendChild(d);
  });
}
const over = s => { notes(s); const b = s.querySelector('.body'); return b.scrollHeight > b.clientHeight + 1; };
const empty = s => [...s.querySelector('.body').children].every(c => c.tagName === 'H2');
const toc = [];
const cover = sheet('표지'); cover.querySelector('.run').style.visibility = 'hidden';
cover.querySelector('.body').innerHTML = document.getElementById('cover-src').innerHTML;
[...src.children].forEach(ch => {
  let s = sheet(ch.dataset.title);
  const entry = { t: ch.dataset.title, p: page, subs: [] }; toc.push(entry);
  s.querySelector('.body').appendChild(ch.querySelector('h2'));
  [...ch.querySelectorAll(':scope > .unit')].forEach(u => {
    const h = u.querySelector('h3');
    let body = s.querySelector('.body'); body.appendChild(u);
    if (over(s) && !empty(s)) { u.remove(); s = sheet(ch.dataset.title); body = s.querySelector('.body'); body.appendChild(u); }
    if (over(s)) {
      // 한 쪽보다 긴 내용: 블록 경계에서 나눔 (증명은 단계 경계까지)
      u.remove(); const kids = [...u.children]; let part = u.cloneNode(false); body.appendChild(part);
      const flat = []; kids.forEach(k => { if (k.classList.contains('proof')) { flat.push({ proof: k }); } else flat.push(k); });
      const pushProof = (pf) => {
        const ol = pf.querySelector('ol'); const lis = [...ol.children]; let cur = pf.cloneNode(true); cur.querySelector('ol').innerHTML = ''; part.appendChild(cur);
        lis.forEach(li => {
          cur.querySelector('ol').appendChild(li);
          if (over(s)) { li.remove(); s = sheet(ch.dataset.title); body = s.querySelector('.body'); part = u.cloneNode(false); part.classList.add('cont');
            if (h) part.appendChild(h.cloneNode(true)); body.appendChild(part); cur = pf.cloneNode(true); cur.querySelector('ol').innerHTML = ''; part.appendChild(cur); cur.querySelector('ol').appendChild(li); }
        });
      };
      flat.forEach(k => {
        if (k.proof) return pushProof(k.proof);
        part.appendChild(k);
        if (over(s)) { k.remove(); s = sheet(ch.dataset.title); body = s.querySelector('.body'); part = u.cloneNode(false); part.classList.add('cont');
          if (h && k !== h) part.appendChild(h.cloneNode(true)); body.appendChild(part); part.appendChild(k); }
      });
    }
    if (h) entry.subs.push({ t: h.textContent, p: page });
  });
});
// 각주 번호 (문서 순서대로)
let num = 0;
document.querySelectorAll('.sheet').forEach(s => { notes(s); const ds = s.querySelectorAll('.fns .n');
  s.querySelectorAll('.body sup.fr').forEach((r, i) => { num++; r.textContent = '[' + num + ']'; ds[i].textContent = '[' + num + ']'; }); });
// 목차
const tl = cover.querySelector('.toc');
toc.forEach(e => { tl.insertAdjacentHTML('beforeend', '<div class="c"><span>' + e.t + '</span><span class="pg">' + e.p + '</span></div>');
  e.subs.forEach(x => tl.insertAdjacentHTML('beforeend', '<div class="s"><span>' + x.t + '</span><span class="pg">' + x.p + '</span></div>')); });
document.getElementById('total').textContent = page + '쪽';
document.documentElement.dataset.ready = '1';
});
