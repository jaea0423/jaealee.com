/* 화면과 주소를 그대로 보존한 채 검정 화면만 잠시 띄웁니다. */
(() => {
  const button = document.getElementById('blackout-button');
  const screen = document.getElementById('blackout-screen');
  const workspace = document.querySelector('.workspace');
  let active = false, clicks = 0, ownedFullscreen = false;
  let previousFocus, previousOverflow, previousInert;
  function close() {
    if (!active) return;
    active = false;
    screen.hidden = true;
    workspace.inert = previousInert;
    document.body.style.overflow = previousOverflow;
    const restoreFocus = () => { if (!active) previousFocus?.focus({preventScroll:true}); };
    if (document.fullscreenElement === screen) document.exitFullscreen().catch(() => {}).then(restoreFocus);
    else restoreFocus();
    ownedFullscreen = false;
  }
  button.addEventListener('click', () => {
    if (active) return;
    active = true; clicks = 0;
    previousFocus = document.activeElement;
    previousOverflow = document.body.style.overflow;
    previousInert = workspace.inert;
    workspace.inert = true;
    document.body.style.overflow = 'hidden';
    screen.hidden = false;
    screen.focus({preventScroll:true});
    // 전체화면이 허용되지 않아도 브라우저 페이지는 검정으로 유지합니다.
    if (!document.fullscreenElement && screen.requestFullscreen) {
      screen.requestFullscreen({navigationUI:'hide'}).then(() => {
        if (!active && document.fullscreenElement === screen) document.exitFullscreen().catch(() => {});
      }).catch(() => {});
    }
  });
  // 빠른 더블클릭뿐 아니라 떨어진 위치에서 천천히 두 번 눌러도 돌아갑니다.
  screen.addEventListener('click', () => { if (active && ++clicks >= 2) close(); });
  screen.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); close(); }
  });
  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement === screen) ownedFullscreen = true;
    else if (ownedFullscreen) close();
  });
})();
