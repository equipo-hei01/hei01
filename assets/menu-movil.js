/* Menú móvil común: abre y cierra el desplegable del menú en píldora. */
(function () {
  function iniciar() {
    var btn = document.querySelector('.menu-btn');
    var drop = document.getElementById('nav-drop');
    if (!btn || !drop) return;

    function cerrar() {
      drop.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }
    function abrir() {
      drop.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (drop.hidden) abrir(); else cerrar();
    });
    drop.addEventListener('click', function (e) {
      if (e.target.closest('a')) cerrar();
    });
    document.addEventListener('click', function (e) {
      if (!drop.hidden && !drop.contains(e.target) && e.target !== btn) cerrar();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drop.hidden) { cerrar(); btn.focus(); }
    });
    // Cierra si el foco sale del menú con Tab.
    drop.addEventListener('focusout', function (e) {
      if (!drop.hidden && e.relatedTarget && !drop.contains(e.relatedTarget) && e.relatedTarget !== btn) cerrar();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 820) cerrar();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
