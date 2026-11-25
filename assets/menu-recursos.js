/* Agrega «Recursos» al menú y al pie de la portada (exportada desde Framer).
   Framer vuelve a dibujar el menú al cargar, así que el link se inserta después
   y se repone si la página lo vuelve a dibujar. */
(function () {
  var URL = './recursos/';

  function texto(el) { return (el.textContent || '').trim(); }

  function agregarEnMenu() {
    // Menú en píldora: cada opción vive en su propio contenedor; se clona el de «Conferencias».
    document.querySelectorAll('a[data-framer-name="Primary"]').forEach(function (a) {
      if (texto(a) !== 'Conferencias') return;
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
      if (texto(a) !== 'Conferencias' || a.closest('[data-hei-recursos]')) return;
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
  }

  var pendiente = false;
  function programar() {
    if (pendiente) return;
    pendiente = true;
    requestAnimationFrame(function () { pendiente = false; agregarEnMenu(); });
  }

  function iniciar() {
    agregarEnMenu();
    new MutationObserver(programar).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
