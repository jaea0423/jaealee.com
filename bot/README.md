# RED — Routine Every Day

하루 기록 텔레그램 봇. 맥에서 24시간 켜두고 쓴다.

| 언제 | 무엇 |
|---|---|
| 매일 밤 23:00 | 내일 날짜가 채워진 입력 틀을 보낸다 |
| 매일 아침 07:00 | 오늘 시간표 링크를 보낸다 |
| 매일 아침 07:30 | 오늘 뉴스 링크를 보낸다 |
| 아무 때나 | `/help` 등 명령어에 답한다 |

시각은 `config.env` 에서 바꿀 수 있다.

> 뉴스는 아직 발행 전이어도 링크를 그대로 보낸다.
> 확인해보니 뉴스 JSON은 오후에 올라오는 날이 많아서,
> 07:30 메시지에 "아직 발행 전일 수 있습니다"가 붙는 경우가 잦다.
> 링크는 계속 유효하니 나중에 다시 눌러보면 된다.

---

## 명령어

| 명령어 | 하는 일 |
|---|---|
| `/help` | 도움말 + 입력 규칙 전문 |
| `/template` | 전체 칸 틀 (기본은 내일 날짜) |
| `/simple` | 간단 틀 |
| `/today` | 오늘 시간표 링크 |
| `/news` | 오늘 뉴스 링크 |
| `/date 2026-08-19` | 그날 시간표 링크 |
| `/status` | 봇이 살아있는지, 마지막 발송이 언제였는지 |

`/template 2026-08-25` 처럼 날짜를 붙이면 그 날짜로 채워진다.

---

## 1. 봇 만들기

텔레그램에서 **@BotFather** 를 찾아 대화를 연다.

```
/newbot
→ 봇 이름 입력      (예: RED)
→ 사용자명 입력     (반드시 bot으로 끝나야 함, 예: jaea_red_bot)
```

그러면 **토큰**을 준다. `1234567890:AAF...` 형태다.

> ⚠️ 이 토큰은 비밀번호와 같다. 아무에게도 보여주지 말고,
> git에 올리지 말고, 채팅에 붙여넣지 마라.
> 실수로 노출되면 BotFather에서 `/revoke` 로 즉시 폐기하고 새로 받는다.

---

## 2. 내 대화방 번호(chat_id) 알아내기

1. 방금 만든 봇을 검색해서 대화를 열고 **아무 말이나 한 번 보낸다** (예: `안녕`)
2. 브라우저 주소창에 아래를 친다. `<토큰>` 자리에 1단계 토큰을 넣는다.

```
https://api.telegram.org/bot<토큰>/getUpdates
```

3. 나오는 글에서 `"chat":{"id":123456789` 부분의 **숫자**가 chat_id다.

봇이 먼저 말을 걸 수는 없기 때문에 내가 먼저 보내는 1번 과정이 꼭 필요하다.

---

## 3. 파일 두고 설정하기

```bash
# 봇 파일을 홈에 둔다
mkdir -p ~/red
curl -o ~/red/red.py https://jaealee.com/bot/red.py

# 설정 파일을 만든다 (저장소 밖이다. 일부러 그렇게 한 것)
mkdir -p ~/.config/red
curl -o ~/.config/red/config.env https://jaealee.com/bot/config.example.env

# 편집기로 열어서 토큰과 chat_id를 채운다
open -e ~/.config/red/config.env

# 남이 못 읽게 권한을 좁힌다
chmod 600 ~/.config/red/config.env
```

**먼저 손으로 돌려서 확인한다.**

```bash
python3 ~/red/red.py
```

`RED 시작` 이 뜨면 성공이다. 텔레그램에서 `/status` 를 보내 답이 오는지 본다.
확인했으면 `Ctrl + C` 로 끈다.

---

## 4. 자동 실행 등록 (launchd)

맥을 껐다 켜도 알아서 돌게 만든다.

```bash
curl -o /tmp/red.plist https://jaealee.com/bot/com.jaealee.red.plist

# 파일 안의 __USERNAME__ 을 내 사용자 이름으로 바꾼다
sed "s/__USERNAME__/$(whoami)/g" /tmp/red.plist \
  > ~/Library/LaunchAgents/com.jaealee.red.plist

# 등록
launchctl load ~/Library/LaunchAgents/com.jaealee.red.plist
```

확인·중지·재시작은 이렇게 한다.

```bash
launchctl list | grep red             # 돌고 있나
tail -f ~/Library/Logs/red.log        # 로그 실시간 보기

launchctl unload ~/Library/LaunchAgents/com.jaealee.red.plist   # 중지
launchctl load   ~/Library/LaunchAgents/com.jaealee.red.plist   # 시작
```

---

## 알아둘 것

**틀을 고치면 봇도 같이 바뀐다.**
봇은 틀 문구를 자기 안에 갖고 있지 않고, 매번
`https://jaealee.com/schedule/template.txt` 를 받아온다.
저장소의 `template.txt` 만 고쳐서 푸시하면 끝이다. 봇을 다시 켤 필요 없다.

**맥이 잠들면 그 시각엔 못 보낸다.**
대신 깨어난 뒤 6시간 안이면 그날치를 한 번 보낸다.
6시간이 넘었으면 이미 늦었다고 보고 건너뛴다.

**내 대화방에서 온 메시지만 처리한다.**
누가 봇 주소를 알아내 말을 걸어도 무시된다.
`config.env` 의 `TELEGRAM_CHAT_ID` 로 걸러진다.

**Cowork의 23:00 점검 작업과 역할이 겹친다.**
지금은 둘 다 밤 11시에 내일 시간표를 챙기라고 알리는 셈이다.
RED가 자리를 잡으면 Cowork 예약 작업은 꺼도 된다.

---

## 파일

| 파일 | 설치 위치 |
|---|---|
| `red.py` | `~/red/red.py` |
| `config.example.env` | `~/.config/red/config.env` (복사 후 값 채움) |
| `com.jaealee.red.plist` | `~/Library/LaunchAgents/` |

상태 기록은 `~/.local/state/red/state.json` 에 쌓인다.
"오늘 이미 보냈는지"만 들어 있어서 지워도 문제없다.

---

## 잘 안 될 때

| 증상 | 볼 곳 |
|---|---|
| 아무 반응이 없다 | `tail ~/Library/Logs/red.error.log` |
| `RED 설정 오류` 로 바로 종료 | `config.env` 경로와 토큰·chat_id 확인 |
| `HTTP 401` | 토큰이 틀렸다. BotFather에서 다시 확인 |
| `HTTP 400 chat not found` | chat_id가 틀렸다. 2단계를 다시 |
| `ZoneInfoNotFoundError` | `pip3 install tzdata` |
| 틀이 안 오고 경고만 온다 | `template.txt` 가 아직 푸시되지 않았다 |
