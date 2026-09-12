/* 기존 상대경로를 유지하고, 새 자료가 올라오면 목록 수정 없이 연결을 활성화합니다. */
(() => {
 const resources = [...document.querySelectorAll('[data-resource]')];
 resources.forEach(link => link.addEventListener('click', event => {
  if(link.getAttribute('aria-disabled') === 'true') event.preventDefault();
 }));
 async function check(link) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 6000);
  try {
   const response = await fetch(link.href, {method:'HEAD', cache:'no-store', signal:controller.signal});
   // 통신 오류는 미등록으로 단정하지 않고 기존 표시와 링크를 보존합니다.
   if(!response.ok && response.status !== 404) return;
   const available = response.ok;
   link.classList.toggle('is-unavailable', !available);
   if(available) link.removeAttribute('aria-disabled'); else link.setAttribute('aria-disabled','true');
   link.querySelector('.resource-status').textContent = available ? (link.getAttribute('href').endsWith('/') ? '열기' : '자료 보기') : '준비 중';
  } catch {} finally { clearTimeout(timer); }
 }
 // 작은 병렬 수로 서버에 한꺼번에 요청하지 않습니다.
 let next = 0;
 async function worker() {while(next < resources.length) await check(resources[next++]);}
 for(let i=0;i<Math.min(4,resources.length);i++) worker();
})();
