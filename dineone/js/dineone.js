/* DineONE 기업 홈페이지 시안
   - 위 막대: 내리면 검정 유리로
   - 첫 화면 제품 화면: 실제 시안을 iframe 으로 넣고 상자 폭에 맞춰 줄임
   - 도입 문의: 어디로도 보내지 않고 화면에서만 접수 처리(더미 접수번호) */
(function () {
  var yr = document.getElementById("yr");
  if (yr) yr.textContent = new Date().getFullYear();

  // 위 막대
  var nav = document.getElementById("nav");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("solid", window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // 제품 화면 크기 맞추기
  var frames = [].slice.call(document.querySelectorAll(".device iframe"));
  function fit() {
    frames.forEach(function (f) {
      var w = +f.dataset.w, h = +f.dataset.h, box = f.parentNode;
      var s = box.clientWidth / w;
      f.style.width = w + "px";
      f.style.height = h + "px";
      f.style.transform = "scale(" + s + ")";
    });
  }
  if (frames.length) {
    fit();
    window.addEventListener("resize", fit);
    if (window.ResizeObserver) frames.forEach(function (f) { new ResizeObserver(fit).observe(f.parentNode); });
  }

  // 도입 문의
  var form = document.getElementById("applyForm");
  if (!form) return;
  var box = document.getElementById("applyBox");
  var tel = form.elements.tel;
  var agreeLabel = form.elements.agree.closest(".agree");

  function fmtTel(v) {
    var d = v.replace(/\D/g, "").slice(0, 11);
    if (d.indexOf("02") === 0) {
      if (d.length > 9) return d.slice(0, 2) + "-" + d.slice(2, 6) + "-" + d.slice(6, 10);
      if (d.length > 5) return d.slice(0, 2) + "-" + d.slice(2, 5) + "-" + d.slice(5);
      if (d.length > 2) return d.slice(0, 2) + "-" + d.slice(2);
      return d;
    }
    if (d.length > 10) return d.slice(0, 3) + "-" + d.slice(3, 7) + "-" + d.slice(7);
    if (d.length > 6) return d.slice(0, 3) + "-" + d.slice(3, 6) + "-" + d.slice(6);
    if (d.length > 3) return d.slice(0, 3) + "-" + d.slice(3);
    return d;
  }
  tel.addEventListener("input", function () { tel.value = fmtTel(tel.value); });

  function check(el) {
    var f = el.closest(".field");
    var ok = el.value.trim() !== "";
    if (el === tel) ok = tel.value.replace(/\D/g, "").length >= 9;
    if (f) f.classList.toggle("bad", !ok);
    return ok;
  }
  var REQ = ["store", "kind", "name", "tel"];
  REQ.forEach(function (n) {
    var el = form.elements[n];
    el.addEventListener("blur", function () { if (el.value) check(el); });
    el.addEventListener("input", function () { if (el.closest(".field").classList.contains("bad")) check(el); });
    el.addEventListener("change", function () { if (el.closest(".field").classList.contains("bad")) check(el); });
  });
  form.elements.agree.addEventListener("change", function () { agreeLabel.classList.remove("bad"); });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = null;
    REQ.forEach(function (n) { var el = form.elements[n]; if (!check(el) && !bad) bad = el; });
    if (bad) { bad.focus(); return; }
    if (!form.elements.agree.checked) { agreeLabel.classList.add("bad"); form.elements.agree.focus(); return; }

    var needs = [].slice.call(form.querySelectorAll('input[name="need"]:checked')).map(function (i) { return i.value; });
    var now = new Date();
    var no = "DO-" + now.getFullYear() + String(now.getMonth() + 1).padStart(2, "0") + String(now.getDate()).padStart(2, "0") +
             "-" + String(Math.floor(Math.random() * 90) + 10);

    box.innerHTML =
      '<div class="done" role="status">' +
        '<span class="ok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></span>' +
        '<h3>문의가 접수됐습니다</h3>' +
        '<p>' + esc(form.elements.name.value.trim()) + ' 님, 영업일 하루 안에 연락드리겠습니다.</p>' +
        '<dl>' +
          '<dt>접수번호</dt><dd>' + no + '</dd>' +
          '<dt>가게</dt><dd>' + esc(form.elements.store.value.trim()) + ' · ' + esc(form.elements.kind.value) + '</dd>' +
          '<dt>연락처</dt><dd>' + esc(tel.value) + '</dd>' +
          '<dt>관심 기능</dt><dd>' + (needs.length ? esc(needs.join(", ")) : "상담 때 정하기") + '</dd>' +
        '</dl>' +
        '<button class="btn line" type="button" id="again">새로 작성하기</button>' +
      '</div>';
    box.querySelector("#again").addEventListener("click", function () { location.reload(); });
    box.scrollIntoView({ behavior: "smooth", block: "center" });
  });
})();
