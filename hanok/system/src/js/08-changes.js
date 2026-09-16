/* ============================================================
   변동 이력 — 사장님의 '파란 글씨' 습관을 옮긴 것

   수기 장부에서는 나중에 바뀐 예약을 파란 펜으로 표시했습니다.
   장부 원본을 고칠 수 없으니 "이 줄은 검정 그대로 믿지 마라"는 표시였습니다.
   화면은 항상 최신값을 보여주므로 그 문제 자체는 없지만,
   **아직 최신이 아닌 곳**이 남아 있습니다 — 주방에 구두로 넘긴 코스 수량,
   직원이 머리로 기억하는 자리 배치.
   그래서 "값"이 아니라 "무엇이 언제 바뀌었는지"를 남깁니다.

   표시 조건은 **방문일 당일에 일어난 변동**입니다.
   어제 미리 바꾼 것은 오늘 아침에 이미 반영돼 있으므로 제외합니다.
   날짜가 넘어가면 자연히 정리되므로 따로 지우는 동작이 필요 없습니다.
   ============================================================ */

/* 변동으로 볼 항목. 여기 없는 것(예약경로 등)은 기록하지 않습니다 —
   손님 응대나 자리 배치에 영향이 없어 표시하면 소음만 됩니다. */
var CHANGE_FIELDS = [
  {k:"date",     n:"날짜",   f:function(v){ return v ? dateLabel(v) : "-"; }},
  {k:"time",     n:"시간",   f:function(v){ return v ? hm(v) : "-"; }},
  {k:"people",   n:"인원",   f:function(v){ return (v||0)+"명"; }},
  {k:"infants",  n:"어린이",   f:function(v){ return (v||0)+"명"; }},
  {k:"chairs",   n:"유아의자", f:function(v){ return (v||0)+"개"; }},
  {k:"roomId",   n:"좌석",   f:function(v){ return v ? seatLabel(v) : "미배정"; }},
  {k:"seatPref", n:"좌석 희망", f:function(v){ return v ? seatLabel(v) : "-"; }},   /* 지하 → 1층 처럼 층만 바꾼 것도 변동입니다(11월 점검) */
  {k:"menuType", n:"식사",   f:function(v){ return v || "-"; }},
  {k:"request",  n:"요청",   f:function(v){ return v || "없음"; }},
  {k:"allergy",  n:"알러지", f:function(v){ return v || "없음"; }},
  {k:"memo",     n:"메모",   f:function(v){ return v || "없음"; }}
];

/* 두 예약을 비교해 바뀐 항목만 뽑습니다 */
function diffRes(a, b){
  var out = [], i;
  for(i=0;i<CHANGE_FIELDS.length;i++){
    var c = CHANGE_FIELDS[i];
    var x = a ? a[c.k] : undefined, y = b ? b[c.k] : undefined;
    if((x||"") === (y||"")) continue;
    if((x||0) === (y||0) && typeof x !== "string") continue;
    out.push({n:c.n, a:c.f(x), b:c.f(y)});
  }
  /* 코스는 개수 묶음이라 따로 비교합니다 */
  var ca = courseSummary(a && a.courses) || (a && a.courseUndecided ? "미정" : "");
  var cb = courseSummary(b && b.courses) || (b && b.courseUndecided ? "미정" : "");
  if(ca !== cb) out.push({n:"코스·세트", a:ca||"없음", b:cb||"없음"});
  return out;
}

/* 이력 한 줄을 남깁니다. on 은 '그날 날짜'(현지 기준) — at 만 쓰면 시차 때문에 어긋납니다 */
function addChange(rec, kind, items){
  if(!rec) return rec;
  var log = (rec.changes || []).slice();
  log.push({ on: todayStr(), at: new Date().toISOString(), kind: kind, items: items || [] });
  if(log.length > 40) log = log.slice(-40);   /* 한 예약이 무한정 커지지 않게 */
  rec.changes = log;
  touch(rec);
  return rec;
}

/* 방문일 당일에 일어난 변동만. 등록은 '그날 받은 당일 예약'일 때만 포함합니다 */
function todayChanges(r){
  var log = r.changes || [], out = [], i;
  for(i=0;i<log.length;i++){
    if(log[i].on !== r.date) continue;
    out.push(log[i]);
  }
  return out;
}
/* 목록·타임라인에 붙일 짧은 표시. 없으면 null */
function changeTag(r){
  /* 파란 표시는 '오늘' 예약에만 — 오늘 바뀐 것을 놓치지 않으려는 표시라서. 다른 날짜는 상세의 '바뀐 내용' 에만 남깁니다(재아) */
  if(r.date !== todayStr()) return null;
  var cs = todayChanges(r);
  if(!cs.length) return null;
  var kinds = {}, items = {}, i, j;
  for(i=0;i<cs.length;i++){
    kinds[cs[i].kind] = 1;
    for(j=0;j<(cs[i].items||[]).length;j++) items[cs[i].items[j].n] = 1;
  }
  /* 취소·노쇼가 가장 중요합니다 — 자리를 비워야 하는 건이라. 단, 그 뒤에 다시 확정으로 되돌렸으면(상태 변경) 취소가 아닙니다 */
  var lastStatus = null;
  for(i=0;i<cs.length;i++){
    if(cs[i].kind==="취소" || cs[i].kind==="노쇼") lastStatus = cs[i].kind;
    else if(cs[i].kind==="변경" && (cs[i].items||[]).some(function(x){ return x.n==="상태"; })) lastStatus = null;
  }
  var kind = lastStatus ? lastStatus : kinds["등록"] ? "신규" : "변경";
  var names = Object.keys(items);
  /* 상태 태그(취소/노쇼)가 이미 옆에 붙으므로 '오늘' 을 넣어 구분합니다.
     지난주에 취소된 건과 오늘 취소된 건은 대응이 완전히 다릅니다. */
  var label = kind==="취소" ? "오늘 취소"
            : kind==="노쇼" ? "오늘 노쇼"
            : kind==="신규" ? "당일 접수"
            : "변경" + (names.length ? " · " + names.join("·") : "");
  return { kind: kind, fields: names, label: label };
}
/* 예약 상세에 펼쳐 보여줄 전체 이력 (그날 것만, 최근이 위로) */
/* 처음부터의 이력 — 날짜까지 붙여서 */
function changeLinesAll(r){
  var cs = (r.changes || []).slice().reverse(), out = [], i, j;
  for(i=0;i<cs.length;i++){
    var c = cs[i], d = c.at ? new Date(c.at) : null;
    var t = d && !isNaN(d) ? (d.getMonth()+1)+"/"+d.getDate()+" "+pad(d.getHours())+":"+pad(d.getMinutes()) : (c.on || "");
    if(c.kind === "등록"){ out.push({t:t, s:"예약 접수"}); continue; }
    if(c.kind === "취소"){ out.push({t:t, s:"예약 취소"}); continue; }
    if(c.kind === "노쇼"){ out.push({t:t, s:"노쇼 처리"}); continue; }
    if(!(c.items||[]).length){ out.push({t:t, s:"수정"}); continue; }
    for(j=0;j<c.items.length;j++) out.push({t:t, s:c.items[j].n + (c.items[j].a != null ? " " + c.items[j].a + " → " + c.items[j].b : "")});
  }
  return out;
}
