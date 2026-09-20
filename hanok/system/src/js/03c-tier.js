/* ---------- 단골 등급 (16차, 재아) ----------
   점수 = 방문 횟수 − 노쇼 × 5.  점수 2 이상 VIP, 5 이상 VVIP. 전화번호(숫자만) 기준으로 예약 기록에서 셉니다.
   TV(공개 뷰)는 전화번호가 없으니 서버가 같은 규칙(hanok_tier)으로 계산해 tier 열로 줍니다 — 숫자를 바꾸면 SQL 도 같이.
   예약 이름 옆 알약(tierTag)·손님 목록·마법사 손님 단계·TV 에서 씁니다. */
var TIER_VIP = 2, TIER_VVIP = 5, TIER_NOSHOW = 5;
var CUST_IDX = null, CUST_IDX_KEY = "", RES_VER = 0;   /* RES_VER 은 저장·동기화 때 올라감 → 그때만 다시 셈 */
function tierOf(visit, noshow){ var s = visit - TIER_NOSHOW * noshow; return s >= TIER_VVIP ? "VVIP" : s >= TIER_VIP ? "VIP" : ""; }
function custIndex(){
  var s = store(); if(!s) return {};
  var key = RES_VER + "|" + s.reservations.length + "|" + (view.storeKey || "");
  if(CUST_IDX && CUST_IDX_KEY === key) return CUST_IDX;
  var idx = {};
  s.reservations.forEach(function(r){
    var d = String(r.phone || "").replace(/\D/g, ""); if(d.length < 8) return;
    var g = idx[d] || (idx[d] = { visit:0, noshow:0, total:0 });
    g.total++; if(r.status === "방문") g.visit++; else if(r.status === "노쇼") g.noshow++;
  });
  Object.keys(idx).forEach(function(k){ var g = idx[k]; g.score = g.visit - TIER_NOSHOW * g.noshow; g.tier = tierOf(g.visit, g.noshow); });
  CUST_IDX = idx; CUST_IDX_KEY = key; return idx;
}
/* 전화번호(또는 예약 객체) → {visit, noshow, score, tier, memo, name} */
function custStat(x){
  var phone = x && typeof x === "object" ? x.phone : x;
  var d = String(phone || "").replace(/\D/g, "");
  var g = (d.length >= 8 && custIndex()[d]) || { visit:0, noshow:0, total:0, score:0, tier:"" };
  var c = typeof custOf === "function" ? custOf(d) : null;
  return { visit:g.visit, noshow:g.noshow, total:g.total, score:g.score, tier:g.tier, memo:(c && c.memo) || "", fixedName:(c && c.name) || "" };
}
/* 이름 옆 알약. TV 처럼 tier 문자열만 있을 때는 tierTagOf */
function tierTag(x){ return tierTagOf(custStat(x).tier); }
/* 단체 딱지(09-20 재아) — 설정 groupSize(기본 8명) 이상. 예약 객체를 받음 */
function groupTag(r){ return r && pplOf(r) >= (store().settings.groupSize || 8) ? '<span class="tier grp" title="단체">단체</span>' : ""; }
function tierTagOf(t){ return t === "VVIP" ? '<span class="tier vvip" title="VVIP — 방문 5회 이상">VVIP</span>' : t === "VIP" ? '<span class="tier vip" title="VIP — 방문 2회 이상">VIP</span>' : ""; }
