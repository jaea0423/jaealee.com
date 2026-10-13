'use strict';
// Credentials stay in ~/.config/yb; curl receives headers on stdin, never argv.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {execFileSync}=require('node:child_process');
const ENDPOINT='https://kwqxvkkscgxhdscuyuyy.supabase.co/rest/v1/rpc/upload_news';
const PRIVATE=path.join(os.homedir(),'.config','yb');
function redact(value,secrets){let s=String(value??'');for(const secret of secrets)if(secret)s=s.split(secret).join('[REDACTED]');return s.slice(0,600);}
function interpret(body,http,date,secrets=[]){
 let data;try{data=JSON.parse(body);}catch{return{ok:false,error:redact(`HTTP ${http}: 응답이 JSON이 아닙니다. ${body}`,secrets)};}
 if(http>=200&&http<300&&data?.ok===true&&data.date===date)return{ok:true};
 return{ok:false,error:redact(data?.message||data?.error||data?.details||`HTTP ${http}: 성공 응답 또는 날짜 불일치`,secrets)};
}
function configQuote(v){if(/[\r\n\0]/.test(v))throw new Error('인증 설정 형식 오류');return '"'+v.replaceAll('\\','\\\\').replaceAll('"','\\"')+'"';}
function upload(file){
 const result={date:path.basename(file,'.json'),file:path.relative(process.cwd(),file),checkedAt:new Date().toISOString(),ok:false};let secrets=[];
 try{
  const doc=JSON.parse(fs.readFileSync(file,'utf8'));if(!/^\d{4}-\d{2}-\d{2}$/.test(doc.date)||doc.date!==result.date)throw new Error('JSON 날짜와 파일명 불일치');
  const tokenPath=path.join(PRIVATE,'news_token');if((fs.statSync(tokenPath).mode&0o777)!==0o600)throw new Error('업로드 키 파일 권한은 600이어야 합니다.');
  const token=fs.readFileSync(tokenPath,'utf8');secrets.push(token);if(!token||/[\r\n\0]/.test(token))throw new Error('업로드 키 파일 형식 오류');
  const cfg=JSON.parse(fs.readFileSync(path.join(PRIVATE,'news_upload.json'),'utf8'));secrets.push(cfg.apikey);if(cfg.endpoint!==ENDPOINT||!cfg.apikey)throw new Error('포털 API 설정 오류');
  const config=['silent','show-error','request = "POST"','url = '+configQuote(ENDPOINT),'header = '+configQuote('apikey: '+cfg.apikey),'header = "Content-Type: application/json"','header = '+configQuote('x-news-token: '+token)].join('\n')+'\n';
  const raw=execFileSync('/usr/bin/curl',['--config','-','--connect-timeout','10','--max-time','30','--data-binary','@'+path.resolve(file),'--write-out','\n%{http_code}'],{input:config,encoding:'utf8',timeout:35000,stdio:['pipe','pipe','pipe'],maxBuffer:2*1024*1024});
  const separator=raw.lastIndexOf('\n');result.http=Number(raw.slice(separator+1));Object.assign(result,interpret(raw.slice(0,separator),result.http,doc.date,secrets));
 }catch(e){result.error=redact(e.stderr?.toString()||e.message,secrets);}
 try{
  fs.mkdirSync(PRIVATE,{recursive:true});const log=path.join(PRIVATE,'news-upload-results.jsonl');const fd=fs.openSync(log,'a',0o600);fs.fchmodSync(fd,0o600);try{fs.writeSync(fd,JSON.stringify(result)+'\n');}finally{fs.closeSync(fd);}
 }catch{result.logError='비공개 업로드 결과 기록 실패';}
 return result;
}
module.exports={redact,interpret,configQuote,upload};
if(require.main===module){
 const args=process.argv.slice(2);let files;
 if(args.includes('--all'))files=fs.readdirSync('news/data').filter(f=>f.endsWith('.json')).sort().map(f=>path.join('news/data',f));
 else files=args.filter(a=>!a.startsWith('--'));
 if(args.includes('--report')){const i=args.indexOf('--report');if(!args[i+1])throw new Error('--report 경로 필요');if(!args.includes('--all'))files=files.filter(f=>f!==args[i+1]);}
 const results=[];
 for(const file of files){const r=upload(file);results.push(r);console.log(JSON.stringify(r));}
 if(args.includes('--report')){const target=args[args.indexOf('--report')+1];fs.mkdirSync(path.dirname(path.resolve(target)),{recursive:true});fs.writeFileSync(target,JSON.stringify({results,success:results.filter(r=>r.ok).length,failed:results.filter(r=>!r.ok).map(r=>r.date)},null,2)+'\n');}
 console.log(JSON.stringify({total:results.length,success:results.filter(r=>r.ok).length,failed:results.filter(r=>!r.ok).map(r=>r.date)}));
 // Portal failure must not abort the independent jaealee.com publication.
}
