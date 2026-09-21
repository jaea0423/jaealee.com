const fs=require('fs'),os=require('os'),path=require('path'),{execFileSync,spawnSync}=require('child_process'),assert=require('assert/strict');
const script=path.join(__dirname,'recover.cjs');
for(const scenario of ['archive','active','unrelated','staged','unpublished','remote-conflict','existing']){
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'daily-recovery-test-'));const remote=path.join(temp,'remote.git'),repo=path.join(temp,'repo');
 const run=(cwd,...a)=>execFileSync('git',a,{cwd,stdio:['ignore','pipe','pipe']}).toString().trim();
 run(temp,'init','--bare',remote);run(temp,'clone',remote,repo);run(repo,'checkout','-b','main');run(repo,'config','user.email','test@example.invalid');run(repo,'config','user.name','Test');fs.mkdirSync(path.join(repo,'news/data'),{recursive:true});fs.writeFileSync(path.join(repo,'news/index.json'),'original\n');
 if(scenario==='existing')fs.writeFileSync(path.join(repo,'news/data/2026-09-17.json'),'old\n');
 run(repo,'add','.');run(repo,'commit','-m','base');run(repo,'push','origin','main');const base=run(repo,'rev-parse','HEAD');
 fs.mkdirSync(path.join(repo,'.git/daily-publish.lock'));fs.writeFileSync(path.join(repo,'.git/daily-publish.lock/state.json'),JSON.stringify({date:'2026-09-17',phase:'prepared',base,existing:scenario==='existing'?['news/data/2026-09-17.json']:[]}));
 fs.writeFileSync(path.join(repo,'news/index.json'),'draft index\n');fs.writeFileSync(path.join(repo,'news/data/2026-09-17.json'),'draft article\n');
 if(scenario==='unrelated')fs.writeFileSync(path.join(repo,'ui.html'),'keep');
 if(scenario==='staged')run(repo,'add','news/index.json');
 if(scenario==='unpublished'){run(repo,'add','.');run(repo,'commit','-m','unpublished');}
 if(scenario==='remote-conflict'){const other=path.join(temp,'other');run(temp,'clone','-b','main',remote,other);run(other,'config','user.email','test@example.invalid');run(other,'config','user.name','Test');fs.writeFileSync(path.join(other,'news/index.json'),'remote\n');run(other,'add','.');run(other,'commit','-m','remote');run(other,'push','origin','main');}
 const result=spawnSync(process.execPath,[script,...(scenario==='active'?[]:['--previous-run-inactive'])],{cwd:repo,encoding:'utf8'});
 if(scenario==='archive'){assert.equal(result.status,0,result.stderr);assert.equal(run(repo,'status','--porcelain'),'');const dir=fs.readdirSync(path.join(repo,'.git/daily-recovery-archives'))[0];assert.equal(fs.readFileSync(path.join(repo,'.git/daily-recovery-archives',dir,'draft/news/data/2026-09-17.json'),'utf8'),'draft article\n');assert(!fs.existsSync(path.join(repo,'.git/daily-publish.lock')));}else{assert.notEqual(result.status,0);assert(fs.existsSync(path.join(repo,'.git/daily-publish.lock/state.json')));assert.equal(fs.readFileSync(path.join(repo,'news/data/2026-09-17.json'),'utf8'),'draft article\n');}
 console.log('PASS '+scenario);
}
