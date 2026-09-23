# GPT(Codex)에게 넘길 때 쓰는 프롬프트

재아가 세세한 수정을 GPT 쪽에서 몰아서 할 때 복사해 쓰는 글입니다.
규칙 자체는 각 폴더 `AGENTS.md`(= `CLAUDE.md` 요약)에 있으니 여기서 되풀이하지 않습니다. 이 글은 **일 시키는 말투**만 담습니다.

---

## 붙여 넣을 프롬프트

```
저장소 jaealee.com 에서 한옥반점 일을 이어서 합니다.

먼저 이 순서로 읽고 시작하세요. 읽기 전에는 파일을 고치지 마세요.
1) 고칠 폴더의 AGENTS.md  (hanok/AGENTS.md · hanok/system/AGENTS.md · anjip/AGENTS.md)
2) 같은 폴더의 CLAUDE.md  (규칙 전문 — AGENTS.md 는 요약입니다)
3) hanok/system/work/PROGRESS.md 의 마지막 20줄  (최근에 무엇을 왜 바꿨는지)

쓰는 사람은 분당 중식당 한옥반점의 사장님과 홀 직원입니다. 개발자가 아닙니다.
화면은 카운터 태블릿이 주력이고, 손님용 TV 는 2018~2020년 크롬이라 최신 문법이 죽습니다.
그래서 AGENTS.md 의 '구형 TV 금지 문법' 과 '경고는 막지 않고 알리기만' 은 취향이 아니라 제약입니다.

이번에 할 일:
- (여기에 고칠 것을 하나씩 적기)
- 
- 

지키는 방식:
- 시스템(hanok/system/)은 src/ 조각만 고치고, 끝나면 `python build.py` 와 `python build.py dev` 를
  돌려 '구형 브라우저 문법 검사 통과' 를 확인합니다. dist/·index.html·dev/·screen/ 은 직접 고치지 않습니다.
- 고친 화면은 직접 띄워 보고 확인합니다. 추측으로 "됐을 겁니다" 하지 않습니다.
  폭 430 / 820 / 1280 / 1920 중 그 변경에 해당하는 것을 봅니다.
- 주석은 한국어로 '왜' 를 씁니다.
- 시킨 것만 합니다. 지나가다 눈에 거슬린 것은 고치지 말고 끝에 목록으로 알려 주세요.
- PIN·API 키·supabase.*.json 은 건드리지도, 새로 적지도 않습니다.
- 한 묶음이 끝나면 hanok/system/work/PROGRESS.md 에 한 줄(날짜 · 무엇을 · 왜) 남기고,
  그 묶음에 해당하는 파일만 골라 커밋합니다. 커밋 메시지는 한국어로 '무엇을 왜'.

끝나면 이렇게 알려 주세요:
- 고친 것 목록(파일 : 무엇을 : 왜)
- 화면으로 확인한 것과 확인 못 한 것
- 손대지 않고 남겨 둔 것 / 건드리면 위험해 보였던 것
```

---

## 넘기기 전에 (재아)

```bash
cd /c/GitHub/jaealee.com && git add -A && git commit -m "GPT 로 넘기기 전 정리" && git tag -f gpt-before && git push
```

`gpt-before` 는 **돌아왔을 때 무엇이 바뀌었는지 볼 표시**입니다(로컬 태그, 올라가지 않습니다).

## 돌아왔을 때

클로드에게 **"GPT 작업 끝, 확인해줘"** 한마디면 됩니다. 클로드가 하는 일:

```bash
cd /c/GitHub/jaealee.com && git fetch && git log --oneline gpt-before..HEAD && git diff --stat gpt-before..HEAD
```

1. `gpt-before` 이후 커밋·변경 파일 훑기
2. 금지 문법·조각 순서·예약 객체 모양이 지켜졌는지 확인
3. `python build.py` · `build.py dev` 다시 돌리기
4. 바뀐 화면을 직접 띄워 확인
5. PROGRESS.md 가 비어 있으면 대신 채워 넣기
