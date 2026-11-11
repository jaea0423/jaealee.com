/* DineONE 기업 홈페이지 시안 — 도입 신청서. 어디로도 보내지 않고 화면에서만 접수 처리(더미 접수번호). */
(function () {
  var yr = document.getElementById("yr");
  if (yr) yr.textContent = new Date().getFullYear();

  var form = document.getElementById("applyForm");
  if (!form) return;
  var box = document.getElementById("applyBox");

  // 전화번호: 숫자만 받아 010-0000-0000 모양으로
  var tel = form.elements.tel;
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
  ["store", "kind", "name", "tel"].forEach(function (n) {
    var el = form.elements[n];
    el.addEventListener("blur", function () { if (el.value) check(el); });
    el.addEventListener("input", function () { if (el.closest(".field").classList.contains("bad")) check(el); });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = null;
    ["store", "kind", "name", "tel"].forEach(function (n) {
      var el = form.elements[n];
      if (!check(el) && !bad) bad = el;
    });
    var agree = form.elements.agree;
    if (!bad && !agree.checked) {
      agree.closest(".agree").style.color = "#C0392B";
      agree.focus();
      return;
    }
    if (bad) { bad.focus(); return; }

    var needs = [].slice.call(form.querySelectorAll('input[name="need"]:checked')).map(function (i) { return i.value; });
    var now = new Date();
    var no = "DO-" + now.getFullYear() + String(now.getMonth() + 1).padStart(2, "0") + String(now.getDate()).padStart(2, "0") +
             "-" + String(Math.floor(Math.random() * 90) + 10);
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

    box.innerHTML =
      '<div class="done" role="status">' +
        '<span class="ok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></span>' +
        '<h3>신청이 접수됐습니다</h3>' +
        '<p>' + esc(form.elements.name.value.trim()) + ' 님, 영업일 하루 안에 연락드리겠습니다.</p>' +
        '<dl>' +
          '<dt>접수번호</dt><dd>' + no + '</dd>' +
          '<dt>가게</dt><dd>' + esc(form.elements.store.value.trim()) + ' · ' + esc(form.elements.kind.value) + '</dd>' +
          '<dt>연락처</dt><dd>' + esc(tel.value) + '</dd>' +
          '<dt>필요한 기능</dt><dd>' + (needs.length ? esc(needs.join(", ")) : "상담 때 정하기") + '</dd>' +
        '</dl>' +
        '<button class="btn line" type="button" id="again">다시 작성하기</button>' +
      '</div>';
    box.querySelector("#again").addEventListener("click", function () { location.reload(); });
    box.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  form.elements.agree.addEventListener("change", function () { this.closest(".agree").style.color = ""; });
})();
