/* ═══════════════════════════════════════════════════════════════
   시험지 공통 엔진 — drive/exam-engine/exam.js
   시험지 HTML 은 이 파일을 먼저 불러온 뒤, const META · const EXAM 만 정의한다.
   (엔진은 DOMContentLoaded 때 META · EXAM 을 읽어 시험지를 만든다)
   채점은 하지 않는다 — 문항마다 「정답 · 해설」을 펼쳐 스스로 확인하고, 원하면 내 점수를 적는다.
   ═══════════════════════════════════════════════════════════════ */

/* ── 데이터 작성용 도우미 (시험지 HTML 에서 그대로 쓴다) ── */
const F = (a,b)=>`<span class="frac"><span class="num">${a}</span><span class="den">${b}</span></span>`;   // 분수: F('n','2')
const B = s=>({a:s});                       // 표 빈칸: B('O') · B({a:'O(n²)',alt:['O(n^2)']})
const blank = (a,alt)=>({a,alt:alt||[]});  // 표 빈칸 (허용 답안 포함)

(function(){
const $=s=>document.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const NUM=['①','②','③','④','⑤','⑥'];
const TYPE={mc:'객관식',ox:'O/X',short:'단답형',table:'표 채우기',line:'코드 줄 고르기',essay:'서술형'};
const KOR='ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊ';
// O/X 문항의 표시 글자 — 과목마다 META.oxLabels 로 바꿀 수 있다 (예: ['T','F']). 답 값은 내부적으로 항상 'O'/'X'
const OXL=()=>(typeof META!=='undefined'&&META.oxLabels)||['O','X'];
// 빨간펜 표시 (path 를 data-d 에도 넣어 두고, 이미지 저장 때는 캔버스에 직접 다시 그린다)
const PEN_D={
  O:['M25 7 C38 6 45 15 44 26 C43 38 33 44 23 43 C11 42 5 33 7 22 C9 13 17 8 29 9',2.6],
  X:['M9 44 C20 31 31 18 43 6',3],
  V:['M7 27 C12 31 16 36 19 42 C25 28 33 16 45 6',2.8]
};
const PEN={}; for(const k in PEN_D){ const [d,w]=PEN_D[k];
  PEN[k]=`<svg class="pen mark" data-d="${d}" data-w="${w}" width="46" height="46" viewBox="0 0 50 50"><path d="${d}" fill="none" stroke="#D42A2A" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/></svg>`; }
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'})[c]);
const norm=s=>String(s).toLowerCase().replace(/<[^>]+>/g,'').replace(/\s+/g,'').replace(/[−–]/g,'-').replace(/[×·]/g,'*').replace(/²/g,'^2').replace(/ⁿ/g,'^n');
let qs=[], MAX=0, tid=null, t0=Date.now();

/* ════════ 1. 문항 HTML ════════ */
function qHTML(it){
  const head=it.q.replace(/<\/p>/,` <span class="pts">[${it.pts}점]</span></p>`);
  return `<article class="q" id="q${it.no}"><span class="pen-slot"></span>
    <div class="stem"><span class="no">${it.no}.</span><div class="text">${head}${field(it)}<div class="reveal"><button type="button" class="rv" data-no="${it.no}">정답 · 해설</button></div><div class="exp"></div></div></div></article>`;
}
function field(it){
  const n=it.no;
  if(it.type==='mc'){
    const len=Math.max(...it.choices.map(c=>c.replace(/<[^>]+>/g,'').length));
    return `<div class="choices ${len>12?'one':''}">`+it.choices.map((c,i)=>`<label><input type="${it.multi?'checkbox':'radio'}" name="a${n}" value="${i+1}"><span class="mk">${i+1}</span><span>${c}</span></label>`).join('')+'</div>';
  }
  if(it.type==='ox'){
    return `<table class="ox">`+it.items.map((s,i)=>`<tr><td class="k">${KOR[i]}.</td><td class="s">${s[0]}</td>
      <td class="c"><label title="${OXL()[0]}"><input type="radio" name="a${n}_${i}" value="O"><span class="mk">${OXL()[0]}</span></label></td>
      <td class="c"><label title="${OXL()[1]}"><input type="radio" name="a${n}_${i}" value="X"><span class="mk">${OXL()[1]}</span></label></td></tr>`).join('')+`</table>`;
  }
  if(it.type==='table'){
    let h=`<div class="tbl-wrap"><table class="tbl"><tr>${it.head.map(c=>`<th>${c}</th>`).join('')}</tr>`;
    it.rows.forEach((r,ri)=>{ h+='<tr>'+r.map((c,ci)=>{
      if(c&&typeof c==='object') return `<td class="blank" data-r="${ri}" data-c="${ci}"><input name="a${n}_${ri}_${ci}" autocomplete="off" aria-label="${n}번 표 ${ri+1}행 ${ci+1}열"><span class="fix"></span></td>`;
      return ci===0?`<th>${c}</th>`:`<td class="given">${c}</td>`;
    }).join('')+'</tr>'; });
    return h+'</table></div>';
  }
  if(it.type==='line'){
    return `<div class="lines">`+it.code.replace(/^\n/,'').split('\n').map((l,i)=>`<label><input type="checkbox" name="a${n}" value="${i+1}"><span class="ln">${i+1}</span><span class="cd">${esc(l)||' '}</span></label>`).join('')+'</div>';
  }
  if(it.type==='short') return `<div class="ansline">답 : <input type="text" name="a${n}" autocomplete="off" aria-label="${n}번 답"></div>`;
  return `<div class="essay ${it.pts>=12?'tall':''}"><div class="eh">답안 (풀이 과정)</div><textarea name="a${n}" aria-label="${n}번 답안"></textarea></div>`;
}
const blanksOf=it=>{const b=[];it.rows.forEach((r,ri)=>r.forEach((c,ci)=>{if(c&&typeof c==='object')b.push({ri,ci,a:c.a,alt:c.alt||[]});}));return b;};

/* ════════ 2. 쪽 만들기 (높이를 재서 2단에 자동 배치) ════════ */
const running=()=>`<div class="running"><span>${META.title}</span><span><b>${META.subject}</b></span></div>`;
const masthead=()=>`<header class="masthead">
  <div class="mh-top"><span class="org">${META.org}</span><span class="subj">${META.subject}</span></div>
  <div class="mh-title"><div class="y">${META.written}</div><h1>${META.title}</h1>
    <div class="total-pen" aria-label="총점"><span class="n" id="totalPen">0</span><span class="of">/ ${MAX}</span></div></div>
  <div class="idrow"><span class="h">응시일</span><span><input id="sdate" autocomplete="off" aria-label="응시일"></span><span class="h">성명</span><span><input id="sname" autocomplete="off" aria-label="성명"></span><span class="h">학번</span><span><input id="sid" autocomplete="off" aria-label="학번"></span></div>
  <div class="scope"><span class="h">출제 범위</span><div class="b">${META.scope}</div></div></header>`;
function paginate(){
  if(META.pages) return META.pages;                    // 직접 지정한 배치가 있으면 그대로
  const PAGE_H=1180, PAD=40+70;
  const m=document.createElement('section'); m.className='page measure';
  m.innerHTML=masthead()+`<div class="cols"><div class="col" id="mcol">${qs.map(qHTML).join('')}</div><div class="col"></div></div>`;
  document.body.appendChild(m);
  const capFirst=PAGE_H-PAD-m.querySelector('.masthead').offsetHeight-18-4;
  m.innerHTML=running()+`<div class="cols"><div class="col" id="mcol">${qs.map(qHTML).join('')}</div><div class="col"></div></div>`;
  const capRest=PAGE_H-PAD-m.querySelector('.running').offsetHeight-18-4;
  const hs=$$('#mcol .q',m).map(e=>e.offsetHeight);
  m.remove();
  const pages=[]; let p=null, side='R', used=0;
  const cap=()=>pages.length===1?capFirst:capRest;
  hs.forEach((h,i)=>{
    const no=i+1;
    if(!p||used+h>cap()&&used>0){                      // 지금 단에 안 들어가면 다음 단으로
      if(!p||side==='R'){ p={L:[],R:[]}; pages.push(p); side='L'; } else side='R';
      used=0;
    }
    p[side].push(no); used+=h;
  });
  // 마지막 쪽의 오른쪽 단이 비면, 왼쪽 단 아래 문항을 옮겨 두 단 높이를 맞춘다
  const last=pages[pages.length-1], H=n=>hs[n-1];
  if(last&&!last.R.length&&last.L.length>1){
    const sum=a=>a.reduce((s,n)=>s+H(n),0);
    while(last.L.length>1){
      const mv=last.L[last.L.length-1];
      const before=Math.max(sum(last.L),sum(last.R)), after=Math.max(sum(last.L)-H(mv),sum(last.R)+H(mv));
      if(after>=before) break;
      last.R.unshift(last.L.pop());
    }
  }
  return pages;
}
function render(){
  const P=paginate(), total=P.length;
  const pno=k=>`<div class="pno">${k} / ${total}</div>`;
  let h='';
  P.forEach((nos,i)=>{
    h+=`<section class="page">${i===0?masthead():running()}
      <div class="cols"><div class="col">${nos.L.map(n=>qHTML(qs[n-1])).join('')}</div><div class="col">${nos.R.map(n=>qHTML(qs[n-1])).join('')}</div></div>${pno(i+1)}</section>`;
  });
  $('#book').innerHTML=h;
  // 코드 블록(pre)을 줄마다 span 으로 감싼다 — 긴 줄이 줄바꿈될 때 이어진 줄만 깊게 들여써서 실제 들여쓰기와 구분 (가로 스크롤은 인쇄 때 잘림)
  $$('#book .q pre').forEach(p=>{ if(p.querySelector('.pl')) return; p.innerHTML=p.innerHTML.replace(/^\n/,'').split('\n').map(l=>`<span class="pl">${l||' '}</span>`).join(''); });
  // 이어진 줄의 들여쓰기 = 그 줄 자신의 들여쓰기 + 4칸 (줄마다 다르므로 여기서 계산)
  $$('#book .q pre .pl, #book .lines .cd').forEach(e=>{ const n=(e.textContent.match(/^ */)||[''])[0].length+4; e.style.paddingLeft=n+'ch'; e.style.textIndent=(-n)+'ch'; });
}

/* ════════ 3. 내 답 읽기 ════════ */
const el=it=>$('#q'+it.no);
function mine(it){
  const e=el(it);
  if(it.type==='mc'||it.type==='line') return $$('input:checked',e).map(x=>+x.value);
  if(it.type==='ox') return it.items.map((_,i)=>{const x=e.querySelector(`input[name="a${it.no}_${i}"]:checked`);return x?x.value:'';});
  if(it.type==='table') return blanksOf(it).map(b=>e.querySelector(`input[name="a${it.no}_${b.ri}_${b.ci}"]`).value.trim());
  return e.querySelector('input[type=text],textarea').value.trim();
}
function isEmpty(it){ const m=mine(it); return Array.isArray(m)?!m.some(v=>v!==''&&v!=null):!m; }

/* ════════ 5. 빨간펜 + 문항 아래 해설 ════════ */
function srcHTML(it){
  if(!it.src||!it.src.length) return '';
  // META.srcHref가 있으면 출처를 그 한 파일(예: 중간고사 슬라이드)의 섹션으로 연결한다: [장, 섹션, 제목] → srcHref#섹션
  if(META.srcHref) return `<div class="src">출처 ${it.src.map(([ch,sec,title])=>`<a href="${META.srcHref}${sec?'#'+sec:''}">${sec||ch}${title?' '+title:''}</a>`).join(' · ')}</div>`;
  return `<div class="src">출처 ${it.src.map(([ses,sec,title])=>{
    const w='week'+String(ses.split('-')[0]).padStart(2,'0');
    const href=`${META.lectureBase||'../lecture'}/${w}/${ses}.html${sec?'#'+sec:''}`;
    return `<a href="${href}">${ses}${title?' '+title:''}</a>`;}).join(' · ')}</div>`;
}
function rubHTML(it){
  if(!it.rubric||!it.rubric.length) return '';
  return `<div class="hit"><span class="rh">채점 기준</span>${it.rubric.map(r=>Array.isArray(r)?`<span>· ${r[0]}${r[1]!=null?` <b class="rp">${r[1]}점</b>`:''}</span>`:`<span>· ${r}</span>`).join('')}</div>`;
}
function selfHTML(it){ return `<div class="self">내 점수 <input type="number" inputmode="numeric" min="0" max="${it.pts}" step="1" name="s${it.no}" aria-label="${it.no}번 내 점수"> / ${it.pts}점</div>`; }
function paint(it){
    const e=el(it);
    const lv=it.lv?`<span class="lv">난이도 ${it.lv}</span>`:'';
    let x='';
    if(it.type==='mc'){
      $$('.choices label',e).forEach((l,i)=>l.classList.toggle('correct',it.answer.includes(i+1)));
      x=`<span class="a">정답 ${it.answer.map(a=>NUM[a-1]).join(', ')}</span>${lv}<br>${it.exp}`;
    } else if(it.type==='ox'){
      it.items.forEach((s,i)=>$$(`input[name="a${it.no}_${i}"]`,e).forEach(inp=>inp.parentElement.classList.toggle('correct',inp.value===(s[1]?'O':'X'))));
      x=`<span class="a">정답 ${it.items.map((s,i)=>KOR[i]+' '+(s[1]?OXL()[0]:OXL()[1])).join(', ')}</span>${lv}<br>${it.exp}`;
    } else if(it.type==='line'){
      $$('.lines label',e).forEach((l,i)=>l.classList.toggle('correct',it.answer.includes(i+1)));
      x=`<span class="a">정답 ${it.answer.join(', ')}번 줄</span>${lv}<br>${it.exp}`;
    } else if(it.type==='table'){
      blanksOf(it).forEach(b=>{ const td=e.querySelector(`td[data-r="${b.ri}"][data-c="${b.ci}"]`); td.querySelector('.fix').innerHTML=b.a; /* 정답에 분수(F) 같은 HTML 이 들어갈 수 있으므로 innerHTML */ });
      x=`<span class="a">정답은 빈칸 아래 빨간 글씨</span>${lv}<br>${it.exp}`;
    } else if(it.type==='short'){
      x=`<span class="a">정답 ${it.show}</span>${it.alt&&it.alt.length?` <span style="font-family:var(--gothic);font-size:11.5px">(허용 ${it.alt.join(' · ')})</span>`:''}${lv}<br>${it.exp}`;
    } else {
      x=`<span class="a">모범답안</span>${lv}<br>${it.model}`;
    }
    const keep=e.querySelector('.self input'); const v=keep?keep.value:null;
    e.querySelector('.exp').innerHTML=x+rubHTML(it)+srcHTML(it)+selfHTML(it);
    if(v!=null) e.querySelector('.self input').value=v;
}
function reveal(it,on){
  const e=el(it); if(on==null) on=!e.classList.contains('graded');
  if(on&&!e.querySelector('.exp').innerHTML) paint(it);
  e.classList.toggle('graded',on);
  e.querySelector('.rv').textContent=on?'정답 · 해설 접기':'정답 · 해설';
  syncAll();
}
function syncAll(){ const all=qs.every(it=>el(it).classList.contains('graded')); const b=$('#allBtn'); if(b) b.textContent=all?'정답 모두 숨기기':'정답 모두 보기'; }
/* ════════ 6. 내 점수 합계 (직접 적은 점수만 더함) ════════ */
const fmt=v=>Number.isInteger(v)?v:v.toFixed(1);
function total(){
  const ins=$$('#book .self input'); let sum=0, any=false;
  ins.forEach(i=>{ if(i.value!==''){ any=true; sum+=Math.max(0,Math.min(+i.max,+i.value||0)); } });
  $('#totalPen').textContent=fmt(sum); document.body.classList.toggle('done',any);
}

/* ════════ 7. 저장: PDF(인쇄) · 이미지(PNG) ════════ */
const stamp=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
const fileBase=()=>`${META.slug||'exam'}-${stamp()}`;
function toast(t,ms){const e=$('#toast'); e.textContent=t; e.classList.add('on'); clearTimeout(e._t); if(ms) e._t=setTimeout(()=>e.classList.remove('on'),ms);}
// 인쇄 직전: 각 쪽의 실제 높이를 재서 A4 한 장에 맞는 zoom 을 준다 (채점 후 해설로 길어진 쪽은 더 줄여서 한 장에)
const A4W=793.7, A4H=1122.5, PW=860;
function preparePrint(){
  document.body.classList.add('printing');
  const pages=$$('#book .page').filter(p=>getComputedStyle(p).display!=='none');
  pages.forEach(p=>{p.style.zoom='';p.style.height='';p.classList.remove('lastprint');});
  const base=A4W/PW, sheet=A4H/base;                  // 한 장 높이 (860px 기준) ≈ 1216px
  pages.forEach(p=>{
    const h=p.scrollHeight;
    if(h<=sheet){ p.style.zoom=base; p.style.height=sheet+'px'; }
    else { p.style.zoom=A4H/h-0.0005; p.style.height=h+'px'; }
  });
  if(pages.length) pages[pages.length-1].classList.add('lastprint');
}
function afterPrint(){ document.body.classList.remove('printing'); $$('#book .page').forEach(p=>{p.style.zoom='';p.style.height='';p.classList.remove('lastprint');}); }
window.addEventListener('beforeprint',preparePrint);
window.addEventListener('afterprint',afterPrint);
window.__examPrint={prepare:preparePrint,done:afterPrint};   // 테스트용
function savePDF(){                                   // 인쇄 창에서 'PDF로 저장' 을 고르면 파일 이름이 slug-날짜 로 잡힌다
  const t=document.title; document.title=fileBase(); window.print(); setTimeout(()=>document.title=t,500);
}
function loadScript(src){return new Promise((ok,no)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=no;document.head.appendChild(s);});}
async function saveImage(){
  try{
    toast('이미지를 만드는 중…');
    if(!window.html2canvas) await loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
    if(document.fonts&&document.fonts.ready) await document.fonts.ready;
    // textarea 는 html2canvas 가 줄바꿈을 못 그려서, 잠시 같은 모양의 div 로 바꿔 찍는다
    const swaps=$$('#book textarea').map(t=>{const d=document.createElement('div');d.className='ta-snap';d.textContent=t.value;
      const cs=getComputedStyle(t); Object.assign(d.style,{whiteSpace:'pre-wrap',font:cs.font,lineHeight:cs.lineHeight,padding:cs.padding,minHeight:cs.height,wordBreak:'break-all'}); t.style.display='none'; t.after(d); return [t,d];});
    document.body.classList.add('snap');
    const pages=$$('#book .page').filter(p=>p.offsetParent!==null);
    const total=pages.reduce((s,p)=>s+p.offsetHeight,0);
    const scale=Math.min(2,15000/total);                // 캔버스 최대 크기를 넘지 않게
    const cvs=[]; for(const p of pages){
      const c=await html2canvas(p,{scale,backgroundColor:'#fff',useCORS:true,logging:false,ignoreElements:e=>e.classList&&e.classList.contains('pen')});
      // html2canvas 는 svg 를 잘라 그리므로 빨간펜은 직접 그린다
      const g=c.getContext('2d'), pr=p.getBoundingClientRect();
      $$('svg.pen',p).forEach(s=>{ if(!s.getBoundingClientRect().width) return; const r=s.getBoundingClientRect(), k=r.width/50*scale;
        g.save(); g.setTransform(1,0,0,1,0,0); g.translate((r.left-pr.left)*scale,(r.top-pr.top)*scale); g.scale(k,k);
        g.strokeStyle='#D42A2A'; g.lineWidth=+s.dataset.w; g.lineCap='round'; g.lineJoin='round'; g.stroke(new Path2D(s.dataset.d)); g.restore(); });
      cvs.push(c);
    }
    swaps.forEach(([t,d])=>{d.remove();t.style.display='';}); document.body.classList.remove('snap');
    const gap=Math.round(16*scale), W=Math.max(...cvs.map(c=>c.width)), H=cvs.reduce((s,c)=>s+c.height,0)+gap*(cvs.length-1);
    const out=document.createElement('canvas'); out.width=W; out.height=H;
    const g=out.getContext('2d'); g.fillStyle='#D9D8D3'; g.fillRect(0,0,W,H);
    let y=0; cvs.forEach(c=>{g.drawImage(c,0,y); y+=c.height+gap;});
    out.toBlob(b=>{const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=fileBase()+'.png'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),4000); toast('이미지를 저장했습니다',2200);},'image/png');
  }catch(e){ document.body.classList.remove('snap'); $$('.ta-snap').forEach(d=>{d.previousElementSibling.style.display='';d.remove();}); toast('이미지 저장 실패 — 인쇄·PDF 저장을 이용하세요',3500); console.error(e); }
}

/* ════════ 8. 타이머 · 임시 저장(이 브라우저에만) ════════ */
function tick(){const s=Math.floor((Date.now()-t0)/1000);$('#timer').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
function startTimer(){ clearInterval(tid); t0=Date.now(); tick(); tid=setInterval(tick,1000); }
const KEY='exam:'+location.pathname;
function save(){ try{const d={};$$('#book [name^=a], #book [name^=s]').forEach(x=>{if(x.type==='radio'||x.type==='checkbox'){if(x.checked)(d[x.name]=d[x.name]||[]).push(x.value)}else d[x.name]=x.value});['sdate','sname','sid'].forEach(k=>d[k]=$('#'+k).value);localStorage.setItem(KEY,JSON.stringify(d));}catch(e){} }
function load(){ try{const d=JSON.parse(localStorage.getItem(KEY)||'{}');qs.forEach(it=>{if(d['s'+it.no]!=null&&d['s'+it.no]!=='')reveal(it,true);});$$('#book [name^=a], #book [name^=s]').forEach(x=>{const v=d[x.name];if(v==null)return;if(x.type==='radio'||x.type==='checkbox')x.checked=v.includes(x.value);else x.value=v});['sdate','sname','sid'].forEach(k=>$('#'+k).value=d[k]||'');total();}catch(e){} }   // 응시일·성명·학번은 직접 쓴다

/* ════════ 9. 출제 규칙 자가 점검 (개발자 콘솔에 경고) ════════ */
function lint(){
  const w=m=>console.warn('[exam] '+m);
  if(MAX!==100) w(`총점이 ${MAX}점입니다 (100점 권장)`);
  const mc=qs.filter(i=>i.type==='mc');
  const mcMax=META.mcMax??0.4;
  if(mc.length/qs.length>mcMax) w(`객관식 비율 ${Math.round(mc.length/qs.length*100)}% (${Math.round(mcMax*100)}% 이하 권장)`);
  const seq=mc.filter(i=>!i.multi).map(i=>i.answer[0]);
  for(let i=2;i<seq.length;i++) if(seq[i]===seq[i-1]&&seq[i]===seq[i-2]) w(`객관식 정답이 ${NUM[seq[i]-1]} 로 3번 연속`);
  const lv={}; qs.forEach(i=>lv[i.lv]=(lv[i.lv]||0)+1); if(!META.level) ['하','중','상'].forEach(k=>{if(!lv[k]) w(`난이도 '${k}' 문항이 없습니다`);});   // 난이도별 문제지(META.level)는 한 단계만 쓴다
  qs.forEach(i=>{ if(!i.exp&&!i.model) w(`${i.no}번 해설 없음`); if(!i.src) w(`${i.no}번 출처 없음`); if(i.rubric&&i.rubric.every(r=>Array.isArray(r)&&r[1]!=null)){const t=i.rubric.reduce((a,r)=>a+r[1],0); if(t!==i.pts) w(`${i.no}번 채점 기준 합 ${t} ≠ 배점 ${i.pts}`);} });
}

/* ════════ 10. 시작 ════════ */
function shell(){
  document.body.insertAdjacentHTML('afterbegin',`
<div class="toolbar">
  <button class="primary" id="allBtn">정답 모두 보기</button>
  <button id="resetBtn">답안 지우기</button>
  <span class="sep"></span>
  <button id="pdfBtn" title="인쇄 창에서 'PDF로 저장'을 고르면 PDF 파일이 됩니다">인쇄 · PDF</button>
  <button id="imgBtn" title="모든 쪽을 PNG 이미지 한 장으로 저장합니다">이미지 저장</button>
  <span class="clock"><span class="timer" id="timer">00:00</span><button id="timerReset" title="타이머를 0으로 되돌립니다">↺ 리셋</button></span>
</div>
<div id="book"></div>
<div class="toast" id="toast" role="status"></div>`);
}
function boot(){
  const miss=document.getElementById('engineMissing'); if(miss) miss.remove();
  qs=EXAM.map((it,i)=>Object.assign(it,{no:i+1,got:null,hits:[]}));
  MAX=qs.reduce((s,i)=>s+i.pts,0);
  if(!document.title||document.title==='시험지') document.title=`${META.subject} ${META.title}`;
  shell(); render(); load(); startTimer(); lint();
  document.addEventListener('input',e=>{ if(e.target.closest('#book')) save(); });
  document.addEventListener('click',e=>{ const b=e.target.closest('.rv'); if(b) reveal(qs[+b.dataset.no-1]); });
  document.addEventListener('input',e=>{ if(e.target.closest('.self')) total(); });
  $('#allBtn').onclick=()=>{ const on=!qs.every(it=>el(it).classList.contains('graded')); qs.forEach(it=>reveal(it,on)); };
  $('#timerReset').onclick=startTimer;
  $('#resetBtn').onclick=()=>{ if(!confirmReset()) return; try{localStorage.removeItem(KEY)}catch(e){} location.reload(); };
  $('#pdfBtn').onclick=savePDF;
  $('#imgBtn').onclick=saveImage;
}
let resetArmed=0;
function confirmReset(){ if(Date.now()-resetArmed<3000) return true; resetArmed=Date.now(); toast('답안과 내 점수가 모두 지워집니다. 한 번 더 누르면 지우기',3000); return false; }
// 글꼴이 다 내려온 뒤에 높이를 재야 쪽 배치가 맞는다 (최대 2초 기다림)
function start(){
  const fams=['400 16px "Nanum Myeongjo"','800 16px "Nanum Myeongjo"','400 16px "Nanum Gothic"','700 16px "Nanum Gothic"','16px "Nanum Gothic Coding"','16px "Nanum Pen Script"'];
  const wait=document.fonts?Promise.all(fams.map(f=>document.fonts.load(f,'가A1').catch(()=>{}))):Promise.resolve();
  Promise.race([wait,new Promise(r=>setTimeout(r,2000))]).then(boot);
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();
