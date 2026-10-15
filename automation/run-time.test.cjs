const test=require('node:test'),assert=require('node:assert/strict');
const {runTime,assertDailyReady}=require('./run-time.cjs');
test('05:59 조기 예약은 오늘 날짜를 유지하고 대기하며 prepare를 거부한다',()=>{
 const now=new Date('2026-10-13T20:59:13Z'),s=runTime('daily',now);
 assert.equal(s.date,'2026-10-14');assert.equal(s.action,'wait');assert.equal(s.waitSeconds,47);assert.throws(()=>assertDailyReady(now),/06:00 이전/);
});
test('정확히 06:00 이후에는 한국 달력의 당일을 준비한다',()=>{
 assert.equal(assertDailyReady(new Date('2026-10-13T21:00:00Z')),'2026-10-14');
 assert.equal(assertDailyReady(new Date('2026-10-14T00:34:01Z')),'2026-10-14');
});
test('07:13 조기 점검은 종료 대신 07:15까지 대기한다',()=>{
 const s=runTime('monitor',new Date('2026-10-13T22:13:13Z'));
 assert.equal(s.action,'wait');assert.equal(s.waitSeconds,107);
 assert.equal(runTime('monitor',new Date('2026-10-13T22:15:00Z')).action,'ready');
});
test('다른 점검 시각도 경계 전 대기하며 지연 점검은 즉시 진행한다',()=>{
 assert.equal(runTime('monitor',new Date('2026-10-14T02:13:00Z')).waitSeconds,120);
 assert.equal(runTime('monitor',new Date('2026-10-14T02:16:00Z')).action,'ready');
});
