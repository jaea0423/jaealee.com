/* 발행일은 한국시간 07:00에 바뀝니다. 브라우저와 자동 발행 도구가 같은 계산을 씁니다. */
(() => {
  const date = (now = Date.now()) => new Date(Number(new Date(now)) + 2 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const preparationDate = (now = Date.now()) => date(Number(new Date(now)) + 3600000);
  const api = {date, preparationDate};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window === 'undefined') return;
  window.EditionDay = api;
  const refresh = () => {if (!document.hidden) window.dispatchEvent(new Event('editionrefresh'));};
  function boundary() {
    const next = Date.parse(date() + 'T07:00:00+09:00') + 86400000;
    setTimeout(() => {refresh(); boundary();}, Math.max(1, next - Date.now()));
  }
  boundary();
  // 6시에 생성한 자료의 배포가 늦어지면 배포가 끝날 때까지 미발행 화면만 주기적으로 갱신합니다.
  setInterval(refresh, 300000);
  window.addEventListener('focus', refresh);
  document.addEventListener('visibilitychange', refresh);
})();
