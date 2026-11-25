/* Portada de hei01.com. Sin librerías.
   (Los bloques 3D del hero y de los tres dolores son CSS puro, en bucle; no dependen de este archivo.)
   - IntersectionObserver: agrega .is-in a [data-anim] y arranca los contadores.
   - Un solo listener de scroll pasivo + rAF escribe variables CSS (--p, --f, --v, --a) en las
     secciones [data-scroll] visibles; el CSS las traduce a transform, opacity y stroke-dashoffset.
   - prefers-reduced-motion: no hay deriva, ni contadores, ni escritura de variables; el CSS deja
     cada diagrama en su estado final. (El video de fondo lo maneja fondo-portada.js, no este archivo.)
   Sin JS el contenido se ve completo. */
(function () {
  'use strict';
  var D = document;
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var STICKY = matchMedia('(min-width:900px) and (min-height:780px) and (prefers-reduced-motion:no-preference)');

  function $(s, c) { return (c || D).querySelector(s); }
  function $$(s, c) { return [].slice.call((c || D).querySelectorAll(s)); }
  function cl(v, a, b) { return v < a ? a : v > b ? b : v; }
  function sv(e, k, v) { v = (+v).toFixed(3); var c = e._c || (e._c = {}); if (c[k] === v) return; c[k] = v; e.style.setProperty(k, v); }
  function miles(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }

  /* ---------- Contadores (una vez, ~1,2 s) ---------- */
  function preparar(sec) {
    $$('[data-cuenta]', sec).forEach(function (s) { s.textContent = '0'; });
  }
  function contar(sec) {
    var t0 = null, items = $$('[data-cuenta]', sec);
    function paso(t) {
      if (t0 === null) t0 = t;
      var u = cl((t - t0) / 1200, 0, 1), e = 1 - Math.pow(1 - u, 3);
      items.forEach(function (s) { s.textContent = miles(Math.round(+s.getAttribute('data-cuenta') * e)); });
      if (u < 1) requestAnimationFrame(paso);
    }
    requestAnimationFrame(paso);
  }

  /* ---------- Entrada por sección ---------- */
  function entradas() {
    var lista = $$('[data-anim]');
    if (!('IntersectionObserver' in window)) { lista.forEach(function (e) { e.classList.add('is-in'); }); return; }
    var costo = $('#costo');
    if (costo && !RM) preparar(costo);
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        if (e.target === costo && !RM) contar(costo);
        io.unobserve(e.target);
      });
    }, { threshold: .3 });
    lista.forEach(function (e) { io.observe(e); });
  }

  /* ---------- Scroll: la ruta ---------- */
  var vh = innerHeight;
  var fns = {
    ruta: function (s) {
      var pasos = s._pasos || (s._pasos = $$('.paso', s));
      if (STICKY.matches) {
        var r = $('.ruta-scroll', s).getBoundingClientRect();
        var p = cl(-r.top / Math.max(1, r.height - vh), 0, 1), S = p * 4;
        sv(s, '--p', p);
        pasos.forEach(function (li, i) {
          var lo = i ? cl((S - i + .06) / .12, 0, 1) : 1;
          var hi = i < 3 ? cl((i + 1 - S + .06) / .12, 0, 1) : 1;
          var v = lo * hi;
          sv(li, '--f', cl((S - i) / .85, 0, 1));
          sv(li, '--v', v);
          sv(li, '--a', v);
          li.classList.toggle('on', v > .5);
        });
      } else {
        var w = $('.pasos-wrap', s).getBoundingClientRect();
        sv(s, '--p', cl((vh * .6 - w.top) / w.height, 0, 1));
        pasos.forEach(function (li) {
          var f = $('.paso-fig', li).getBoundingClientRect();
          var v = cl((vh * .92 - f.top) / (f.height * .85), 0, 1);
          sv(li, '--f', v);
          sv(li, '--v', 1);
          sv(li, '--a', 1);
          li.classList.toggle('on', v > 0);
        });
      }
    }
  };

  function scroll() {
    var activos = [];
    function tick() {
      raf = 0;
      vh = innerHeight;
      activos.forEach(function (s) { fns[s.getAttribute('data-scroll')](s); });
    }
    var raf = 0;
    function pedir() { if (!raf) raf = requestAnimationFrame(tick); }
    var secs = $$('[data-scroll]');
    if ('IntersectionObserver' in window) {
      var vis = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var i = activos.indexOf(e.target);
          if (e.isIntersecting && i < 0) activos.push(e.target);
          if (!e.isIntersecting && i >= 0) { activos.splice(i, 1); fns[e.target.getAttribute('data-scroll')](e.target); }
        });
        pedir();
      }, { rootMargin: '25% 0px 25% 0px' });
      secs.forEach(function (s) { vis.observe(s); });
    } else { activos = secs; }
    addEventListener('scroll', pedir, { passive: true });
    addEventListener('resize', pedir);
    pedir();
  }

  /* Un solo detalle abierto por bloque (sin JS cada uno abre por separado). */
  function acordeones() {
    $$('.det-lista').forEach(function (l) {
      var ds = $$('details', l);
      ds.forEach(function (d) {
        d.addEventListener('toggle', function () {
          if (d.open) ds.forEach(function (o) { if (o !== d) o.open = false; });
        });
      });
    });
  }

  // Cada parte arranca por separado: si una falla, las demás siguen funcionando.
  function seguro(f) { try { f(); } catch (e) { if (window.console) console.error(e); } }
  function iniciar() {
    seguro(entradas);
    if (!RM) seguro(scroll);
    seguro(acordeones);
  }
  try {
    if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', iniciar); else iniciar();
  } catch (e) {
    $$('[data-anim]').forEach(function (n) { n.classList.add('is-in'); });
  }
})();
