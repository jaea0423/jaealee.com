// 예약 메시지의 시각 대신 실제 한국 시각으로 실행 경계를 판단합니다.
function runTime(mode, now = new Date()) {
  if (!['daily','monitor'].includes(mode)) throw new Error('daily 또는 monitor가 필요합니다.');
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-CA', {
    timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit',
    hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'
  }).formatToParts(now).map(p=>[p.type,p.value]));
  const date = `${parts.year}-${parts.month}-${parts.day}`;
  const seconds = Number(parts.hour)*3600+Number(parts.minute)*60+Number(parts.second);
  const slots = [7,11,15,19].map(h=>h*3600+15*60);
  let target = mode==='daily' ? 6*3600 : slots[0];
  if(mode==='monitor' && seconds>=slots[0]) {
    target = slots.find(s=>seconds<s && s-seconds<=300) ?? seconds;
  }
  return {mode,date,checkedAt:now.toISOString(),kst:`${parts.hour}:${parts.minute}:${parts.second}`,
    action:seconds<target?'wait':'ready',waitSeconds:Math.max(0,target-seconds)};
}
function assertDailyReady(now=new Date()) {
  const state=runTime('daily',now);
  if(state.action!=='ready') throw new Error(`한국시간 06:00 이전입니다. ${state.waitSeconds}초 후 시각을 재확인하고 prepare를 실행하세요.`);
  return state.date;
}
module.exports={runTime,assertDailyReady};
if(require.main===module) {
  try {console.log(JSON.stringify(runTime(process.argv[2])));}
  catch(e){console.error(e.message);process.exitCode=1;}
}
