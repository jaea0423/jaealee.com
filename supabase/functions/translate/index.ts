// =====================================================================
// Supabase Edge Function: translate
// 상하이 가족여행 페이지(jaealee.com/family/trip/2027/shanghai/)의 번역 탭 전용
//
// 하는 일: 한국어 문장을 받아 Gemini로 간체 중국어 + 병음을 만들어 돌려줌
//   요청  POST { "text": "이 근처에 약국 있나요?" }
//   응답  200  { "zh": "这附近有药店吗？", "pinyin": "zhè fùjìn yǒu yàodiàn ma?" }
//
// 왜 서버를 거치나: Gemini 키를 웹페이지에 넣으면 누구나 소스 보기로 복사할 수 있음.
//                  키는 Supabase 비밀값(secret)에만 두고, 페이지는 이 함수만 부름.
//
// 필요한 비밀값 (supabase secrets set 이름=값)
//   GEMINI_API_KEY  (필수) 이 페이지 전용으로 새로 만든 Gemini 키 → 다른 곳과 사용량이 섞이지 않음
//   FAMILY_CODE     (권장) 가족 암호. 설정하면 암호를 아는 사람만 번역 가능 (남이 함수를 마구 호출하는 것 방지)
//   GEMINI_MODEL    (선택) 기본값 gemini-3.5-flash-lite
//
// 배포 순서 (저장소 폴더에서, Supabase CLI 로그인 후)
//   1) supabase secrets set GEMINI_API_KEY=새키 FAMILY_CODE=가족암호 --project-ref 프로젝트ID
//   2) supabase functions deploy translate --project-ref 프로젝트ID
//   3) 페이지 index.html의 TRANSLATE.url / TRANSLATE.anonKey 채우기
// =====================================================================

// 브라우저에서 호출을 허용할 주소. 다른 사이트의 페이지가 이 함수를 쓰지 못하게 제한
// (단, 브라우저 밖 도구는 Origin을 속일 수 있으므로 진짜 보호는 FAMILY_CODE가 담당)
const ALLOWED_ORIGINS = ["https://jaealee.com", "https://www.jaealee.com"];
const MAX_LEN = 300; // 한 번에 번역할 최대 글자 수 → 긴 글로 사용량을 많이 쓰는 것 방지

function cors(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-family-code",
    "Vary": "Origin",
  };
}

function json(body: unknown, status: number, origin: string | null) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(origin), "Content-Type": "application/json; charset=utf-8" },
  });
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");

  // 브라우저가 본 요청 전에 보내는 사전 확인(preflight) 요청
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "POST만 가능" }, 405, origin);

  // 가족 암호 확인 (FAMILY_CODE를 설정한 경우에만)
  const familyCode = Deno.env.get("FAMILY_CODE");
  if (familyCode && req.headers.get("x-family-code") !== familyCode) {
    return json({ error: "가족 암호가 맞지 않습니다" }, 403, origin);
  }

  // 입력 검사
  let text = "";
  try {
    text = String((await req.json()).text ?? "").trim();
  } catch {
    return json({ error: "잘못된 요청 형식" }, 400, origin);
  }
  if (!text) return json({ error: "번역할 문장이 없습니다" }, 400, origin);
  if (text.length > MAX_LEN) return json({ error: `${MAX_LEN}자 이하로 입력해 주세요` }, 400, origin);

  const key = Deno.env.get("GEMINI_API_KEY");
  if (!key) return json({ error: "서버에 GEMINI_API_KEY가 설정되지 않았습니다" }, 500, origin);
  const model = Deno.env.get("GEMINI_MODEL") ?? "gemini-3.5-flash-lite";

  // 결과를 JSON 형식으로 강제(responseSchema) → 중국어와 병음을 따로 받기 쉬움
  const body = {
    contents: [{
      parts: [{
        text:
          "다음 한국어를 중국 본토(상하이)에서 자연스럽게 쓰는 간체 중국어로 번역해. " +
          "여행 중 현지인에게 말하거나 화면으로 보여주는 상황이니 짧고 공손하게. " +
          "pinyin은 성조 부호를 붙이고 단어 단위로 띄어 써.\n\n한국어: " + text,
      }],
    }],
    generationConfig: {
      temperature: 0.2,
      responseMimeType: "application/json",
      responseSchema: {
        type: "OBJECT",
        properties: { zh: { type: "STRING" }, pinyin: { type: "STRING" } },
        required: ["zh", "pinyin"],
      },
    },
  };

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-goog-api-key": key },
        body: JSON.stringify(body),
      },
    );
    const data = await res.json();
    if (!res.ok) {
      // Gemini 쪽 오류 내용은 서버 로그에만 남기고, 페이지에는 간단히 전달 (키 관련 정보 노출 방지)
      console.error("Gemini error", res.status, JSON.stringify(data));
      return json({ error: res.status === 429 ? "사용량 한도 초과, 잠시 후 다시" : "번역 서버 오류" }, 502, origin);
    }
    const out = JSON.parse(data.candidates[0].content.parts[0].text);
    return json({ zh: out.zh, pinyin: out.pinyin }, 200, origin);
  } catch (e) {
    console.error("translate failed", e);
    return json({ error: "번역 실패" }, 500, origin);
  }
});
