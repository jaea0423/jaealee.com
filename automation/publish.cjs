// 자동화 전용 main 복제본에서 허용된 당일 자료만 발행합니다. 실패 시 작업을 보존합니다.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const assert = require('node:assert/strict');
const git = (...args) => execFileSync('git',args,{encoding:'utf8',timeout:60000,stdio:['ignore','pipe','pipe']}).trim();
const root = git('rev-parse','--show-toplevel');
process.chdir(root);
const lock = path.resolve(git('rev-parse','--git-common-dir'),'daily-publish.lock');
const statePath = path.join(lock,'state.json');
const read = file => JSON.parse(fs.readFileSync(file,'utf8'));
const seoulDate = () => new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const validDate = value => /^\d{4}-\d{2}-\d{2}$/.test(value) && new Date(value+'T12:00:00Z').toISOString().slice(0,10)===value;
const filesFor = date => [`news/data/${date}.json`,`knowledge/data/${date}.json`,'knowledge/index.json',`opportunities/${date}.json`,'opportunities/index.json'];
const lines = text => text.split('\n').filter(Boolean);
const nul = text => text.split('\0').filter(Boolean);
const clean = () => !git('status','--porcelain');
const branch = () => assert.equal(git('branch','--show-current'),'main','자동화 전용 main 브랜치가 필요합니다.');
const save = state => fs.writeFileSync(statePath,JSON.stringify(state,null,2));
function url(value) { assert(['https:','http:'].includes(new URL(value).protocol),'잘못된 출처 URL'); }
function text(value) { assert(typeof value==='string' && value.trim(),'필수 텍스트 누락'); }
function check() {
  // 공개 목록과 본문을 함께 검사합니다. 사실성·의미 중복은 편집자가 별도 확인합니다.
  const ki=read('knowledge/index.json');assert(Array.isArray(ki.editions));
  assert.equal(new Set(ki.editions.map(e=>e.date)).size,ki.editions.length,'지식 날짜 중복');
  for(const edition of ki.editions){
    assert(validDate(edition.date));const d=read(`knowledge/data/${edition.date}.json`);
    assert.equal(d.date,edition.date);assert.equal(d.articles.length,3);
    assert.deepEqual(d.articles.map(a=>a.kind),['basic','deep','sentence']);
    for(const a of d.articles){text(a.title);text(a.learning);assert(a.sources.length>0);a.sources.forEach(s=>url(s.url));assert(a.blocks.every(b=>['paragraph','heading','table','fraction'].includes(b.type)));}
    assert.deepEqual(edition.articles.map(a=>a.title),d.articles.map(a=>a.title),'지식 목록·본문 불일치');
  }
  const oi=read('opportunities/index.json');assert.equal(oi.schemaVersion,1);assert(Array.isArray(oi.editions));
  assert.equal(new Set(oi.editions).size,oi.editions.length,'기회 날짜 중복');
  for(const date of oi.editions){
    assert(validDate(date));const d=read(`opportunities/${date}.json`);assert.equal(d.date,date);assert.equal(d.schemaVersion,1);assert(Array.isArray(d.items));
    assert.equal(new Set(d.items.map(i=>i.id)).size,d.items.length,'기회 ID 중복');
    for(const i of d.items){for(const v of [i.id,i.title,i.category,i.location.region,i.location.place,i.event.label,i.application.status,i.price.label,i.verification,i.description,i.action,i.eligibility,i.caveat])text(v);assert(i.sources.length>0);i.sources.forEach(s=>url(s.url));assert(validDate(i.checkedOn));}
  }
  // 뉴스의 과거 형식 전체를 새 규격으로 강제하지 않고 최신 구조 파일을 검사합니다.
  const state=fs.existsSync(statePath)?read(statePath):null;
  const date=state?.date || seoulDate();
  const news=`news/data/${date}.json`;
  if(fs.existsSync(news)){
    const d=read(news);assert.equal(d.date,date);text(d.generatedAt);text(d.cutoff);assert(d.market&&Array.isArray(d.market.tiles));assert.equal(d.sections.length,5);
    for(const s of d.sections){text(s.labelKr);assert(Array.isArray(s.cards)&&s.cards.length<=4);for(const c of s.cards){text(c.title);text(c.summary);url(c.url);(c.supportingUrls||[]).forEach(url);}}
  }
  console.log('PASS: 콘텐츠 형식·날짜·출처 URL·목록 연결');
}
function preserveIndexes(state) {
  for(const [file,key] of [['knowledge/index.json','date'],['opportunities/index.json',null]]){
    const before=JSON.parse(git('show',`${state.base}:${file}`)).editions;
    const after=read(file).editions;
    for(const entry of before){
      const match=key?after.find(e=>e[key]===entry[key]):after.find(e=>e===entry);
      assert.deepEqual(match,entry,`기존 목록 변경 금지: ${file}`);
    }
  }
}
function changedFiles() {return [...new Set([...nul(git('diff','--name-only','-z','HEAD')),...nul(git('ls-files','--others','--exclude-standard','-z'))])];}
function prepare() {
  branch();assert(clean(),'기존 변경이 있습니다. 자동 stash/reset하지 않습니다.');
  fs.mkdirSync(lock); // atomic mkdir: 이전 실행이 남아 있으면 여기서 중단합니다.
  try {
    git('fetch','origin','main');assert.equal(git('rev-list','--count','origin/main..HEAD'),'0','미발행 커밋을 먼저 검토하세요.');git('merge','--ff-only','origin/main');
    const date=seoulDate(),base=git('rev-parse','HEAD');
    const existing=filesFor(date).filter(f=>!f.endsWith('/index.json')&&fs.existsSync(f));
    save({date,base,existing,phase:'prepared',createdAt:new Date().toISOString()});
    console.log(JSON.stringify({date,existing,allowed:filesFor(date)},null,2));
  } catch(e){save({phase:'prepare-failed',createdAt:new Date().toISOString()});throw e;}
}
function publish(){
  branch();const state=read(statePath);assert.equal(state.phase,'prepared','실패·미발행 상태는 먼저 수동 검토하세요.');
  assert.equal(git('rev-parse','HEAD'),state.base,'시작 후 다른 커밋이 생겼습니다.');
  const files=changedFiles();const allowed=filesFor(state.date);
  for(const file of files){assert(allowed.includes(file),`허용하지 않은 파일: ${file}`);assert(!state.existing.includes(file),`기존 발행본 변경 금지: ${file}`);assert(fs.existsSync(file),`파일 삭제 금지: ${file}`);}
  assert(!lines(git('diff','--name-only','--diff-filter=D','HEAD')).length,'삭제 금지');
  check();preserveIndexes(state);
  for(const [file,index] of [[`knowledge/data/${state.date}.json`,'knowledge/index.json'],[`opportunities/${state.date}.json`,'opportunities/index.json']]){
    if(files.includes(file))assert(files.includes(index),'날짜 파일과 목록을 함께 발행하세요.');
  }
  if(!files.length){fs.unlinkSync(statePath);fs.rmdirSync(lock);console.log('변경 없음');return;}
  git('diff','--check');git('add','--',...files);git('commit','-m',`Publish daily editions ${state.date}`);state.phase='committed';save(state);
  // 시간차 푸시는 정상적인 경합입니다. 서로 다른 파일만 최대 2회 재동기화합니다.
  for(let attempt=0;attempt<2;attempt++){
    git('fetch','origin','main');
    assert.equal(git('merge-base',state.base,'origin/main'),state.base,'원격 이력이 변경되었습니다.');
    const remoteFiles=nul(git('diff','--name-only','-z',state.base,'origin/main'));
    assert(!remoteFiles.some(f=>files.includes(f)),'같은 파일의 원격 변경 발견. 자동 병합하지 않습니다.');
    try{git('rebase','origin/main');}catch(e){git('rebase','--abort');throw e;}
    check();
    try{git('push','origin','HEAD:main');fs.unlinkSync(statePath);fs.rmdirSync(lock);console.log('PUSHED '+git('rev-parse','HEAD'));return;}
    catch(e){if(attempt===1)throw e;}
  }
}
function cancel(){branch();assert(clean(),'초안을 보존하고 검토하세요.');git('fetch','origin','main');assert.equal(git('rev-list','--count','origin/main..HEAD'),'0','미발행 커밋이 있습니다.');if(fs.existsSync(statePath))fs.unlinkSync(statePath);fs.rmdirSync(lock);console.log('잠금 해제');}
try{const command=process.argv[2];assert(['prepare','check','publish','cancel'].includes(command),'사용법: node automation/publish.cjs prepare|check|publish|cancel');({prepare,check,publish,cancel})[command]();}
catch(e){console.error('STOP: '+e.message);process.exitCode=1;}
