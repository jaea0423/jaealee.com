# -*- coding: utf-8 -*-
"""6차-I — 수정 시트 저장 전 확인(saveIssues)이 경고 판정(resWarn)과 어긋나던 것.
   유아를 총 인원까지 올려 저장하면 '경고 예약'이 되는데 확인창은 안 떴습니다 — '성인 없음' 등 5가지가 saveIssues 에 없었음"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
old = """      if(!hallFits(h, ppl)) out.push(`${seat.name}에 ${ppl}명 앉힐 자리가 부족합니다`);
    }
  }
  return out;
}"""
new = """      if(!hallFits(h, ppl)) out.push(`${seat.name}에 ${ppl}명 앉힐 자리가 부족합니다`);
    }
  }
  /* 경고 판정(resWarn)과 같은 기준으로 — 여기서 안 물어본 것이 저장 뒤 '경고 예약'으로 뜨면 사장님이 놀랍니다.
     (재아 발견: 유아를 총 인원까지 올려 저장하니 경고는 붙는데 확인창이 없었음 — '성인 없음' 이 빠져 있었습니다)
     시각·좌석 겹침·정원은 위에서 자세한 문장으로 이미 넣었으므로 나머지만 옮깁니다 */
  const words = {
    "성인 없음": `유아 ${rec.infants||0}명이 총 인원 ${pplOf(rec)}명과 같습니다 — 성인이 없습니다`,
    "유아의자 초과": `유아용 의자 ${rec.chairs||0}개가 유아 ${rec.infants||0}명보다 많습니다`,
    "룸·코스 아님": `룸 예약인데 식사가 '해당 없음' 입니다`,
    "코스 미확정": `코스가 '확인 필요' 상태입니다`,
    "코스 인원 부족": `코스 인원이 성인 수보다 적습니다`
  };
  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });
  return out;
}"""
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_i ok")
