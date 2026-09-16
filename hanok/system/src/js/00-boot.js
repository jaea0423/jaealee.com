/* 오래된 브라우저에서 스크립트가 멈추면 흰 화면 대신 안내를 띄웁니다 */
window.onerror = function(msg){
  var app = document.getElementById("app");
  if(app && !app.getAttribute("data-ok")){
    app.innerHTML = '<div style="max-width:420px;margin:14vh auto;padding:28px;text-align:center;'+
      'font-family:sans-serif;color:#333;border:1px solid #ddd;border-radius:4px">'+
      '<div style="font-size:17px;font-weight:700;margin-bottom:10px">화면을 열 수 없습니다</div>'+
      '<div style="font-size:13.5px;line-height:1.7;color:#666">브라우저가 오래되어 이 화면을 표시할 수 없습니다.<br>'+
      'TV 브라우저를 최신으로 업데이트하거나,<br>크롬캐스트·미니PC·스틱PC를 연결해 사용해 주세요.</div>'+
      '<div style="font-size:11px;color:#aaa;margin-top:16px;word-break:break-all">'+String(msg)+'</div></div>';
  }
  return false;
};
