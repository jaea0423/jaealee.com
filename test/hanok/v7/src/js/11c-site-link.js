/* ---------- 홈페이지 연동 (Supabase 가 켜져 있을 때만) ----------
   ① 남은 자리 올리기: 내일부터 30일치를 계산해 public_avail 에 upsert. 홈페이지는 이 표만 읽습니다.
      계산은 여기(v7)가 이미 하는 것 그대로 — roomStatus·floorMaxParty. SQL 로 다시 짜지 않습니다.
      부르는 때: 저장 뒤(flush) · 1분 갱신 · 설정 적용. 너무 자주 안 올리게 45초 간격으로 묶습니다.
   ② 홈페이지 예약 읽기: requests 표에서 '대기' 를 가져와 REQUESTS 에 맞춥니다(11b 의 흉내 REQ_API 를 덮어씀).
      새로 보이는 것은 reqNotify 로 팝업. 24시간 지난 것은 '만료' 로 PATCH.
   supaOn() 이 아니면(로컬·데모) 아무것도 안 하고 11b 의 흉내가 그대로 돕니다. */
var AVAIL_LAST = 0, AVAIL_BUSY = false, AVAIL_DIRTY = false, AVAIL_DAYS = 30;

/* 하루치 남은 자리 — {"11:00":{"rooms":[[min,max],…],"tableMax":n}, …} */
function availOfDay(date){
  const out = {}, ss = sessionsFor(date); if(!ss.length) return out;
  const rooms = roomsAt(date).filter(isRoom);
  const floors = []; roomsAt(date).filter(isTable).forEach(t => { const f = t.floor || ""; if(floors.indexOf(f) < 0) floors.push(f); });
  ss.forEach(se => {
    const from = toMin(se.from), last = toMin(se.lastBook);
    for(let m = from; m <= last; m += 30){
      const time = minToHM(m);
      if(inBreak(date, time)) continue;
      /* 잠정 배정(미배정 예약이 임시로 잡은 방)도 찬 것으로 — findSeat 의 free 판정과 같게. state 만 보면 '비켜줄 수 있는' 잠정이 있는 방이
         빈 방으로 세어져 홈페이지에 실제보다 방이 많아 보였습니다 */
      const free = rooms.filter(x => { if(blockedAt(x, date, time)) return false; const rs = roomStatus(date, time, x.id); return rs.state === "free" && !rs.tentative.length && !rs.movable.length; })
                        .map(x => [roomMin(x, date), seatMax(x)]);
      let tableMax = 0; floors.forEach(f => { tableMax = Math.max(tableMax, floorMaxParty(f, date, time)); });
      out[time] = { rooms: free, tableMax: tableMax };
    }
  });
  return out;
}
async function publishAvail(force){
  if(!supaOn() || !SESSION || OFFLINE || !DATA || DATA._readonly) return;
  if(!force && Date.now() - AVAIL_LAST < 45000){ AVAIL_DIRTY = true; return; }
  if(AVAIL_BUSY){ AVAIL_DIRTY = true; return; }
  AVAIL_BUSY = true;
  try{
    const key = view.storeKey || "hanok", today = todayStr(), rows = [];
    for(let i = 1; i <= AVAIL_DAYS; i++){ const d = shiftDate(today, i); rows.push({ store:key, date:d, data:availOfDay(d) }); }
    await sb("/rest/v1/public_avail?on_conflict=store,date", { method:"POST", body:rows, prefer:"resolution=merge-duplicates,return=minimal" });
    AVAIL_LAST = Date.now(); AVAIL_DIRTY = false;
  }catch(e){ console.error("남은 자리 올리기 실패", e.message); }
  finally{ AVAIL_BUSY = false; }
}

/* ---------- requests ↔ REQUESTS ---------- */
const rowToReq = function(x){
  return { id:x.id, createdAt:x.created_at, date:x.date, time:x.time, adults:x.adults, kids:x.kids, people:x.people, seat:x.seat,
           course:x.course, courseLabel:x.course_label, name:x.name, phone:phoneFmtReq(x.phone), request:x.request||"",
           status:x.status, reason:x.reason||"", resId:x.res_id||null, expiresAt:x.expires_at };
};
function phoneFmtReq(p){ const d = String(p||"").replace(/\D/g,""); return d.length >= 10 ? d.replace(/(\d{3})(\d{3,4})(\d{4})/, "$1-$2-$3") : d; }
async function pullRequests(){
  if(!supaOn() || !SESSION || OFFLINE) return;
  const key = view.storeKey || "hanok";
  let rows;
  try{ rows = await sb("/rest/v1/requests?store=eq." + key + "&status=eq.%EB%8C%80%EA%B8%B0&select=*&order=created_at"); }
  catch(e){ console.error("홈페이지 예약 읽기 실패", e.message); return; }
  const now = Date.now(), fresh = [], seen = {};
  for(const x of rows){
    const q = rowToReq(x); seen[q.id] = 1;
    if(new Date(q.expiresAt).getTime() <= now){   /* 만료 → 서버에도 표시 */
      try{ await sb("/rest/v1/requests?id=eq." + encodeURIComponent(q.id), { method:"PATCH", body:{status:"만료", reason:"24시간 안에 처리되지 않음"}, prefer:"return=minimal" }); }catch(e){}
      continue;
    }
    const i = REQUESTS.findIndex(r => r.id === q.id);
    if(i < 0){ REQUESTS.push(q); fresh.push(q); } else REQUESTS[i] = q;
  }
  /* 서버에서 사라진(다른 기기가 처리한) 것은 목록에서 뺌 */
  for(let i = REQUESTS.length - 1; i >= 0; i--) if(REQUESTS[i].status === "대기" && !seen[REQUESTS[i].id]) REQUESTS.splice(i, 1);
  if(fresh.length && REQ_SEEN_INIT) reqNotify(fresh); else fresh.forEach(q => { REQ_SEEN[q.id] = true; });
  REQ_SEEN_INIT = true;
  return fresh.length;
}
var REQ_SEEN_INIT = false;   /* 처음 불러온 것은 '새로 들어온 것' 이 아니므로 팝업을 안 띄웁니다 */

/* 11b 의 흉내 API 를 서버 것으로 덮어씀 (supaOn 일 때만) */
if(typeof supaOn === "function" && supaOn()){
  REQ_API.list = async () => { await pullRequests(); return reqPending(); };
  REQ_API.accept = async (id, resId) => {
    await sb("/rest/v1/requests?id=eq." + encodeURIComponent(id), { method:"PATCH", body:{status:"확정", res_id:resId}, prefer:"return=minimal" });
    const q = REQUESTS.find(x => x.id === id); if(q){ q.status = "확정"; q.resId = resId; }
    return {ok:true};
  };
  REQ_API.reject = async (id, why) => {
    await sb("/rest/v1/requests?id=eq." + encodeURIComponent(id), { method:"PATCH", body:{status:"거절", reason:why}, prefer:"return=minimal" });
    const q = REQUESTS.find(x => x.id === id); if(q){ q.status = "거절"; q.reason = why; }
    return {ok:true};
  };
}
