// Run only after the scheduler has verified the preceding writer is inactive.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const git = (...args) => execFileSync('git', args, {encoding:'utf8',timeout:60000,stdio:['ignore','pipe','pipe']}).trim();
const rawGit = (...args) => execFileSync('git', args, {timeout:60000,stdio:['ignore','pipe','pipe']});
function resumePush(state,lock,common){
  assert.equal(git('status','--porcelain'),'','Committed recovery requires a clean tree');
  git('fetch','origin','main');
  const archive=()=>{const dir=path.join(common,'daily-recovery-archives',new Date().toISOString().replace(/[:.]/g,'-'));fs.mkdirSync(dir,{recursive:true,mode:0o700});fs.renameSync(lock,path.join(dir,'published-lock'));console.log('PUSH_RECOVERED '+git('rev-parse','HEAD'));};
  if(git('rev-list','--count','origin/main..HEAD')==='0'){archive();return;}
  assert.equal(git('rev-list','--count','origin/main..HEAD'),'1','Unexpected unpublished commits');
  assert.equal(git('log','-1','--format=%s'),`Publish daily editions ${state.date}`,'Unexpected commit');
  const allowed=[`news/data/${state.date}.json`,'news/index.json',`knowledge/data/${state.date}.json`,'knowledge/index.json',`opportunities/${state.date}.json`,'opportunities/index.json'];
  const files=git('diff','--name-only','HEAD^','HEAD').split('\n').filter(Boolean);
  for(const f of files){assert(allowed.includes(f)&&!(state.existing||[]).includes(f),'Unexpected committed file: '+f);assert(fs.existsSync(f),'Deleted file');if(!f.endsWith('/index.json'))assert.equal(git('ls-tree','HEAD^','--',f),'','Existing edition modified');}
  for(const f of files.filter(f=>f.endsWith('/index.json'))){const before=JSON.parse(git('show',`HEAD^:${f}`)).editions,after=JSON.parse(fs.readFileSync(f)).editions;for(const item of before)assert.deepEqual(after.find(e=>typeof item==='string'?e===item:e.date===item.date),item,'Existing index entry modified');}
  for(let attempt=0;attempt<2;attempt++){
    git('fetch','origin','main');
    const parent=git('rev-parse','HEAD^');assert.equal(git('merge-base',parent,'origin/main'),parent,'Unexpected history');
    const remote=git('diff','--name-only',parent,'origin/main').split('\n');assert(!remote.some(f=>files.includes(f)),'Same-file remote conflict');
    git('rebase','origin/main');
    execFileSync(process.execPath,['automation/publish.cjs','check'],{stdio:'inherit'});
    try{git('push','origin','HEAD:main');archive();return;}catch(e){if(attempt===1)throw e;}
  }
}
function recover() {
  assert(process.argv.includes('--previous-run-inactive'), 'Confirm previous scheduler run is inactive first');
  process.chdir(git('rev-parse','--show-toplevel'));
  assert.equal(git('branch','--show-current'),'main');
  const common=path.resolve(git('rev-parse','--git-common-dir'));
  const lock=path.join(common,'daily-publish.lock');
  if(!fs.existsSync(lock)){console.log('NO_LOCK');return;}
  for(const marker of ['index.lock','MERGE_HEAD','rebase-merge','rebase-apply','CHERRY_PICK_HEAD']) assert(!fs.existsSync(path.join(common,marker)), 'Git operation in progress: '+marker);
  const stateText=fs.readFileSync(path.join(lock,'state.json'),'utf8');
  const state=JSON.parse(stateText);
  if(state.phase==='committed'){resumePush(state,lock,common);return;}
  assert(['prepared','prepare-failed'].includes(state.phase),'Committed run needs validated push recovery; no automatic discard');
  assert.equal(git('diff','--cached','--name-only'),'','Staged changes require review');
  git('fetch','origin','main');
  assert.equal(git('rev-list','--count','origin/main..HEAD'),'0','Unpublished commits require push recovery');
  const head=git('rev-parse','HEAD');
  if(state.phase==='prepared')assert.equal(head,state.base,'HEAD changed since prepare');
  const files=[...new Set([...git('diff','--name-only','-z','HEAD').split('\0'),...git('ls-files','--others','--exclude-standard','-z').split('\0')].filter(Boolean))];
  const allowed=[`news/data/${state.date}.json`,'news/index.json',`knowledge/data/${state.date}.json`,'knowledge/index.json',`opportunities/${state.date}.json`,'opportunities/index.json'];
  if(state.phase==='prepare-failed')assert.equal(files.length,0,'Failed prepare must be clean');
  const remoteFiles=git('diff','--name-only','-z',head,'origin/main').split('\0');
  assert(!files.some(f=>remoteFiles.includes(f)),'Remote changed the same files; preserve for review');
  const snapshots=[];
  for(const file of files){
    assert(allowed.includes(file),'Unrelated change: '+file);
    assert(!(state.existing||[]).includes(file),'Existing edition modified: '+file);
    assert(fs.lstatSync(file).isFile(),'Missing or nonregular file: '+file);
    const tracked=!!git('ls-files','--',file);
    assert(!tracked || file.endsWith('/index.json'),'Published JSON must remain immutable');
    const data=fs.readFileSync(file);
    snapshots.push({file,tracked,data,original:tracked?rawGit('show',`HEAD:${file}`):null});
  }
  const guard=path.join(common,'daily-recovery.lock');
  fs.mkdirSync(guard);
  try {
    const archive=path.join(common,'daily-recovery-archives',new Date().toISOString().replace(/[:.]/g,'-'));
    fs.mkdirSync(archive,{recursive:true,mode:0o700});
    fs.writeFileSync(path.join(archive,'state.json'),stateText,{mode:0o600});
    fs.writeFileSync(path.join(archive,'manifest.json'),JSON.stringify({head,origin:git('rev-parse','origin/main'),files:files,reason:'inactive interrupted generation',createdAt:new Date().toISOString()},null,2),{mode:0o600});
    for(const s of snapshots){const target=path.join(archive,'draft',s.file);fs.mkdirSync(path.dirname(target),{recursive:true,mode:0o700});fs.writeFileSync(target,s.data,{mode:0o600});assert(fs.readFileSync(target).equals(s.data));}
    // Recheck every snapshot before touching any source. Backups remain on failure.
    assert.equal(fs.readFileSync(path.join(lock,'state.json'),'utf8'),stateText);
    assert.equal(git('rev-parse','HEAD'),head);
    for(const s of snapshots)assert(fs.readFileSync(s.file).equals(s.data),'Concurrent change: '+s.file);
    for(const s of snapshots){if(s.tracked)fs.writeFileSync(s.file,s.original);else fs.unlinkSync(s.file);}
    assert.equal(git('status','--porcelain'),'','Unexpected changes remain');
    fs.renameSync(lock,path.join(archive,'original-lock'));
    console.log('RECOVERED '+archive);
  } finally { fs.rmdirSync(guard); }
}
try{recover();}catch(e){console.error('STOP: '+e.message);process.exitCode=1;}
