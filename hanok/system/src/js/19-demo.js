/* ============================================================
   예시 데이터 — 처음 실행할 때만 채웁니다 (설정에서 지울 수 있음)
   ============================================================ */
function seedDemo(d){
  const today = todayStr();
  const rooms = d.hanok.settings.rooms;
  const pick = function(n){ const r=rooms.find(function(x){return x.name===n;}); return r?r.id:null; };
  /* ---------- 예약 예시 ----------
     운영시간·룸 정원·코스 규칙을 지켜서 만듭니다 (경고 없는 정상 예약).
     요일별로 쓸 수 있는 시각만 골라 씁니다. */
  const ROOMS = [
    {n:"조조", min:2, max:4}, {n:"유비", min:2, max:4}, {n:"장비", min:2, max:4},
    {n:"관우", min:4, max:6}, {n:"공명", min:4, max:6}, {n:"주유", min:4, max:6},
    {n:"초선", min:6, max:8}, {n:"동탁", min:8, max:10}
  ];
  const HALLS = ["1층 홀","저층 홀"];
  /* 룸(체류 3h)·홀(2.5h) 모두 안전한 시각만 사용 */
  const SLOTS = {
    0: {lunch:["11:30","12:00","12:30","13:00"], dinner:["17:00","17:30"]},           /* 일 20:30 마감 */
    6: {lunch:["11:30","12:00","12:30","13:00"], dinner:["17:00","17:30","18:00","18:30","19:00"]},
    x: {lunch:["11:30","12:00","12:30","13:00"], dinner:["17:00","17:30","18:00","18:30","19:00"]}
  };
  /* 코스 구성 — 시간대에 맞는 줄에서 고릅니다 */
  const COURSE_BY = (lunch, weekend) =>
    lunch ? (weekend ? ["cg_welunch|요리사","cg_welunch|B","cg_welunch|A"] : ["cg_wdlunch|요리사","cg_wdlunch|동한","cg_wdlunch|서한"])
          : ["cg_dinner|오","cg_dinner|촉","cg_dinner|한","cg_dinner|위"];

  const names = ["김하람","이도현","박수빈","정우성","최유나","한서진","오지호","배소민",
                 "신태호","권나연","황준서","문가영","서동우","임하경","조성민","윤지완",
                 "남기범","홍세아","유정민","곽태영","심다혜","방준혁","노아린","전승우",
                 "박서준","이재아","조은결","최민서","윤소라","김도윤","정하늘","한지호"];
  const nsPool = ["010-3300-1188","010-9042-7761","010-8834-2205"];
  const nsNames = ["차민석","임세연","고은비"];

  let gi = 0;
  const mkRes = (ds, opt, used) => {
    const dow = new Date(ds+"T00:00:00").getDay();
    const weekend = dow===0 || dow===6;
    const slots = SLOTS[dow] || SLOTS.x;
    const lunch = opt.lunch;
    const time = (lunch ? slots.lunch : slots.dinner)[gi % (lunch?slots.lunch.length:slots.dinner.length)];
    const useRoom = opt.room;
    let people, roomName, courses = {}, menuType = "해당 없음", infants = 0;

    if(useRoom){
      /* 같은 시각에 이미 쓰는 룸은 건너뜁니다 */
      let rm = null;
      for(let i=0;i<ROOMS.length;i++){
        const cand = ROOMS[(gi*5 + i) % ROOMS.length];
        if(!used[time+"|"+cand.n]){ rm = cand; break; }
      }
      if(!rm) return null;                 /* 그 시각 룸이 다 찼으면 건너뜀 */
      used[time+"|"+rm.n] = true;
      roomName = rm.n;
      people = rm.min + ((gi*3) % (rm.max - rm.min + 1));
      if(gi % 11 === 0 && people >= rm.min + 2) infants = 1;   /* 어린이가 있어도 성인이 최소 인원 이상 */
      const adults = people - infants;
      const pool = COURSE_BY(lunch, weekend);
      menuType = "코스";
      courses[pool[gi % pool.length]] = adults;                /* 코스 인원 = 성인 수 */
    }else{
      roomName = HALLS[gi % HALLS.length];
      people = [2,3,4,4,5,6,8][(gi*3) % 7];
      if(gi % 13 === 0 && people >= 3) infants = 1;
      menuType = "해당 없음";
    }
    return {
      id:"demo_"+(gi)+"_"+ds, date:ds, time,
      name: names[gi % names.length],
      phone:"010-"+pad(2000+((gi*37)%7999)).slice(0,4)+"-"+pad(1000+((gi*53)%8999)).slice(0,4),
      people, infants, chairs:infants,
      roomId: pick(roomName), seatPref:null, tentativeRoomId:null,
      source: gi%4===0 ? "네이버예약" : "전화", sourceDetail:"",
      createdAt: new Date(new Date(ds+"T00:00:00").getTime() - (3+(gi%9))*86400000).toISOString(),
      menuType, courses, courseUndecided:false,
      request: gi%17===0 ? "창가 자리 부탁드립니다" : "",
      allergy: gi%23===0 ? "땅콩 알러지" : "",
      status:"확정", demo:true
    };
  };

  const [yy] = today.split("-").map(Number);
  for(let mo=7; mo<=10; mo++){
    const lastDay = new Date(yy, mo, 0).getDate();
    for(let day=1; day<=lastDay; day++){
      const ds = `${yy}-${pad(mo)}-${pad(day)}`;
      if(mo===10 && day>12) continue;
      const dow = new Date(ds+"T00:00:00").getDay();
      let cnt = (dow===5||dow===6) ? 15 : (dow===0 ? 12 : 9);
      if(ds===today) cnt = 16;
      if(mo===10) cnt = Math.max(1, Math.round(cnt*0.45));
      const used = {};
      for(let k=0;k<cnt;k++,gi++){
        const rec = mkRes(ds, {lunch: k%2===0, room: k%5<3}, used);   /* 5건 중 3건은 룸, 2건은 홀 */
        if(!rec) continue;
        /* 지난 날짜는 대부분 방문, 가끔 노쇼·취소 (어제는 확정으로 남겨 자동 처리 확인) */
        if(ds < today && ds !== shiftDate(today,-1)){
          const rr = gi % 23;
          if(rr===0){
            rec.status = "노쇼";
            const ni = Math.floor(gi/7) % nsPool.length;   /* 세 사람에게 고르게 */
            rec.phone = nsPool[ni]; rec.name = nsNames[ni];
          }else if(rr===7){ rec.status = "취소"; }
          else rec.status = "방문";
        }
        d.hanok.reservations.push(rec);
      }
      /* 사장 판단으로 받은 '경고 예약'을 가끔 섞습니다 — 확인 필요 화면 테스트용 */
      if(ds === today || day % 5 === 0){   /* 5일에 한 번쯤 경고 예약이 섞이도록 */
        const kind = gi % 4;
        const w = mkRes(ds, {lunch:false, room:true}, used);
        if(w){
          w.id = "demo_w_"+gi+"_"+ds;
          if(kind===0){
            /* 라스트오더 이후 접수 */
            w.time = dow===0 ? "20:00" : "21:20";
          }else if(kind===1){
            /* 룸인데 코스가 아님 */
            w.menuType = "해당 없음"; w.courses = {};
          }else if(kind===2){
            /* 코스 인원이 성인보다 적음 */
            const keys = Object.keys(w.courses);
            if(keys.length) w.courses[keys[0]] = Math.max(1, w.people - 2);
          }else{
            /* 브레이크타임에 접수 (평일만) */
            if(dow>=1 && dow<=5) w.time = "16:00";
            else { w.menuType = "확인 필요"; w.courses = {}; }
          }
          if(ds < today && ds !== shiftDate(today,-1)) w.status = "방문";
          d.hanok.reservations.push(w);
          gi++;
        }
      }

      /* 좌석 미정 예약을 섞습니다 (오늘·내일은 꼭 몇 건) */
      const wantUn = ds===today ? 2 : (ds===shiftDate(today,1) ? 1 : (gi % 11 === 0 && ds > today ? 1 : 0));
      for(let u=0; u<wantUn; u++, gi++){
        const un = mkRes(ds, {lunch:u%2===0, room:false}, used);
        if(!un) continue;
        un.id = "demo_u_"+gi+"_"+ds; un.roomId = null;
        un.seatPref = u%2===0 ? "room-any" : "table-any";
        un.people = 4; un.infants = 0; un.chairs = 0;
        un.menuType = un.seatPref==="room-any" ? "확인 필요" : "해당 없음";
        un.courses = {};
        d.hanok.reservations.push(un);
      }
    }
  }

  /* 접속 기록 예시 — 형식 확인용 */
  const sampleIPs = ["121.174.22.9","121.174.22.9","203.234.11.87","172.30.1.44"];
  const acts = [
    ["로그인 성공",""],
    ["매장 진입","hanok"],
    ["예약 등록", `${today} 18:30 오세라 12명 동탁 룸 경로:전화`],
    ["상태 변경", `${shiftDate(today,-2)} 18:30 차민석 확정 → 노쇼`],
    ["좌석 배정", `${today} 19:00 이가은 → 관우`],
    ["로그인 실패","입력값 1111"],
    ["설정 변경","stayHours = 3"],
    ["예약 삭제", `${shiftDate(today,-6)} 20:00 김테스트 010-0000-0000`]
  ];
  d._logs = acts.map((a,i)=>({
    ts: new Date(Date.now() - (acts.length-i)*3600000*3).toISOString(),
    ip: sampleIPs[i%sampleIPs.length],
    store: "hanok", action:a[0], detail:a[1],
    ua: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
  }));
  return assignTentatives(d);
}
/* 좌석 미정 예약에 잠정 배정을 붙임 (예시 데이터용) */
function assignTentatives(d){
  const prev = view.storeKey; view.storeKey = "hanok";
  const saved = DATA; DATA = d;
  d.hanok.reservations.filter(r=>!r.roomId && !r.tentativeRoomId).forEach(r=>{
    r.tentativeRoomId = suggestSeat(r.date, r.time, pplOf(r), r.seatPref||"any", r.id);
  });
  DATA = saved; view.storeKey = prev;
  return d;
}
/* 예시 데이터 버튼(넣기·지우기)은 7차-M 에서 뺐습니다 — dev DB 는 work/seed_dev.py 로만 넣습니다 */

loadData();
