/* Asegura que el video de fondo (ondas) se reproduzca, como en la portada.
   - Vue (página del taller) vuelve a dibujar el body y quita el atributo muted, lo que bloquea el autoplay.
   - Algunos navegadores no inician el autoplay si la pestaña cargó en segundo plano.
   Por eso se marca como silenciado y se reintenta durante unos segundos. */
(function () {
  // Decisión de la dueña: se reproduce aunque el sistema pida menos movimiento.
  function reproducir() {
    var v = document.querySelector('.fondo-portada video');
    if (!v) return false;
    v.muted = true;
    v.defaultMuted = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    if (v.paused) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    return !v.paused;
  }
  var intentos = 0;
  var t = setInterval(function () {
    intentos++;
    if (reproducir() && intentos > 4) clearInterval(t);
    if (intentos > 20) clearInterval(t);
  }, 500);
  window.addEventListener('load', reproducir);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) reproducir(); });
})();
