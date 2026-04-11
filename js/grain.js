function copyBibtex(btn) {
  var pre = btn.nextElementSibling;
  var text = pre.textContent;
  navigator.clipboard.writeText(text).then(function() {
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    setTimeout(function() {
      btn.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2000);
  });
}

(function() {
  var canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
  document.body.appendChild(canvas);

  var ctx = canvas.getContext('2d');
  var w, h;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  function draw() {
    var img = ctx.createImageData(w, h);
    var d = img.data;
    for (var i = 0; i < d.length; i += 4) {
      var r = Math.random();
      if (r > 0.93) {
        d[i] = d[i + 1] = d[i + 2] = 255;
        d[i + 3] = 20;
      } else if (r < 0.07) {
        d[i] = d[i + 1] = d[i + 2] = 0;
        d[i + 3] = 15;
      } else {
        d[i + 3] = 0;
      }
    }
    ctx.putImageData(img, 0, 0);
    requestAnimationFrame(draw);
  }
  draw();
})();