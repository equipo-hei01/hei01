// Biblioteca de recursos HEI01 · generado por recursos/_fuente/build.py
(function(){
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // aparición al hacer scroll, escalonada
  var obs = 'IntersectionObserver' in window && !quieto ? new IntersectionObserver(function(es){
    es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('visto'); obs.unobserve(en.target); } });
  }, {threshold:.12}) : null;
  document.querySelectorAll('.revela').forEach(function(el, i){
    if(!obs){ el.classList.add('visto'); return; }
    el.style.transitionDelay = (el.dataset.retraso || (i % 3) * 90) + 'ms';
    obs.observe(el);
  });
  // vitrina: un recurso a la vez se muestra trabajando
  var vit = document.getElementById('vitrina');
  if(vit){
    var minis = [].slice.call(vit.querySelectorAll('.mini')), botones = [].slice.call(document.querySelectorAll('.leyenda button')), act = -1, reloj;
    function mostrar(i){
      act = i;
      minis.forEach(function(m, j){ m.classList.remove('activa'); if(j === i){ void m.offsetWidth; m.classList.add('activa'); } });
      botones.forEach(function(b, j){ b.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
    }
    function siguiente(){ mostrar((act + 1) % minis.length); }
    function andar(){ clearInterval(reloj); if(!quieto) reloj = setInterval(siguiente, 4500); }
    botones.forEach(function(b){ b.addEventListener('click', function(){ mostrar(+b.dataset.i); andar(); }); });
    minis.forEach(function(m){ m.addEventListener('mouseenter', function(){ mostrar(+m.dataset.i); andar(); }); });
    mostrar(1); andar();
  }
  // prompt en vivo: se escribe letra a letra la primera vez que se ve
  document.querySelectorAll('.prompt pre').forEach(function(pre){
    var texto = pre.textContent; pre.dataset.texto = texto;
    if(quieto || !('IntersectionObserver' in window)) return;
    pre.textContent = '';
    var cursor = document.createElement('span'); cursor.className = 'cursor'; cursor.textContent = ' ';
    var io = new IntersectionObserver(function(es){
      if(!es[0].isIntersecting) return; io.disconnect();
      var i = 0, nodo = document.createTextNode(''); pre.appendChild(nodo); pre.appendChild(cursor);
      var paso = Math.max(1, Math.round(texto.length / 260));
      (function escribe(){ i = Math.min(texto.length, i + paso); nodo.data = texto.slice(0, i);
        if(i < texto.length) setTimeout(escribe, 14); else setTimeout(function(){ cursor.remove(); }, 1600); })();
    }, {threshold:.3});
    io.observe(pre);
  });
  document.querySelectorAll('.copiar').forEach(function(b){
    b.addEventListener('click', function(){
      var t = b.closest('.prompt').querySelector('pre').dataset.texto;
      var ok = function(){ b.textContent = 'Copiado ✓'; setTimeout(function(){ b.textContent = 'Copiar prompt'; }, 1800); };
      if(navigator.clipboard) navigator.clipboard.writeText(t).then(ok).catch(function(){});
      try{ window.dataLayer = window.dataLayer || []; dataLayer.push({event:'copiar_prompt', recurso:location.pathname}); }catch(e){}
    });
  });
  // buscador y filtros (solo en la portada de la biblioteca)
  var q = document.getElementById('q'); if(!q) return;
  var tarjetas = [].slice.call(document.querySelectorAll('.grilla .tarjeta')),
      cuenta = document.getElementById('cuenta'), vacio = document.getElementById('vacio'), limpiar = document.getElementById('limpiar'),
      sel = {para:[], necesidad:[], tipo:[]};
  function norm(s){ return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function aplicar(){
    var txt = norm(q.value.trim()), n = 0;
    tarjetas.forEach(function(t){
      var ok = !txt || norm(t.dataset.texto).indexOf(txt) > -1;
      ['para','necesidad','tipo'].forEach(function(g){
        if(ok && sel[g].length){ var v = t.dataset[g].split(' '); ok = sel[g].some(function(x){ return v.indexOf(x) > -1; }); }
      });
      t.style.display = ok ? '' : 'none'; if(ok){ n++; t.classList.add('visto'); }
    });
    cuenta.textContent = n + (n === 1 ? ' recurso' : ' recursos');
    vacio.style.display = n ? 'none' : 'block';
    limpiar.hidden = !(txt || sel.para.length || sel.necesidad.length || sel.tipo.length);
    var p = new URLSearchParams();
    ['para','necesidad','tipo'].forEach(function(g){ if(sel[g].length) p.set(g, sel[g].join(',')); });
    if(txt) p.set('q', q.value.trim());
    history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
  }
  document.querySelectorAll('.grupo').forEach(function(c){
    var g = c.dataset.grupo;
    c.addEventListener('click', function(ev){
      var b = ev.target.closest('.chip'); if(!b) return;
      var v = b.dataset.valor, i = sel[g].indexOf(v);
      if(i > -1){ sel[g].splice(i, 1); b.setAttribute('aria-pressed', 'false'); } else { sel[g].push(v); b.setAttribute('aria-pressed', 'true'); }
      aplicar();
    });
  });
  q.addEventListener('input', aplicar);
  limpiar.addEventListener('click', function(){
    q.value = ''; Object.keys(sel).forEach(function(g){ sel[g] = []; });
    document.querySelectorAll('.chip').forEach(function(b){ b.setAttribute('aria-pressed', 'false'); }); aplicar();
  });
  var p = new URLSearchParams(location.search);
  ['para','necesidad','tipo'].forEach(function(g){
    (p.get(g) || '').split(',').filter(Boolean).forEach(function(v){
      var b = document.querySelector('.grupo[data-grupo="' + g + '"] .chip[data-valor="' + v + '"]');
      if(b){ sel[g].push(v); b.setAttribute('aria-pressed', 'true'); }
    });
  });
  if(p.get('q')) q.value = p.get('q');
  aplicar();
})();
