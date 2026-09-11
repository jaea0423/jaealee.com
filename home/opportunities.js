/* 한 날짜의 구조화된 자료를 읽고, 필터와 검색만 화면에서 처리합니다. */
(() => {
  const panel = document.getElementById('panel-opportunities');
  if (!panel) return;
  const list = document.getElementById('opp-list');
  const status = document.getElementById('opp-status');
  const retry = document.getElementById('opp-retry');
  const filters = document.getElementById('opp-filters');
  const search = document.getElementById('opp-search');
  let data, category = '전체', loading = false;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const link = value => { try { const url = new URL(value); return ['https:','http:'].includes(url.protocol) ? esc(url.href) : ''; } catch { return ''; } };
  function render() {
    const query = search.value.trim().toLocaleLowerCase('ko');
    const matches = data.items.filter(item => (category === '전체' || item.category === category) && [item.title,item.category,item.location.region,item.location.place,item.description].join(' ').toLocaleLowerCase('ko').includes(query));
    document.getElementById('opp-count').textContent = matches.length+'개';
    status.textContent = matches.length ? '' : '조건에 맞는 기회가 없습니다. 다른 분야나 검색어로 찾아보세요.';
    list.innerHTML = matches.map(item => `<article class="opp-entry"><div class="opp-main"><div class="opp-meta"><span>${esc(item.category)}</span><span class="opp-badge ${['확인 필요','사용자 제공','일부 확인'].includes(item.verification)?'opp-check':''}">${esc(item.verification)}</span></div><h4>${esc(item.title)}</h4><p class="opp-description">${esc(item.description)}</p><dl class="opp-facts"><div><dt>일정</dt><dd>${esc(item.event.label)}</dd></div><div><dt>장소</dt><dd>${esc(item.location.region)} · ${esc(item.location.place)}</dd></div><div><dt>가격</dt><dd>${esc(item.price.label)}</dd></div></dl></div><aside class="opp-action"><span class="opp-application">${esc(item.application.status)}</span>${item.application.deadline?`<strong class="opp-deadline">${esc(item.application.label)}</strong>`:''}<p>${esc(item.action)}</p><a href="${link(item.sources[0].url)}" target="_blank" rel="noopener noreferrer">${esc(item.sources[0].label)} <span aria-hidden="true">↗</span><span class="sr-only"> (새 탭)</span></a></aside><details class="opp-details"><summary>참여 조건·확인할 점·출처<span class="sr-only"> — ${esc(item.title)}</span></summary><div class="opp-detail-body"><div><h5>참여 조건</h5><p>${esc(item.eligibility)}</p></div><div><h5>확인할 점</h5><p>${esc(item.caveat)}</p></div><div class="opp-sources"><h5>출처</h5>${item.sources.map(source=>`<a href="${link(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.label)} ↗<span class="sr-only"> (새 탭)</span></a>`).join('')}<p>${esc(item.checkedOn)} 조사 기준</p></div></div></details></article>`).join('');
  }
  async function load() {
    if (loading || data) return;
    loading = true; retry.hidden = true; status.textContent = '기회를 불러오는 중입니다.';
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(),10000);
    try {
      const response = await fetch('/opportunities/2026-09-11.json',{signal:controller.signal,cache:'no-cache'});
      if (!response.ok) throw new Error('HTTP '+response.status);
      const result = await response.json();
      if (result.schemaVersion !== 1 || !Array.isArray(result.items)) throw new Error('Invalid data');
      data = result;
      filters.innerHTML = ['전체',...new Set(data.items.map(item=>item.category))].map(label=>`<button type="button" aria-pressed="${label===category}" data-opp-category="${esc(label)}">${esc(label)}</button>`).join('');
      document.getElementById('opp-note').textContent = data.researchNote;
      render();
    } catch { status.textContent = '자료를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.'; retry.hidden = false; }
    finally { clearTimeout(timer); loading = false; }
  }
  filters.addEventListener('click',event=>{
    const button = event.target.closest('[data-opp-category]'); if (!button) return;
    category = button.dataset.oppCategory;
    filters.querySelectorAll('button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
    render();
  });
  search.addEventListener('input',()=>{if(data)render();});
  retry.addEventListener('click',load);
  // 다른 탭을 읽는 동안에는 추가 요청을 만들지 않습니다.
  const route = () => { if(location.hash.split('/')[0]==='#opportunities') load(); };
  addEventListener('hashchange',route); route();
})();
