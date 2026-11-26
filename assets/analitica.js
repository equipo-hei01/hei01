/* ============================================================
   COMPONENTE: medición de hei01.com (Google Tag Manager)
   Único lugar donde se define el contenedor. Todas las páginas cargan este archivo:
     <script src="assets/analitica.js" async></script>      (en /recursos/: ../assets/analitica.js)
   Google Analytics 4 se configura DENTRO de Tag Manager (etiqueta "Google tag" con el ID G-41TTEEDFB5).
   Incluye el aviso de cookies (Modo de consentimiento v2): nada se activa hasta que la persona elige.
     Aceptar todas   -> medición (Analytics) y publicidad (Google Ads)
     Solo medición   -> solo Analytics
     Rechazar        -> nada

   Eventos que se envían a la capa de datos (dataLayer) para usarlos como activadores en GTM:
     cta_agendar      clic en "Agendar sesión" / "Agendar sesión ejecutiva" (calendario o /contact)
     cta_inscribir    clic en "Inscribirme", "Asegurar mi cupo", "Reservar…" o formularios de Google
     buscador_nivel   resultado del buscador "¿Qué nivel necesita mi equipo?" (formaciones.html)
   Cada evento lleva: cta_texto, cta_destino, pagina.
   ============================================================ */
(function () {
  var GTM_ID = 'GTM-5G4MFF75';
  var CLAVE = 'hei01_consentimiento';            // 'aceptado' (todas) | 'medicion' | 'rechazado'
  var VERSION_AVISO = '2026-11-26';                // cambiar para volver a preguntar a todos

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  // ---------- Consentimiento (Ley 21.719 · Modo de consentimiento v2 de Google) ----------
  // Por defecto todo denegado: Analytics no guarda cookies ni identifica al visitante hasta que acepte.
  function leer() { try { var v = JSON.parse(localStorage.getItem(CLAVE) || 'null'); return v && v.version === VERSION_AVISO ? v.estado : null; } catch (e) { return null; } }
  function guardar(estado) { try { localStorage.setItem(CLAVE, JSON.stringify({ estado: estado, version: VERSION_AVISO, fecha: new Date().toISOString() })); } catch (e) {} }
  // estado: 'aceptado' = medición y publicidad · 'medicion' = solo Analytics · cualquier otro = todo denegado
  function permisos(estado) { var m = (estado === 'aceptado' || estado === 'medicion') ? 'granted' : 'denied'; var p = estado === 'aceptado' ? 'granted' : 'denied'; return { analytics_storage: m, ad_storage: p, ad_user_data: p, ad_personalization: p }; }
  if (!window.__heiConsent) {
    window.__heiConsent = true;
    var d = permisos('rechazado'); d.wait_for_update = 500;
    gtag('consent', 'default', d);
    gtag('set', 'ads_data_redaction', true);
    var previo = leer();
    if (previo === 'aceptado' || previo === 'medicion') gtag('consent', 'update', permisos(previo));
  }

  var BASE = (function () { var s = document.currentScript; var src = s && s.getAttribute('src') || ''; return src.indexOf('../') === 0 ? '../' : ''; })();
  var CSS = '' +
    '.hei-cookies{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;padding:20px 22px;border-radius:20px;background:rgba(255,255,255,.97);box-shadow:0 1px 1px -.5px rgba(13,13,18,.17),0 3.6px 3.6px -1.2px rgba(13,13,18,.16),0 18px 36px -6px rgba(13,13,18,.22);font:15px/1.5 Inter,system-ui,sans-serif;color:#0D0D12}' +
    '.hei-cookies p{margin:0 0 14px;color:#3A3A42}.hei-cookies a{color:#0D0D12;text-decoration:underline;text-decoration-color:#FF6F61;text-underline-offset:3px}' +
    '.hei-cookies-btns{display:flex;gap:8px;flex-wrap:wrap}.hei-cookies button{font:500 15px Inter,system-ui,sans-serif;min-height:44px;padding:10px 20px;border-radius:100px;cursor:pointer;border:1px solid #D9D9DE;background:#fff;color:#0D0D12}' +
    '.hei-cookies button.hei-ok{background:#0D0D12;border-color:#0D0D12;color:#fff}.hei-cookies button.hei-ok:hover{background:#FF6F61;border-color:#FF6F61;color:#0D0D12}' +
    '.hei-cookies button:focus-visible{outline:2px solid #0D0D12;outline-offset:2px}' +
    '@media (max-width:480px){.hei-cookies button{flex:1 1 auto}}';

  function aviso() {
    if (document.getElementById('hei-cookies')) return;
    if (!document.getElementById('hei-cookies-css')) { var st = document.createElement('style'); st.id = 'hei-cookies-css'; st.textContent = CSS; document.head.appendChild(st); }
    var c = document.createElement('div');
    c.id = 'hei-cookies'; c.className = 'hei-cookies'; c.setAttribute('role', 'region'); c.setAttribute('aria-label', 'Aviso de cookies');
    c.innerHTML = '<p>Usamos cookies de medición (Google Analytics) para mejorar el sitio y de publicidad (Google Ads) para medir nuestras campañas y mostrarte anuncios de HEI01. Solo se activan si las aceptas. ' +
      '<a href="' + BASE + 'privacidad/">Política de privacidad</a></p>' +
      '<div class="hei-cookies-btns"><button type="button" class="hei-ok" data-c="aceptado">Aceptar todas</button><button type="button" data-c="medicion">Solo medición</button><button type="button" data-c="rechazado">Rechazar</button></div>';
    c.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-c]'); if (!b) return;
      var estado = b.getAttribute('data-c');
      guardar(estado);
      gtag('consent', 'update', permisos(estado));
      // 'consentimiento_aceptado' es el activador de la etiqueta de Google en GTM: se envía también con 'Solo medición'.
      window.dataLayer.push({ event: estado === 'rechazado' ? 'consentimiento_rechazado' : 'consentimiento_aceptado', consentimiento_alcance: estado === 'aceptado' ? 'todas' : estado });
      c.remove();
    });
    document.body.appendChild(c);
  }
  // Cualquier enlace o botón con data-configurar-cookies vuelve a abrir el aviso (footer, política).
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-configurar-cookies]');
    if (t) { e.preventDefault(); aviso(); }
  });
  function iniciarAviso() { if (!leer()) aviso(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciarAviso);
  else iniciarAviso();
  // ----------------------------------------------------------------------------------------

  if (!window.__heiGtm) {
    window.__heiGtm = true;
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    var primero = document.getElementsByTagName('script')[0];
    primero.parentNode.insertBefore(s, primero);
  }

  function texto(el) { return (el.textContent || el.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim(); }
  function enviar(evento, el, destino) {
    window.dataLayer.push({ event: evento, cta_texto: texto(el).slice(0, 80), cta_destino: destino || '', pagina: location.pathname });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a, button');
    if (!a) return;
    var t = texto(a).toLowerCase();
    var href = a.getAttribute('href') || '';
    if (/agendar|agenda y conversemos/.test(t) || /calendar\.(app\.)?google|(^|\/)contact\/?(\?|$)/.test(href)) {
      enviar('cta_agendar', a, href);
    } else if (/inscrib|asegurar mi cupo|reservar/.test(t) || /forms\.gle|docs\.google\.com\/forms/.test(href)) {
      enviar('cta_inscribir', a, href);
    }
  }, true);

  // Buscador de nivel (formaciones.html): se envía cuando aparece el resultado.
  function vigilarBuscador() {
    var caja = document.getElementById('buscador-nivel');
    if (!caja) return;
    var ultimo = '';
    new MutationObserver(function () {
      var r = caja.querySelector('[role="status"]');
      if (!r) return;
      var t = (r.innerText || '').trim();
      var nivel = (t.match(/Nivel\s*\d[^\n]*/) || [''])[0];
      if (nivel && nivel !== ultimo) {
        ultimo = nivel;
        window.dataLayer.push({ event: 'buscador_nivel', nivel_recomendado: nivel, pagina: location.pathname });
      }
    }).observe(caja, { childList: true, subtree: true, characterData: true, attributes: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', vigilarBuscador);
  else vigilarBuscador();
})();
