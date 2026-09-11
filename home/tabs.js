/* 같은 문서에서 탭을 전환하고 주소 해시로 뒤로 가기와 공유를 지원합니다. */
(() => {
  const buttons = [...document.querySelectorAll('[data-home-tab]')];
  const allowed = buttons.map(button => button.dataset.homeTab);
  const dateInput = document.getElementById('news-date');
  let lastNewsDate = '', requestId = 0;
  const seoul = new Date(new Date().toLocaleString('en-US', {timeZone:'Asia/Seoul'}));
  const format = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  dateInput.value = format(seoul);
  function activate(key) {
    if (!allowed.includes(key)) key = 'start';
    buttons.forEach(button => {
      const active = button.dataset.homeTab === key;
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
      document.getElementById(button.getAttribute('aria-controls')).hidden = !active;
    });
    document.title = `${buttons.find(button => button.dataset.homeTab === key).textContent} · Jaea Lee`;
    if (key === 'news') loadArchive();
    if (key === 'news' && lastNewsDate !== dateInput.value) loadNews();
  }
  function readRoute() {
    const [key, date] = location.hash.slice(1).split('/');
    if (key === 'news' && /^\d{4}-\d{2}-\d{2}$/.test(date || '')) dateInput.value = date;
    activate(key);
  }
  buttons.forEach((button,index) => {
    button.addEventListener('click', () => {
      const key = button.dataset.homeTab;
      if (location.hash === '#'+key) activate(key); else location.hash = key;
    });
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length-1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
      buttons[next].focus(); buttons[next].click();
    });
  });
  addEventListener('hashchange', readRoute);
  document.querySelectorAll('[data-project-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-project-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    const empty = button.dataset.projectFilter === 'design';
    document.getElementById('project-list').hidden = empty;
    document.getElementById('project-empty').hidden = !empty;
  }));
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeURL = value => { try { const url = new URL(value); return ['http:','https:'].includes(url.protocol) ? url.href : ''; } catch { return ''; } };
  // 타임아웃은 본문을 읽을 때까지 적용하고, 이전 날짜 요청은 화면을 덮어쓰지 못하게 합니다.
  async function get(url, head = false) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch(url, {method:head ? 'HEAD':'GET',signal:controller.signal,cache:'no-store'});
      if (response.status === 404) return null;
      if (!response.ok) throw new Error('HTTP '+response.status);
      return head ? true : await response.json();
    } finally { clearTimeout(timer); }
  }
  async function loadNews() {
    const date = dateInput.value;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return;
    const current = ++requestId;
    const status = document.getElementById('news-status');
    const content = document.getElementById('news-content');
    status.textContent = '브리핑을 불러오는 중…'; content.replaceChildren();
    lastNewsDate = date;
    try {
      const data = await get(`/news/data/${date}.json`);
      if (current !== requestId) return;
      if (!data) {
        const legacy = `/news/News%20Source/DailyNews_${date.replaceAll('-','')}.html`;
        const exists = await get(legacy, true);
        if (current !== requestId) return;
        if (exists) {
          status.textContent = '이 날짜는 이전 형식의 보관본입니다.';
          const frame = document.createElement('iframe');
          frame.className = 'legacy-news'; frame.title = `${date} 뉴스 보관본`;
          frame.setAttribute('sandbox','allow-popups allow-popups-to-escape-sandbox');
          frame.src = legacy; content.append(frame);
        } else status.textContent = `${date}에 등록된 뉴스가 없습니다. 다른 날짜를 선택해주세요.`;
        return;
      }
      status.textContent = `${date} 브리핑`;
      renderNews(data, content);
    } catch {
      if (current !== requestId) return;
      lastNewsDate = '';
      status.textContent = '뉴스를 불러오지 못했습니다. 연결을 확인한 뒤 뉴스 보기를 다시 눌러주세요.';
    }
  }
  let archiveLoaded = false;
  function displayArchive(dates) {
    const valid = [...new Set(dates.filter(date => /^\d{4}-\d{2}-\d{2}$/.test(date)))].sort().reverse();
    const list = document.getElementById('archive-list');
    list.replaceChildren();
    document.getElementById('archive-count').textContent = `· ${valid.length}일`;
    valid.forEach(date => {
      const button = document.createElement('button');
      button.type = 'button'; button.textContent = date;
      button.addEventListener('click', () => { dateInput.value = date; if (location.hash === '#news/'+date) loadNews(); else location.hash = 'news/'+date; });
      list.append(button);
    });
  }
  async function loadArchive() {
    if (archiveLoaded) return;
    archiveLoaded = true;
    const status = document.getElementById('archive-status');
    // 배포된 목록을 먼저 표시하고 공개 저장소의 등록 파일로 갱신합니다.
    let hasSnapshot = false;
    try {
      const snapshot = await get('/news/archive.json');
      if (Array.isArray(snapshot?.dates)) {
        displayArchive(snapshot.dates); hasSnapshot = true;
        status.textContent = '최신순으로 표시합니다.';
      }
    } catch {}
    try {
      const base = 'https://api.github.com/repos/jaea0423/jaealee.com/contents/news/';
      const results = await Promise.all([get(base+'data?ref=main'),get(base+'News%20Source?ref=main')]);
      if (!results.every(Array.isArray)) throw new Error('Invalid listing');
      const dates = results.flat().filter(file => file.type === 'file').map(file => {
        const modern = /^(\d{4}-\d{2}-\d{2})\.json$/.exec(file.name);
        const legacy = /^DailyNews_(\d{4})(\d{2})(\d{2})\.html$/.exec(file.name);
        return modern ? modern[1] : legacy ? `${legacy[1]}-${legacy[2]}-${legacy[3]}` : '';
      }).filter(Boolean);
      displayArchive(dates);
      status.textContent = '최신순으로 표시합니다. 날짜를 누르면 아래에서 읽을 수 있습니다.';
    } catch {
      status.textContent = hasSnapshot ? '최근 갱신은 확인하지 못했습니다. 저장된 목록을 표시합니다.' : '목록을 불러오지 못했습니다. 아래에서 날짜를 직접 선택할 수 있습니다.';
    }
  }
  function renderNews(data, content) {
    const tiles = (data.market?.tiles || []).map(tile => `<div class="news-tile"><span>${esc(tile.name)}</span><strong>${esc(tile.value)}</strong><span>${esc(tile.change)}</span><small>${esc(tile.fx)}</small><small>${esc(tile.asof)}</small></div>`).join('');
    content.innerHTML = `<div class="news-summary"><h3>${esc(data.title || '뉴스 브리핑')}</h3><p>${esc(data.tagline)}</p><p>${esc(data.market?.oneliner)}</p><div class="news-market">${tiles}</div><p class="news-meta">${esc(data.market?.note)}</p></div>` + (data.sections || []).map(section => `<section class="news-section"><h3>${esc(section.labelKr || section.label)}</h3><p>${esc(section.desc)}</p><div class="news-cards">${(section.cards || []).map(card => {
      const url = safeURL(card.url);
      return `<article class="news-article"><div class="news-meta">${esc(card.tag)} · ${esc(card.date)} · ${esc(card.source)}</div><h4>${url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(card.title)}</a>` : esc(card.title)}</h4><p>${esc(card.summary)}</p></article>`;
    }).join('')}</div><div class="news-keywords">${(section.keywords || []).map(keyword => `<details><summary>${esc(keyword.word)}</summary><p>${esc(keyword.desc)}</p></details>`).join('')}</div>${section.forYou ? `<aside class="news-extra"><strong>${esc(section.forYou.sub)}</strong><p>${esc(section.forYou.body)}</p></aside>` : ''}</section>`).join('');
  }
  document.getElementById('news-form').addEventListener('submit', event => {
    event.preventDefault();
    history.replaceState(null, '', '#news/'+dateInput.value); loadNews();
  });
  function shiftDate(delta) {
    if (!dateInput.value) return;
    const date = new Date(dateInput.value+'T12:00:00');
    date.setDate(date.getDate()+delta); dateInput.value = format(date);
    history.replaceState(null, '', '#news/'+dateInput.value); loadNews();
  }
  document.getElementById('news-prev').addEventListener('click', () => shiftDate(-1));
  document.getElementById('news-next').addEventListener('click', () => shiftDate(1));
  readRoute();
})();
