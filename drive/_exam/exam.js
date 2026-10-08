/* ═══════════════════════════════════════════════════════════════
   시험지 공통 엔진 — drive/_exam/exam.js
   시험지 HTML 은 이 파일을 먼저 불러온 뒤, const META · const EXAM 만 정의한다.
   (엔진은 DOMContentLoaded 때 META · EXAM 을 읽어 시험지를 만든다)
   ═══════════════════════════════════════════════════════════════ */

/* ── 데이터 작성용 도우미 (시험지 HTML 에서 그대로 쓴다) ── */
const F = (a,b)=>`<span class="frac"><span class="num">${a}</span><span class="den">${b}</span></span>`;   // 분수: F('n','2')
const B = s=>({a:s});                       // 표 빈칸: B('O') · B({a:'O(n²)',alt:['O(n^2)']})
const blank = (a,alt)=>({a,alt:alt||[]});  // 표 빈칸 (허용 답안 포함)

(function(){
const $=s=>document.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const NUM=['①','②','③','④','⑤','⑥'];
const TYPE={mc:'객관식',ox:'O/X',short:'단답형',table:'표 채우기',line:'코드 줄 고르기',essay:'서술형'};
const AUTO=new Set(['mc','ox','line']);           // 자동 채점 유형 (고르기만 하는 문항)
const KOR='ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊ';
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
let qs=[], MAX=0, submitted=false, manual=[], gi=0, tid=null, t0=Date.now();

/* ════════ 1. 문항 HTML ════════ */
function qHTML(it){
  const head=it.q.replace(/<\/p>/,` <span class="pts">[${it.pts}점]</span></p>`);
  return `<article class="q" id="q${it.no}"><span class="pen-slot"></span>
    <div class="stem"><span class="no">${it.no}.</span><div class="text">${head}${field(it)}<div class="exp"></div></div></div></article>`;
}
function field(it){
  const n=it.no;
  if(it.type==='mc'){
    const len=Math.max(...it.choices.map(c=>c.replace(/<[^>]+>/g,'').length));
    return `<div class="choices ${len>12?'one':''}">`+it.choices.map((c,i)=>`<label><input type="${it.multi?'checkbox':'radio'}" name="a${n}" value="${i+1}"><span class="mk">${i+1}</span><span>${c}</span></label>`).join('')+'</div>';
  }
  if(it.type==='ox'){
    return `<table class="ox">`+it.items.map((s,i)=>`<tr><td class="k">${KOR[i]}.</td><td class="s">${s[0]}</td>
      <td class="c"><label title="O"><input type="radio" name="a${n}_${i}" value="O"><span class="mk">O</span></label></td>
      <td class="c"><label title="X"><input type="radio" name="a${n}_${i}" value="X"><span class="mk">X</span></label></td></tr>`).join('')+`</table>`;
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
  const P=paginate(), total=P.length+1;
  const pno=k=>`<div class="pno">${k} / ${total}</div>`;
  let h='';
  P.forEach((nos,i)=>{
    h+=`<section class="page">${i===0?masthead():running()}
      <div class="cols"><div class="col">${nos.L.map(n=>qHTML(qs[n-1])).join('')}</div><div class="col">${nos.R.map(n=>qHTML(qs[n-1])).join('')}</div></div>${pno(i+1)}</section>`;
  });
  h+=`<section class="page after" id="repPage">${running()}<div id="report"></div>${pno(total)}</section>`;
  $('#book').innerHTML=h;
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

/* ════════ 4. 제출 → 자동 채점 → 직접 채점 ════════ */
// 덜 쓴 문항: 아무것도 안 했거나, O/X·표에서 하나라도 비운 문항
function incomplete(it){ const m=mine(it); if(it.type==='mc'||it.type==='line') return !m.length; return Array.isArray(m)?m.some(v=>v===''):!m; }
function openConfirm(){
  const empty=qs.filter(incomplete);
  $('#cfBody').innerHTML = empty.length
    ? `<p style="margin:0 0 6px">비었거나 덜 쓴 문항이 <b>${empty.length}개</b> 있습니다.<br>(${empty.map(i=>i.no+'번').join(', ')})</p><p style="margin:0">이 문항들은 정답일 수 없어 바로 오답 처리됩니다. 정말 제출하시겠습니까?</p>`
    : `<p style="margin:0">모든 문항에 답했습니다. 정말 제출하시겠습니까?</p><p style="margin:6px 0 0;font-size:12.5px;color:var(--ink-2)">제출하면 답안을 고칠 수 없습니다.</p>`;
  $('#confirmModal').classList.add('open'); $('#cfOk').focus();
}
/* 채점 원칙: 부분 점수 없음 — 문항마다 정답(배점 전부) 또는 오답(0점)
   · 객관식 · O/X · 코드 줄 : 자동 (하나라도 틀리면 오답)
   · 단답 · 표 · 서술 : 직접 판정. 단, 빈 답(표는 빈칸이 하나라도 있으면)은 정답일 수 없으므로 자동 오답 */
function autoGrade(it){
  const m=mine(it);
  if(it.type==='mc'||it.type==='line') return [...m].sort().join()===[...it.answer].sort().join()?it.pts:0;
  if(it.type==='ox') return it.items.every((s,i)=>m[i]===(s[1]?'O':'X'))?it.pts:0;
}
const hasBlank=it=>{ const m=mine(it); return Array.isArray(m)?m.some(v=>v===''):!m; };   // 빈 곳이 하나라도 있으면 정답 불가
const exact=it=>{                                      // 정답과 글자 그대로 같은가 (판정 '추천' 표시용)
  const m=mine(it);
  if(it.type==='short') return [it.show,...(it.alt||[])].map(norm).includes(norm(m));
  if(it.type==='table') return blanksOf(it).every((b,k)=>[b.a,...b.alt].map(norm).includes(norm(m[k])));
  return false;
};
function submit(){
  $('#confirmModal').classList.remove('open');
  submitted=true; clearInterval(tid); $('#submitBtn').disabled=true; save(true);
  $$('#book .q input, #book .q textarea').forEach(x=>x.disabled=true);
  qs.forEach(it=>{ if(AUTO.has(it.type)) it.got=autoGrade(it); });
  const rest=qs.filter(i=>!AUTO.has(i.type));
  rest.filter(hasBlank).forEach(it=>{ it.got=0; it.auto0=true; });   // 빈 답 → 자동 오답, 직접 채점에서 뺀다
  manual=rest.filter(i=>!i.auto0); gi=0;
  if(manual.length) openGrade(); else finish();
}
function openGrade(){ $('#gradeModal').classList.add('open'); drawGrade(); }
function drawGrade(){
  const it=manual[gi], m=mine(it), same=exact(it);
  $('#gdStep').textContent=`${gi+1} / ${manual.length} · ${it.no}번 (${TYPE[it.type]} · ${it.pts}점)`;
  let h=`<div>${it.q}</div>`;
  if(it.type==='table'){
    const bl=blanksOf(it); let k=0;
    h+=`<div class="tbl-wrap"><table class="tbl"><tr>${it.head.map(c=>`<th>${c}</th>`).join('')}</tr>`+
      it.rows.map(r=>'<tr>'+r.map((c,ci)=>{
        if(c&&typeof c==='object'){ const j=k++, b=bl[j], ok=[b.a,...b.alt].map(norm).includes(norm(m[j]));
          return `<td class="blank"><span class="cell"><span><span class="my">${esc(m[j])}</span><span class="ky">${ok?'':'정답 '}${b.a}${b.alt.length?' · '+b.alt.join(' · '):''}</span></span></span></td>`; }
        return ci===0?`<th>${c}</th>`:`<td class="given">${c}</td>`;
      }).join('')+'</tr>').join('')+`</table></div>
      <div class="note">각 칸: 위는 내 답, 빨간 글씨는 정답(허용 답안). 모든 칸이 맞아야 정답입니다.</div>
      <div class="box key"><div class="t">해설</div>${it.exp}</div>`;
  } else {
    h+=`<div class="box"><div class="t">내 답안</div><div class="mine">${esc(m)}</div></div>
      <div class="box key"><div class="t">${it.type==='essay'?'모범답안':'정답'}</div><div>${it.type==='essay'?it.model:`<b>${it.show}</b>${it.alt&&it.alt.length?`<div class="alt">허용 답안 : ${it.alt.join(' · ')}</div>`:''}<div style="margin-top:3px;color:var(--ink-2);font-size:12.6px">${it.exp}</div>`}</div></div>`;
    if(it.type==='essay'&&it.rubric) h+=`<div class="rub"><div class="rt"><span>채점 포인트 · 모두 들어 있어야 정답</span></div>${it.rubric.map(r=>`<div class="pt">· ${Array.isArray(r)?r[0]:r}</div>`).join('')}</div>`;
  }
  h+=`<div class="verdict"><button class="btn ${it.got===it.pts?'sel':''}" data-v="${it.pts}">정답 (${it.pts}점)</button><button class="btn ${it.got===0?'sel':''}" data-v="0">오답 (0점)</button>
      ${same&&it.got==null?'<span class="note" style="margin:0">정답과 글자 그대로 같습니다</span>':''}</div>`;
  $('#gdBody').innerHTML=h; $('#gdBody').scrollTop=0;
  $('#gdPrev').disabled=gi===0;
  $('#gdNext').textContent=gi===manual.length-1?'채점 완료':'다음';
  $$('#gdBody .verdict button[data-v]').forEach(b=>b.onclick=()=>{it.got=+b.dataset.v; it.judged=true; drawGrade();});
}
function nextGrade(){ const it=manual[gi]; if(it.got==null) it.got=0; it.judged=true; if(gi<manual.length-1){gi++; drawGrade();} else finish(); }   // 판정 없이 넘기면 오답
function allWrong(){   // 아직 판정하지 않은 문항(지금 문항 포함)을 모두 오답으로
  manual.slice(gi).forEach(it=>{ if(!it.judged){ it.got=0; it.judged=true; } });
  finish();
}
function finish(){
  $('#gradeModal').classList.remove('open');
  document.body.classList.add('done'); $('#regradeBtn').hidden=false;
  paint(); report(); window.scrollTo({top:0,behavior:'smooth'});
}

/* ════════ 5. 빨간펜 + 문항 아래 해설 ════════ */
function srcHTML(it){
  if(!it.src||!it.src.length) return '';
  return `<div class="src">출처 ${it.src.map(([ses,sec,title])=>{
    const w='week'+String(ses.split('-')[0]).padStart(2,'0');
    const href=`${META.lectureBase||'../lecture'}/${w}/${ses}.html${sec?'#'+sec:''}`;
    return `<a href="${href}">${ses}${title?' '+title:''}</a>`;}).join(' · ')}</div>`;
}
function paint(){
  qs.forEach(it=>{
    const e=el(it); e.classList.add('graded');
    e.querySelector('.pen-slot').innerHTML=it.got>=it.pts?PEN.O:PEN.X;
    const lv=it.lv?`<span class="lv">난이도 ${it.lv}</span>`:'';
    let x='';
    if(it.type==='mc'){
      $$('.choices label',e).forEach((l,i)=>l.classList.toggle('correct',it.answer.includes(i+1)));
      x=`<span class="a">정답 ${it.answer.map(a=>NUM[a-1]).join(', ')}</span>${lv}<br>${it.exp}`;
    } else if(it.type==='ox'){
      it.items.forEach((s,i)=>$$(`input[name="a${it.no}_${i}"]`,e).forEach(inp=>inp.parentElement.classList.toggle('correct',inp.value===(s[1]?'O':'X'))));
      x=`<span class="a">정답 ${it.items.map((s,i)=>KOR[i]+' '+(s[1]?'O':'X')).join(', ')}</span>${lv}<br>${it.exp}`;
    } else if(it.type==='line'){
      $$('.lines label',e).forEach((l,i)=>l.classList.toggle('correct',it.answer.includes(i+1)));
      x=`<span class="a">정답 ${it.answer.join(', ')}번 줄</span>${lv}<br>${it.exp}`;
    } else if(it.type==='table'){
      const m=mine(it);   // 정답 처리된 표는 표시 안 함. 오답이면 정답과 다른 칸에 빨간 글씨
      blanksOf(it).forEach((b,k)=>{ const td=e.querySelector(`td[data-r="${b.ri}"][data-c="${b.ci}"]`); const bad=it.got===0&&![b.a,...b.alt].map(norm).includes(norm(m[k])); td.classList.toggle('wrong',bad); td.querySelector('.fix').textContent=b.a; });
      x=`<span class="a">정답은 틀린 칸 아래 빨간 글씨</span>${lv}<br>${it.exp}`;
    } else if(it.type==='short'){
      x=`<span class="a">정답 ${it.show}</span>${it.alt&&it.alt.length?` <span style="font-family:var(--gothic);font-size:11.5px">(허용 ${it.alt.join(' · ')})</span>`:''}${lv}<br>${it.exp}`;
    } else {
      x=`<span class="a">모범답안</span>${lv}<br>${it.model}${it.rubric?`<div class="hit">${it.rubric.map(r=>`<span>· ${Array.isArray(r)?r[0]:r}</span>`).join('')}</div>`:''}`;
    }
    e.querySelector('.exp').innerHTML=x+srcHTML(it);
  });
}

/* ════════ 6. 총점 · 성적표 ════════ */
const fmt=v=>Number.isInteger(v)?v:v.toFixed(1);
function report(){
  const total=Math.round(qs.reduce((s,i)=>s+(i.got||0),0)*10)/10;
  $('#totalPen').textContent=fmt(total);
  const g=total>=90?'A':total>=80?'B':total>=70?'C':total>=60?'D':'F';
  const per=Math.ceil(qs.length/2), rows=[qs.slice(0,per),qs.slice(per)];
  const short={mc:'객관',ox:'OX',short:'단답',table:'표',line:'코드',essay:'서술'};
  const grid=rows.map(r=>`<table class="grid"><tr><th>번호</th>${r.map(i=>`<th>${i.no}</th>`).join('')}</tr><tr><th>유형</th>${r.map(i=>`<td>${short[i.type]}</td>`).join('')}</tr><tr><th>난이도</th>${r.map(i=>`<td>${i.lv||'-'}</td>`).join('')}</tr><tr><th>배점</th>${r.map(i=>`<td>${i.pts}</td>`).join('')}</tr><tr><th>득점</th>${r.map(i=>`<td class="r">${fmt(i.got)}</td>`).join('')}</tr></table>`).join('');
  const agg=key=>{const o={}; qs.forEach(i=>{const k=key(i); if(!k) return; const u=o[k]=o[k]||{g:0,m:0,n:[]}; u.g+=i.got; u.m+=i.pts; u.n.push(i.no);}); return Object.entries(o);};
  const bar=(g,m)=>`<div class="bar"><i style="width:${m?g/m*100:0}%"></i></div>`;
  const tbl=(title,list)=>list.length?`<table class="rep"><tr><th style="width:22%">${title}</th><th style="width:16%">득점 / 배점</th><th>득점률</th><th style="width:24%">문항</th></tr>
      ${list.map(([u,v])=>`<tr><td class="l">${u}</td><td>${fmt(Math.round(v.g*10)/10)} / ${v.m}</td><td>${bar(v.g,v.m)}</td><td>${v.n.join(', ')}</td></tr>`).join('')}</table>`:'';
  const order=['하','중','상'];
  const wrong=qs.filter(i=>i.got<i.pts);
  $('#report').innerHTML=`<div class="report-head"><h2>성적표</h2><div>${$('#sdate').value||'응시일 미기입'} · ${$('#sname').value||'성명 미기입'} · ${$('#sid').value||'학번 미기입'} · ${META.subject} · 소요 시간 ${$('#timer').textContent}</div></div>
    <div class="total"><span class="n">${fmt(total)}</span><span class="of">/ ${MAX}점</span><span class="g">${g}</span></div>
    ${grid}${tbl('난이도',agg(i=>i.lv).sort((a,b)=>order.indexOf(a[0])-order.indexOf(b[0])))}${tbl('유형',agg(i=>TYPE[i.type]))}${tbl('단원',agg(i=>i.unit))}
    <div class="review">${wrong.length?`<b>다시 볼 문항</b> &nbsp;${wrong.map(i=>`<a href="#q${i.no}">${i.no}번</a> (${i.unit}, ${fmt(i.got)}/${i.pts})`).join(' · ')}`:'<b>모든 문항 만점입니다.</b>'}<br>점수를 고치려면 위쪽의 「채점 수정」을 누르세요. 등급은 90·80·70·60점 기준의 임의 표시입니다.</div>`;
}

/* ════════ 7. 저장: PDF(인쇄) · 이미지(PNG) ════════ */
const stamp=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
const fileBase=()=>`${META.slug||'exam'}-${stamp()}${submitted?'-graded':''}`;
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
function startTimer(){ if(submitted) return; clearInterval(tid); t0=Date.now(); tick(); tid=setInterval(tick,1000); }
const KEY='exam:'+location.pathname;
function save(force){ if(submitted&&!force) return; try{const d={};$$('#book [name^=a]').forEach(x=>{if(x.type==='radio'||x.type==='checkbox'){if(x.checked)(d[x.name]=d[x.name]||[]).push(x.value)}else d[x.name]=x.value});['sdate','sname','sid'].forEach(k=>d[k]=$('#'+k).value);localStorage.setItem(KEY,JSON.stringify(d));}catch(e){} }
function load(){ try{const d=JSON.parse(localStorage.getItem(KEY)||'{}');$$('#book [name^=a]').forEach(x=>{const v=d[x.name];if(v==null)return;if(x.type==='radio'||x.type==='checkbox')x.checked=v.includes(x.value);else x.value=v});['sdate','sname','sid'].forEach(k=>$('#'+k).value=d[k]||'');}catch(e){} }   // 응시일·성명·학번은 직접 쓴다

/* ════════ 9. 출제 규칙 자가 점검 (개발자 콘솔에 경고) ════════ */
function lint(){
  const w=m=>console.warn('[exam] '+m);
  if(MAX!==100) w(`총점이 ${MAX}점입니다 (100점 권장)`);
  const mc=qs.filter(i=>i.type==='mc');
  const mcMax=META.mcMax??0.4;
  if(mc.length/qs.length>mcMax) w(`객관식 비율 ${Math.round(mc.length/qs.length*100)}% (${Math.round(mcMax*100)}% 이하 권장)`);
  const seq=mc.filter(i=>!i.multi).map(i=>i.answer[0]);
  for(let i=2;i<seq.length;i++) if(seq[i]===seq[i-1]&&seq[i]===seq[i-2]) w(`객관식 정답이 ${NUM[seq[i]-1]} 로 3번 연속`);
  const lv={}; qs.forEach(i=>lv[i.lv]=(lv[i.lv]||0)+1); ['하','중','상'].forEach(k=>{if(!lv[k]) w(`난이도 '${k}' 문항이 없습니다`);});
  qs.forEach(i=>{ if(!i.exp&&!i.model) w(`${i.no}번 해설 없음`); if(!i.src) w(`${i.no}번 출처 없음`); });
}

/* ════════ 10. 시작 ════════ */
function shell(){
  document.body.insertAdjacentHTML('afterbegin',`
<div class="toolbar">
  <button class="primary" id="submitBtn">답안 제출</button>
  <button id="regradeBtn" hidden>채점 수정</button>
  <button id="resetBtn">다시 풀기</button>
  <span class="sep"></span>
  <button id="pdfBtn" title="인쇄 창에서 'PDF로 저장'을 고르면 PDF 파일이 됩니다">인쇄 · PDF</button>
  <button id="imgBtn" title="모든 쪽을 PNG 이미지 한 장으로 저장합니다">이미지 저장</button>
  <span class="clock"><span class="timer" id="timer">00:00</span><button id="timerReset" title="타이머를 0으로 되돌립니다">↺ 리셋</button></span>
</div>
<div id="book"></div>
<div class="modal" id="confirmModal" role="dialog" aria-modal="true" aria-labelledby="cfTitle"><div class="dlg">
  <div class="dh" id="cfTitle">답안 제출</div><div class="db" id="cfBody"></div>
  <div class="df"><span class="sp"></span><button class="btn" id="cfCancel">계속 풀기</button><button class="btn dark" id="cfOk">제출하기</button></div></div></div>
<div class="modal" id="gradeModal" role="dialog" aria-modal="true" aria-labelledby="gdTitle"><div class="dlg wide">
  <div class="dh"><span id="gdTitle">직접 채점</span><span class="step" id="gdStep"></span></div><div class="db" id="gdBody"></div>
  <div class="df"><button class="btn ghost" id="gdAllWrong">남은 문항 일괄 오답</button><span class="sp"></span><button class="btn" id="gdPrev">이전</button><button class="btn dark" id="gdNext">다음</button></div></div></div>
<div class="toast" id="toast" role="status"></div>`);
}
function boot(){
  const miss=document.getElementById('engineMissing'); if(miss) miss.remove();
  qs=EXAM.map((it,i)=>Object.assign(it,{no:i+1,got:null,hits:[]}));
  MAX=qs.reduce((s,i)=>s+i.pts,0);
  if(!document.title||document.title==='시험지') document.title=`${META.subject} ${META.title}`;
  shell(); render(); load(); startTimer(); lint();
  document.addEventListener('input',e=>{ if(e.target.closest('#book')) save(); });
  $('#submitBtn').onclick=openConfirm;
  $('#cfCancel').onclick=()=>$('#confirmModal').classList.remove('open');
  $('#cfOk').onclick=submit;
  $('#gdNext').onclick=nextGrade;
  $('#gdPrev').onclick=()=>{ if(gi>0){gi--; drawGrade();} };
  $('#gdAllWrong').onclick=allWrong;
  $('#regradeBtn').onclick=()=>{ gi=0; openGrade(); };
  $('#timerReset').onclick=startTimer;
  $('#resetBtn').onclick=()=>{ if(!submitted&&!confirmReset()) return; try{localStorage.removeItem(KEY)}catch(e){} location.reload(); };
  $('#pdfBtn').onclick=savePDF;
  $('#imgBtn').onclick=saveImage;
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') $('#confirmModal').classList.remove('open'); });
}
let resetArmed=0;
function confirmReset(){ if(Date.now()-resetArmed<3000) return true; resetArmed=Date.now(); toast('답안이 모두 지워집니다. 한 번 더 누르면 다시 풀기',3000); return false; }
// 글꼴이 다 내려온 뒤에 높이를 재야 쪽 배치가 맞는다 (최대 2초 기다림)
function start(){
  const fams=['400 16px "Nanum Myeongjo"','800 16px "Nanum Myeongjo"','400 16px "Nanum Gothic"','700 16px "Nanum Gothic"','16px "Nanum Gothic Coding"','16px "Nanum Pen Script"'];
  const wait=document.fonts?Promise.all(fams.map(f=>document.fonts.load(f,'가A1').catch(()=>{}))):Promise.resolve();
  Promise.race([wait,new Promise(r=>setTimeout(r,2000))]).then(boot);
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();
