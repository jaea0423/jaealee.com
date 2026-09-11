/* 날짜별 읽을거리와 보관함을 분리하고, 데이터는 HTML로 실행하지 않습니다. */
(() => {
  const $ = id => document.getElementById(id);
  const content=$('knowledge-content'), status=$('knowledge-status'), date=$('knowledge-date');
  const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  let editions=[], loaded=false, loading=null, request=0, current='';
  const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
  const validDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s)&&!Number.isNaN(Date.parse(s+'T12:00:00Z'))&&new Date(s+'T12:00:00Z').toISOString().slice(0,10)===s;
  async function get(path){
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),10000);
    try{const r=await fetch(path,{signal:controller.signal,cache:'no-store'});if(!r.ok)throw Error(String(r.status));return await r.json();}finally{clearTimeout(timer);}
  }
  function sourceLinks(sources){
    const box=node('div',null,'knowledge-sources');box.append(node('span','출처'));
    for(const s of sources||[]){try{const u=new URL(s.url);if(u.protocol!=='https:')continue;const a=node('a',s.title+' ↗');a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';box.append(a);}catch{}}
    return box;
  }
  function renderBlock(block){
    if(block.type==='table'){
      const wrap=node('div',null,'knowledge-table'),table=node('table');table.append(node('caption',block.caption));
      const head=node('thead'),row=node('tr');for(const cell of block.headers){const th=node('th',cell);th.scope='col';row.append(th);}head.append(row);table.append(head);
      const body=node('tbody');for(const cells of block.rows){const tr=node('tr');cells.forEach((cell,i)=>{const td=node(i===0?'th':'td',cell);if(i===0)td.scope='row';tr.append(td);});body.append(tr);}table.append(body);wrap.append(table);return wrap;
    }
    if(block.type==='fraction'){
      const wrap=node('div',null,'knowledge-formula');const ns='http://www.w3.org/1998/Math/MathML';const math=document.createElementNS(ns,'math');math.setAttribute('display','block');math.setAttribute('aria-label',block.label);
      const frac=document.createElementNS(ns,'mfrac');for(const t of [block.numerator,block.denominator]){const e=document.createElementNS(ns,'mtext');e.textContent=t;frac.append(e);}math.append(frac);wrap.append(math,node('span',block.result));return wrap;
    }
    return node(block.type==='heading'?'h4':'p',block.text);
  }
  function render(data){
    if(data.date!==date.value||!Array.isArray(data.articles)||data.articles.length!==3)throw Error('Invalid edition');
    const frag=document.createDocumentFragment();
    data.articles.forEach((a,i)=>{
      const article=node('article',null,'knowledge-article');article.id='knowledge-'+a.kind;article.tabIndex=-1;
      const margin=node('div',null,'knowledge-margin');margin.append(node('span',String(i+1).padStart(2,'0'),'knowledge-number'),node('h3',a.label),node('p',a.category+' · '+a.readingTime));
      const body=node('div',null,'knowledge-body');body.append(node('h3',a.title));
      if(a.quote){body.append(node('blockquote',a.quote),node('p',a.attribution,'knowledge-attribution'));}
      else body.append(node('p',a.summary,'knowledge-summary'));
      for(const b of a.blocks||[])body.append(renderBlock(b));
      if(a.takeaway)body.append(node('p',a.takeaway,'knowledge-takeaway'));
      body.append(sourceLinks(a.sources));article.append(margin,body);frag.append(article);
    });
    content.replaceChildren(frag);
    $('knowledge-edition').textContent=data.date.replaceAll('-','.');
    $('knowledge-jumps').hidden=false;
  }
  function archive(){
    const q=$('knowledge-search').value.trim().toLocaleLowerCase(),cat=$('knowledge-category').value;
    const list=$('knowledge-archive-list');list.replaceChildren();let count=0;
    for(const e of editions){for(const a of e.articles){if(cat&&a.category!==cat)continue;if(q&&!`${a.title} ${a.category} ${a.author||''}`.toLocaleLowerCase().includes(q))continue;
      const item=node('li'),link=node('a');link.href='#knowledge/'+e.date+'/'+a.kind;
      link.append(node('time',e.date),node('span',a.title),node('small',a.label+' · '+a.category));item.append(link);list.append(item);count++;}}
    $('knowledge-archive-count').textContent=`${count}편`;
    $('knowledge-archive-empty').hidden=count>0;
  }
  async function init(){
    if(loaded)return;if(loading)return loading;
    loading=(async()=>{const data=await get('/knowledge/index.json');if(!Array.isArray(data.editions))throw Error('Invalid index');
      editions=data.editions.filter(e=>validDate(e.date)&&e.date<=today&&Array.isArray(e.articles)).sort((a,b)=>b.date.localeCompare(a.date));
      const categories=[...new Set(editions.flatMap(e=>e.articles.map(a=>a.category)))];
      $('knowledge-category').replaceChildren(new Option('모든 분야',''),...categories.map(c=>new Option(c,c)));loaded=true;archive();})();
    try{await loading;}finally{loading=null;}
  }
  function navigation(){
    $('knowledge-prev').disabled=!editions.some(e=>e.date<date.value);
    $('knowledge-next').disabled=!editions.some(e=>e.date>date.value);
  }
  async function route(force=false){
    const [tab,chosen,part]=location.hash.slice(1).split('/');if(tab!=='knowledge')return;
    const id=++request;status.textContent='읽을거리를 불러오는 중입니다.';$('knowledge-retry').hidden=true;
    try{
      await init();if(id!==request)return;
      date.value=validDate(chosen||'')?chosen:(editions[0]?.date||today);navigation();
      if(current!==date.value||force){
        content.replaceChildren();$('knowledge-jumps').hidden=true;$('knowledge-edition').textContent=date.value.replaceAll('-','.');
        if(!editions.some(e=>e.date===date.value)){status.textContent='이 날짜에는 발행된 지식이 없습니다. 아래 보관함에서 다른 글을 선택해주세요.';current='';return;}
        const data=await get('/knowledge/data/'+date.value+'.json');if(id!==request)return;render(data);current=date.value;
      }
      status.textContent='';
      if(['basic','deep','sentence'].includes(part)){const target=$('knowledge-'+part);target?.focus({preventScroll:true});target?.scrollIntoView({block:'start'});}
    }catch{if(id!==request)return;current='';content.replaceChildren();$('knowledge-jumps').hidden=true;status.textContent='읽을거리를 불러오지 못했습니다. 다시 시도해주세요.';$('knowledge-retry').hidden=false;}
  }
  $('knowledge-retry').addEventListener('click',()=>route(true));
  $('knowledge-form').addEventListener('submit',e=>{e.preventDefault();if(validDate(date.value))location.hash='knowledge/'+date.value;});
  date.addEventListener('change',()=>{if(validDate(date.value))location.hash='knowledge/'+date.value;});
  for(const [id,direction] of [['knowledge-prev',-1],['knowledge-next',1]])$(id).addEventListener('click',()=>{
    const candidates=editions.filter(e=>direction<0?e.date<date.value:e.date>date.value);const next=direction<0?candidates[0]:candidates.at(-1);if(next)location.hash='knowledge/'+next.date;
  });
  $('knowledge-latest').addEventListener('click',()=>{if(location.hash==='#knowledge')route(true);else location.hash='knowledge';});
  $('knowledge-search').addEventListener('input',archive);$('knowledge-category').addEventListener('change',archive);
  $('knowledge-jumps').addEventListener('click',e=>{const b=e.target.closest('[data-reading]');if(b){const a=$('knowledge-'+b.dataset.reading);a?.focus({preventScroll:true});a?.scrollIntoView({block:'start'});}});
  window.addEventListener('hashchange',()=>route());route();
})();
