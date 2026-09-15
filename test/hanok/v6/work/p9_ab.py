# -*- coding: utf-8 -*-
"""8차-AB — 재아: '확인 필요' → '확인', 좌석 꼬리표 통일('장비 룸(잠정)' · '1층 테이블 · 21(잠정)', 잠정은 경고색 아님·자리 없음만 붉게),
   비상예약지는 새 탭 + 전체화면이었으면 '다시 전체화면' 팝업"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 좌석 꼬리표 통일 ----------
s = R(s, """/* 룸 미배정(잠정 포함) 여부 — 테이블 예약은 층이 자리이므로 미배정으로 세지 않습니다 */""",
"""/* 확인 시트·검색·상세에 쓰는 좌석 꼬리표(8차-AB 재아) — 잠정도 '배정된 것' 이라 붉게 쓰지 않습니다. 붉은색은 자리가 정말 없을 때만.
   확정 룸/테이블 → 'pine', 잠정 → 색 없음 '장비 룸(잠정)' / '1층 테이블 · 21(잠정)', 자리 없음 → 'rust' */
function seatTag(r){
  var t = seatTagText(r);
  return '<span class="tag ' + (r.roomId ? "pine" : (t.ok ? "" : "rust")) + '">' + esc(t.text) + '</span>';
}
function seatTagText(r){
  if(r.roomId) return { ok:true, text:resSeatLabel(r) };
  var names = r.tentativeRoomId ? seatsOf(r).map(function(id){ var x = seatById(id); return x ? x.name : ""; }).filter(Boolean) : [];
  if(isTablePref(r.seatPref)){
    var fl = prefFloor(r.seatPref), head = fl ? floorLabel(fl) : "테이블 (층 상관없음)";
    return names.length ? { ok:true, text: head + " · " + names.join("+") + (r.tentativeSplit ? " 나눠" : "") + "(잠정)" } : { ok:false, text: head + " · 자리 없음" };
  }
  return names.length ? { ok:true, text: seatLabelIds(names.length ? [r.tentativeRoomId].concat(r.tentativeExtra||[]) : []) + "(잠정)" } : { ok:false, text:"미배정" };
}
/* 룸 미배정(잠정 포함) 여부 — 테이블 예약은 층이 자리이므로 미배정으로 세지 않습니다 */""")
# 상세
s = R(s, """  const seat = r.roomId ? resSeatLabel(r)
             : isTablePref(r.seatPref) ? resSeatLabel(r)
             : (r.tentativeRoomId ? `미배정 (${resTentLabel(r)} 잠정)` : "미배정");
  const srcTxt""", """  const seat = seatTagText(r).text;   /* '장비 룸(잠정)' · '1층 테이블 · 21(잠정)' (재아) */
  const srcTxt""")
# 확인 시트(알러지·경고·단체 …)
s = R(s, """      <span class="tag ${r.roomId?'pine':'rust'}">${r.roomId?esc(resSeatLabel(r)):"미배정"}</span>
    </button>`).join("") : `<div class="empty">해당 예약이 없습니다.</div>`;""",
"""      ${seatTag(r)}
    </button>`).join("") : `<div class="empty">해당 예약이 없습니다.</div>`;""")
# 미배정 시트
s = R(s, """          <span class="rm tag ${room?'pine':(r.tentativeRoomId?'amber':'rust')}">${
            room ? esc(resSeatLabel(r))
                 : (r.tentativeRoomId ? `미배정 · ${esc(resTentLabel(r))}(잠정)` : "미배정")}</span>""",
"""          ${seatTag(r).replace('class="tag', 'class="rm tag')}""")
# 검색
s = R(s, """        <span class="tag ${r.roomId?'pine':'amber'}">${r.roomId?esc(resSeatLabel(r)):"미배정"}</span>
      </button>`).join("")
      : `<div class="empty">찾은 예약이 없습니다.</div>`;""",
"""        ${seatTag(r)}
      </button>`).join("")
      : `<div class="empty">찾은 예약이 없습니다.</div>`;""")

# ---------- '확인 필요' → '확인' (메뉴 종류 값 '확인 필요' 는 데이터라 그대로) ----------
s = R(s, """          <div class="k">확인 필요</div></button>""", """          <div class="k">확인</div></button>""")
s = R(s, """    ${sheetHead(`확인 필요 · ${dateLabel(view.date)}`)}""", """    ${sheetHead(`확인 · ${dateLabel(view.date)}`)}""")
s = R(s, """onclick="openCheck()">확인 필요 ${chk}건</button>`;""", """onclick="openCheck()">확인 ${chk}건</button>`;""")
s = R(s, """  if(menuChk.length) items.push(["amber", `메뉴 확인 필요 ${menuChk.length}건`,""", """  if(menuChk.length) items.push(["amber", `메뉴 확인 ${menuChk.length}건`,""")
s = R(s, """    menu:{title:"메뉴 확인 필요", pick:""", """    menu:{title:"메뉴 확인", pick:""")
s = R(s, """<div class="f-note">이 인원부터 확인 필요에 ‘단체 손님’으로 뜹니다.</div>""", """<div class="f-note">이 인원부터 확인에 ‘단체 손님’으로 뜹니다.</div>""")
s = R(s, """저장해도 됩니다. 대신 '경고 예약'으로 남아 확인 필요에 뜹니다.",""", """저장해도 됩니다. 대신 '경고 예약'으로 남아 확인에 뜹니다.",""")
s = R(s, """<b>경고 예약</b>으로 남아 확인 필요에 뜹니다. 자리를 옮기려면""", """<b>경고 예약</b>으로 남아 확인에 뜹니다. 자리를 옮기려면""")
s = R(s, """대신 '경고 예약'으로 남아 확인 필요에 뜹니다.",
      {ok""", """대신 '경고 예약'으로 남아 확인에 뜹니다.",
      {ok""")

# ---------- 비상예약지: 새 탭 + 전체화면 복귀 팝업 ----------
s = R(s, """      <a class="btn" href="${location.pathname.indexOf('/dev/')>=0?'../':''}비상예약지.html" target="_blank" rel="noopener">비상 예약지 인쇄</a>""",
         """      <button class="btn" onclick="openSlip()">비상 예약지 인쇄</button>""")
s = R(s, """function toggleFullscreen(){""",
"""/* 비상 예약지를 새 탭에 — 새 탭이 열리면 전체화면이 풀리므로, 전체화면이었다면 돌아와서 다시 켤 버튼을 띄웁니다(재아).
   전체화면은 손짓이 있어야 켜져서 팝업 버튼을 누르는 순간에 요청합니다 */
async function openSlip(){
  var wasFs = !!document.fullscreenElement;
  window.open((location.pathname.indexOf('/dev/') >= 0 ? '../' : '') + '비상예약지.html', '_blank', 'noopener');
  if(!wasFs) return;
  if(await uiConfirm("비상 예약지를 새 탭에 열었습니다", "새 탭이 열리면서 전체화면이 풀립니다.\\n인쇄하고 돌아오면 아래 버튼으로 다시 켜세요.", {ok:"다시 전체화면", cancel:"그냥 두기", tone:"ok"})) tryFullscreenForce();
}
function toggleFullscreen(){""")

L.js_check(s)
L.save(s)
print("p9_ab 적용")
