/* Agrega «Recursos» al menú y al pie de la portada (exportada desde Framer).
   Framer vuelve a dibujar el menú al cargar, así que el link se inserta después
   y se repone si la página lo vuelve a dibujar. */
(function () {
  var URL = './recursos/';

  function texto(el) { return (el.textContent || '').trim(); }

  function agregarEnMenu() {
    // Menú en píldora: cada opción vive en su propio contenedor; se clona el de «Conferencias».
    document.querySelectorAll('a[data-framer-name="Primary"]').forEach(function (a) {
      if (texto(a) !== 'Conferencias' || a.closest('.pie-hei')) return;
      var caja = a.parentElement;
      if (!caja || caja.parentElement.querySelector('[data-hei-recursos]')) return;
      var nueva = caja.cloneNode(true);
      nueva.setAttribute('data-hei-recursos', '1');
      var link = nueva.querySelector('a');
      link.setAttribute('href', URL);
      link.removeAttribute('data-framer-page-link-current');
      var p = link.querySelector('p') || link;
      p.textContent = 'Recursos';
      caja.parentElement.insertBefore(nueva, caja.nextSibling);
    });
    // Pie de página: los links son párrafos dentro de un <nav>.
    document.querySelectorAll('nav a').forEach(function (a) {
      if (texto(a) !== 'Conferencias' || a.closest('[data-hei-recursos]') || a.closest('.pie-hei')) return;
      var bloque = a.closest('div');
      if (!bloque || bloque.parentElement.querySelector('[data-hei-recursos]')) return;
      var nuevo = bloque.cloneNode(true);
      nuevo.setAttribute('data-hei-recursos', '1');
      var link = nuevo.querySelector('a');
      link.setAttribute('href', URL);
      link.removeAttribute('target');
      link.textContent = 'Recursos';
      bloque.parentElement.insertBefore(nuevo, bloque.nextSibling);
    });
    // «Formaciones» lleva al catálogo (formaciones.html), no directo al taller de Google Workspace.
    document.querySelectorAll('a[href*="google-workspace-ai.html"]').forEach(function (a) {
      if (texto(a) !== 'Formaciones') return;
      a.setAttribute('href', './formaciones.html');
      a.removeAttribute('target');
      a.removeAttribute('rel');
    });
  }

  var pendiente = false;
  function programar() {
    if (pendiente) return;
    pendiente = true;
    requestAnimationFrame(function () { pendiente = false; agregarEnMenu(); });
  }

  function iniciar() {
    agregarEnMenu();
    new MutationObserver(programar).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['href'] });
    // Framer abre el taller con su propio manejador de clic aunque el href ya diga formaciones.html.
    // Se intercepta el clic antes que Framer (fase de captura en window) y se va al catálogo.
    function irAFormaciones(e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a || texto(a) !== 'Formaciones') return;
      e.preventDefault();
      e.stopImmediatePropagation();
      if (e.type === 'click') window.location.href = './formaciones.html';
    }
    window.addEventListener('click', irAFormaciones, true);
    window.addEventListener('auxclick', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (a && texto(a) === 'Formaciones') { e.preventDefault(); e.stopImmediatePropagation(); window.open('./formaciones.html', '_blank'); }
    }, true);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
