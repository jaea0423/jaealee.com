/* 기존 프로젝트 분류 동작을 독립 페이지에서 유지합니다. */
(() => {
  document.querySelectorAll('[data-project-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-project-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    const empty = button.dataset.projectFilter === 'design';
    document.getElementById('project-list').hidden = empty;
    document.getElementById('project-empty').hidden = !empty;
  }));
})();
