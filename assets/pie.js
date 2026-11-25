/* ============================================================
   COMPONENTE: pie de página de hei01.com
   Este es el ÚNICO lugar donde se define el footer del sitio.
   Si cambias aquí un texto, link o red social, cambia en todas las páginas.
   Estilos: assets/pie.css

   Uso en una página:
     <link rel="stylesheet" href="assets/pie.css">
     <footer data-componente="pie"></footer>   (en páginas con Vue agregar v-pre)
     <script src="assets/pie.js" data-base="" defer></script>
   data-base = ruta a la raíz del sitio desde la página ("" en la raíz, "../" en /recursos/).
   En el placeholder se puede agregar data-nota="texto" para una línea legal extra.
   En la portada (Framer) reemplaza el footer de Framer.
   ============================================================ */
(function () {
  var script = document.currentScript;
  var BASE = (script && script.getAttribute('data-base')) || '';

  // ---------- CONTENIDO (editar aquí) ----------
  var BAJADA = 'Humanos Empoderados por Inteligencia';
  var LINKS = [
    { texto: 'Orquestación', href: '' },
    { texto: 'Formaciones', href: 'formaciones.html' },
    { texto: 'Conferencias', href: '' },
    { texto: 'Recursos', href: 'recursos/' }
  ];
  var REDES = [
    { nombre: 'Instagram', href: 'https://www.instagram.com/heileengoodson/',
      svg: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/>' },
    { nombre: 'LinkedIn', href: 'https://www.linkedin.com/company/hei01',
      svg: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 10.5V16M8 7.5v.01M11.5 16v-5.5M11.5 13c0-1.6 1-2.5 2.3-2.5s2.2.9 2.2 2.5V16"/>' },
    { nombre: 'YouTube', href: 'https://www.youtube.com/@HEILEENGOODSON',
      svg: '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.5v5l4-2.5z"/>' }
  ];
  // ---------------------------------------------

  function url(h) { return BASE + h || './'; }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function html(nota) {
    var redes = REDES.map(function (r) {
      return '<a href="' + r.href + '" target="_blank" rel="noopener" aria-label="' + r.nombre + '">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + r.svg + '</svg></a>';
    }).join('');
    var links = LINKS.map(function (l) { return '<a href="' + url(l.href) + '">' + l.texto + '</a>'; }).join('');
    return '' +
      '<div class="pie-hei-in">' +
        '<div class="pie-hei-fila">' +
          '<div class="pie-hei-marca">' +
            '<a href="' + url('') + '" class="pie-hei-logo" aria-label="HEI01, ir al inicio"><img src="' + BASE + 'assets/marca/hei01-compacto.svg" alt="HEI01" width="86" height="39"></a>' +
            '<p class="pie-hei-bajada">' + BAJADA + '</p>' +
          '</div>' +
          '<div class="pie-hei-redes">' + redes + '</div>' +
        '</div>' +
        '<nav class="pie-hei-links" aria-label="Pie de página">' + links + '</nav>' +
        '<div class="pie-hei-linea"></div>' +
        '<div class="pie-hei-base">' +
          '<p class="pie-hei-copy">© ' + new Date().getFullYear() + ' HEI01</p>' +
          '<nav class="pie-hei-legal" aria-label="Legal">' +
            '<a href="' + url('privacidad/') + '">Política de privacidad</a>' +
            '<button type="button" class="pie-hei-boton" data-configurar-cookies>Configurar cookies</button>' +
          '</nav>' +
        '</div>' +
        (nota ? '<p class="pie-hei-nota">' + esc(nota) + '</p>' : '') +
      '</div>';
  }

  function crear(nota) {
    var f = document.createElement('footer');
    f.className = 'pie-hei';
    f.innerHTML = html(nota);
    return f;
  }

  function montar() {
    var marcadores = document.querySelectorAll('[data-componente="pie"]');
    if (marcadores.length) {
      // Se rellena el marcador (no se reemplaza) para no romper páginas con Vue.
      marcadores.forEach(function (m) { m.classList.add('pie-hei'); m.innerHTML = html(m.getAttribute('data-nota')); });
      return;
    }
    // Portada (Framer): se oculta su footer (pie.css) y se agrega el componente al final.
    var main = document.getElementById('main');
    if (main && !document.querySelector('footer.pie-hei')) {
      document.documentElement.classList.add('con-pie-hei');
      main.parentNode.insertBefore(crear(''), main.nextSibling);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', montar);
  else montar();
})();
