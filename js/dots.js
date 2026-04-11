(function () {
  var hero = document.querySelector('.hero');
  if (!hero) return;

  var canvas = document.createElement('canvas');
  canvas.style.position = 'absolute';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.pointerEvents = 'none';
  canvas.style.zIndex = '0';
  hero.style.position = 'relative';
  hero.insertBefore(canvas, hero.firstChild);

  var ctx = canvas.getContext('2d');
  var prevMX = -1000;
  var prevMY = -1000;
  var mouseVX = 0;
  var mouseVY = 0;
  var mouseX = -1000;
  var mouseY = -1000;
  var mouseActive = false;
  var dots = [];
  var spacing = 24;
  var baseRadius = 1.2;
  var influenceRadius = 140;
  var momentumTransfer = 0.04;
  var friction = 0.82;
  var returnForce = 0.04;
  var radiusReturn = 0.025;

  var color = { r: 68, g: 68, b: 68 };

  function resize() {
    var rect = hero.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    var cols = Math.ceil(canvas.width / spacing) + 1;
    var rows = Math.ceil(canvas.height / spacing) + 1;

    dots = [];
    for (var row = 0; row < rows; row++) {
      for (var col = 0; col < cols; col++) {
        var bx = col * spacing;
        var by = row * spacing;
        dots.push({ ox: bx, oy: by, x: bx, y: by, vx: 0, vy: 0, r: baseRadius });
      }
    }
  }

  hero.addEventListener('mousemove', function (e) {
    var rect = hero.getBoundingClientRect();
    var nx = e.clientX - rect.left;
    var ny = e.clientY - rect.top;
    if (prevMX > -900) {
      mouseVX = nx - prevMX;
      mouseVY = ny - prevMY;
    }
    prevMX = nx;
    prevMY = ny;
    mouseX = nx;
    mouseY = ny;
    mouseActive = true;
  });

  hero.addEventListener('mouseleave', function () {
    mouseX = -1000;
    mouseY = -1000;
    mouseVX = 0;
    mouseVY = 0;
    mouseActive = false;
  });

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var speed = Math.sqrt(mouseVX * mouseVX + mouseVY * mouseVY);
    var cx = canvas.width / 2;
    var cy = canvas.height / 2;

    for (var i = 0; i < dots.length; i++) {
      var d = dots[i];
      var dx = d.ox - mouseX;
      var dy = d.oy - mouseY;
      var dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < influenceRadius && mouseActive && speed > 0.5) {
        var force = 1 - dist / influenceRadius;
        var impulse = force * momentumTransfer;
        d.vx += mouseVX * impulse;
        d.vy += mouseVY * impulse;
      }

      d.vx += (d.ox - d.x) * returnForce;
      d.vy += (d.oy - d.y) * returnForce;
      d.vx *= friction;
      d.vy *= friction;
      d.x += d.vx;
      d.y += d.vy;

      var displace = Math.sqrt((d.x - d.ox) * (d.x - d.ox) + (d.y - d.oy) * (d.y - d.oy));
      var targetR = baseRadius + Math.min(displace * 0.03, 0.8);
      d.r += (targetR - d.r) * radiusReturn;

      var edgeX = Math.min(d.x, canvas.width - d.x);
      var edgeY = Math.min(d.y, canvas.height - d.y);
      var edgeDist = Math.min(edgeX, edgeY);
      var fade = edgeDist < 50 ? Math.max(0, edgeDist / 50) * 0.5 + 0.5 : 1;

      var offDist = Math.sqrt((d.x - d.ox) * (d.x - d.ox) + (d.y - d.oy) * (d.y - d.oy));
      var alpha = (0.8 + Math.min(offDist * 0.008, 0.2)) * fade;

      if (alpha > 0.02) {
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + color.r + ',' + color.g + ',' + color.b + ',' + alpha.toFixed(2) + ')';
        ctx.fill();
      }
    }

    requestAnimationFrame(draw);
  }

  resize();
  draw();

  window.addEventListener('resize', resize);
})();