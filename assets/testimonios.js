/* Componente compartido de testimonios de hei01.com.
   Uso: <section data-componente="testimonios"></section> y, al final de la página,
        <script src="assets/testimonios.js" data-base="" defer></script>
        (data-base="../" en páginas dentro de una carpeta).
   Para cambiar un testimonio en todo el sitio, edita solo la lista TESTIMONIOS de este archivo.

   Reglas de contenido: solo citas textuales y autorizadas por la persona (nombre y empresa).
   No resumir ni "mejorar" las citas. Fuente: banco de pruebas de HEI01. */
(function () {
  'use strict';
  var script = document.currentScript;
  var BASE = (script && script.getAttribute('data-base')) || '';

  // ---------- CONTENIDO (editar aquí) ----------
  var ETIQUETA = 'Formación en IA para ejecutivos';
  var TITULO = 'Lo que se llevan quienes ya trabajaron con nosotros.';
  /* Cada testimonio: cita (textual), nombre, cargo y empresa. Opcional:
       video:  'assets/testimonios/nombre.mp4'   video vertical 4:5, liviano (720x900)
       poster: 'assets/testimonios/nombre.webp'  imagen que se ve antes de reproducir
     Sin video, la tarjeta muestra solo la cita. */
  var TESTIMONIOS = [
    { cita: 'Me llevo la tranquilidad de poder incorporar la gobernanza de la IA al día a día de nuestra empresa.',
      nombre: 'Lorena Ramis', cargo: 'Cofundadora y CCO', empresa: 'Fincloud',
      video: 'assets/testimonios/lorena-ramis.mp4?v=2', poster: 'assets/testimonios/lorena-ramis.webp?v=2' },
    { cita: 'Con herramientas prácticas logramos salir con resultados concretos, a pesar de que fueron 2 mañanas de trabajo.',
      nombre: 'Javier Ramírez', cargo: 'CEO', empresa: 'WeDo Cowork',
      video: 'assets/testimonios/javier-ramirez.mp4', poster: 'assets/testimonios/javier-ramirez.webp' },
    { cita: 'Fue bien informativo, pero también bien práctico. No solamente estuvo en la teoría: entregó la información y empezamos a aplicar.',
      nombre: 'Cristóbal Matamala', cargo: 'CEO y cofundador', empresa: 'CF Ingenieros',
      video: 'assets/testimonios/cristobal-matamala.mp4', poster: 'assets/testimonios/cristobal-matamala.webp' },
    { cita: 'Este programa genera una ruta clara, considerando todas las variables, tanto lo técnico como lo humano.',
      nombre: 'Marcelo Alvarez', cargo: 'Fundador', empresa: 'alvarezcastelli',
      video: 'assets/testimonios/marcelo-alvarez.mp4', poster: 'assets/testimonios/marcelo-alvarez.webp' }
  ];
  // ---------------------------------------------

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function local(u) { return /^assets\/[\w\/.-]+(\?v=\d+)?$/.test(u) ? BASE + u : ''; }

  function tarjeta(t) {
    var video = t.video ? local(t.video) : '';
    var poster = t.poster ? local(t.poster) : '';
    var detalle = [t.cargo, t.empresa].filter(Boolean).map(esc).join(' · ');
    return '<li class="tst-tarjeta' + (video ? ' tst-con-video' : '') + '"><figure>' +
      (video ? '<video class="tst-video" controls playsinline preload="none"' + (poster ? ' poster="' + esc(poster) + '"' : '') +
               ' aria-label="Testimonio en video de ' + esc(t.nombre) + '"><source src="' + esc(video) + '" type="video/mp4"></video>' : '') +
      '<blockquote><p>“' + esc(t.cita) + '”</p></blockquote>' +
      '<figcaption><strong>' + esc(t.nombre) + '</strong>' + (detalle ? '<span>' + detalle + '</span>' : '') + '</figcaption>' +
      '</figure></li>';
  }

  function montar() {
    var nodos = document.querySelectorAll('[data-componente="testimonios"]');
    [].forEach.call(nodos, function (n, i) {
      if (!TESTIMONIOS.length) { n.hidden = true; return; }
      var id = 'tst-titulo-' + i;
      n.classList.add('tst');
      n.setAttribute('aria-labelledby', id);
      n.innerHTML = '<div class="tst-in">' +
        '<p class="tst-etiqueta">' + esc(ETIQUETA) + '</p>' +
        '<h2 class="tst-titulo" id="' + id + '">' + esc(TITULO) + '</h2>' +
        '<ul class="tst-lista">' + TESTIMONIOS.map(tarjeta).join('') + '</ul>' +
      '</div>';
      var vids = n.querySelectorAll('video');
      [].forEach.call(vids, function (v) {
        v.addEventListener('play', function () { [].forEach.call(vids, function (o) { if (o !== v) o.pause(); }); });
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', montar); else montar();
})();
