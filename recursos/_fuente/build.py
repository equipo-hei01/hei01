"""Construye la Biblioteca de recursos de HEI01 (hei01.com/recursos/).

Uso:  python -X utf8 recursos/_fuente/build.py   (desde la raíz del repo)

Lee recursos/_fuente/recursos.json y escribe:
  recursos/index.html          la biblioteca con buscador y filtros
  recursos/<slug>.html         una página por recurso
  recursos/recursos.css        estilos (mismo lenguaje visual que la portada de hei01.com)
  recursos/recursos.js         animaciones, filtros y botón copiar
y agrega las páginas a sitemap.xml. La carpeta _fuente no se publica (GitHub Pages ignora las carpetas que empiezan con _).
Para sumar un recurso: agrega un objeto al JSON con la misma forma y vuelve a correr este script.
"""
import html, io, json, os, re, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(RAIZ, 'recursos')
DOMINIO = 'https://hei01.com'
HOY = datetime.date.today().isoformat()
AGENDA = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ1PQZrGvaF53wBSMlrRLVGigUUl3GasROhOxy6AEsgrtlvdHRfxye6OBRsKI6WdBp5pTV-G0AL4'

PARA = {'directorio': 'Directorio y gerencia general', 'transformacion': 'Transformación e innovación', 'personas': 'Personas y RR. HH.'}
NECESIDAD = {'gobernar': 'Gobernar', 'decidir': 'Decidir', 'priorizar': 'Priorizar', 'comunicar': 'Comunicar el cambio', 'formar': 'Formar a mi equipo'}
TIPO = {'checklist': 'Checklist', 'prompt': 'Prompt', 'plantilla': 'Plantilla', 'ejercicio': 'Ejercicio', 'guia': 'Guía', 'test': 'Test'}

# Íconos de línea, en rosa como los de los módulos de la portada.
ICONO = {
    'checklist': '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/>',
    'prompt': '<path d="M8 9l-4 3 4 3"/><path d="M16 9l4 3-4 3"/><path d="M13.5 6l-3 12"/>',
    'plantilla': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    'ejercicio': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    'guia': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5"/><path d="M9 7h6"/>',
    'test': '<path d="M3 12a9 9 0 1 0 9-9"/><path d="M12 3v9l6 3"/>',
}

e = lambda s: html.escape(str(s), quote=True)


def leer(p):
    return io.open(p, encoding='utf8').read()


def escribir(p, s):
    io.open(p, 'w', encoding='utf8', newline='\n').write(s)


_f = leer(os.path.join(RAIZ, 'formaciones.html'))
GTM = re.search(r'<script>\(function\(w,d,s,l,i\).*?</script>', _f, re.S).group(0)


def icono(tipo, tam=22):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONO[tipo]}</svg>')


def cabeza(titulo, descripcion, url):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="../assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:locale" content="es_ES">
<meta property="og:image" content="{DOMINIO}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{GTM}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="recursos.css">
</head>
<body>
<div class="fondo" aria-hidden="true">
  <svg class="lineas" viewBox="0 0 1440 900" preserveAspectRatio="none"><path d="M-40 260C260 120 420 520 760 380s520-360 760-120"/><path d="M1180-20c-60 220 120 360 300 420"/><path d="M-60 640c240-80 380 40 560 0"/></svg>
  <img class="nube nube-1" src="../assets/module-image.webp" alt="">
  <img class="nube nube-2" src="../assets/module-image.webp" alt="">
</div>
<header class="barra">
  <nav class="nav-pill" aria-label="Principal">
    <a href="../" class="nav-logo"><img src="../assets/hero-bg.png" alt="HEI01" width="80" height="32"></a>
    <a href="../" class="nav-link">Orquestación</a>
    <a href="../formaciones.html" class="nav-link">Formaciones</a>
    <a href="./" class="nav-link activo" aria-current="page">Recursos</a>
    <a href="../contact/" class="btn-oscuro">Agendar sesión →</a>
  </nav>
</header>
'''


PIE = f'''<footer class="pie">
  <div class="contenedor pie-inner">
    <div>
      <img src="../assets/hero-bg.png" alt="HEI01" width="110" height="44">
      <p class="pie-tag">IA que deja huella.</p>
      <p class="suave">Human Empowered Intelligence · Santiago, Chile · Latam + España</p>
    </div>
    <div class="pie-links">
      <a href="https://linkedin.com/in/heileengoodson" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://instagram.com/heileengoodson" target="_blank" rel="noopener">Instagram</a>
      <a href="https://youtube.com/@heileengoodson" target="_blank" rel="noopener">YouTube</a>
    </div>
  </div>
  <p class="contenedor suave pie-bajo">© {datetime.date.today().year} HEI01 · Los recursos son de libre uso citando la fuente.</p>
</footer>
<script src="recursos.js" defer></script>
'''

CSS = '''/* Biblioteca de recursos HEI01 · generado por recursos/_fuente/build.py (no editar a mano) */
:root{--tinta:#15131A;--suave:#6E6B65;--rosa:#E8678A;--violeta:#7C3AED;--lila:#F6F1FC;--lavanda:#D8B4FE;--borde:rgba(21,19,26,.07);
--vidrio:linear-gradient(rgba(255,255,255,.92),rgba(255,255,255,.5));
--sombra:0 .8px .8px -1px rgba(0,0,0,.04),0 2.4px 2.4px -2px rgba(0,0,0,.04),0 6.4px 6.4px -3px rgba(0,0,0,.03),0 20px 40px -6px rgba(36,10,90,.07);
--sombra-alta:0 1px 1px -.5px rgba(16,0,69,.17),0 3.6px 3.6px -1.2px rgba(16,0,69,.16),0 18px 36px -6px rgba(16,0,69,.22);
--ease:cubic-bezier(.22,1,.36,1)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:#fff;color:var(--tinta);font-family:Inter,system-ui,sans-serif;font-size:16px;line-height:1.6;letter-spacing:-.01em;overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:inherit}
.suave{color:var(--suave)}
.contenedor{max-width:1080px;margin:0 auto;padding:0 20px}
.angosto{max-width:760px}
/* fondo como la portada: lila suave, líneas curvas y nubes que flotan */
.fondo{position:fixed;inset:0;z-index:-1;overflow:hidden;background:radial-gradient(70% 55% at 50% 0%,#EEE7FA 0%,rgba(246,241,252,.6) 45%,#fff 80%)}
.lineas{position:absolute;inset:0;width:100%;height:100%;fill:none;stroke:#fff;stroke-width:2.2;opacity:.9;filter:drop-shadow(0 2px 6px rgba(124,58,237,.08))}
.nube{position:absolute;width:520px;opacity:.28;mix-blend-mode:multiply;filter:blur(2px);animation:flotar 22s ease-in-out infinite}
.nube-1{top:8%;left:-140px}.nube-2{top:52%;right:-180px;width:620px;animation-duration:28s;animation-delay:-8s}
@keyframes flotar{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-18px)}}
/* navegación en píldora, como la de la portada */
.barra{position:sticky;top:18px;z-index:20;display:flex;justify-content:center;padding:0 12px}
.nav-pill{display:flex;align-items:center;gap:10px;width:min(780px,100%);background:var(--vidrio);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-radius:100px;padding:12px 12px 12px 30px;box-shadow:var(--sombra)}
.nav-pill .btn-oscuro{margin-left:auto;padding:12px 24px}
.nav-pill .nav-logo{margin-right:auto}
.nav-logo img{display:block;height:34px;width:auto}
.nav-link{font-size:15px;font-weight:500;color:var(--suave);text-decoration:none;padding:9px 16px;border-radius:100px;transition:color .2s,background .2s}
.nav-link:hover{color:var(--tinta)}
.nav-link.activo{color:var(--tinta);background:var(--lila)}
.btn-oscuro{white-space:nowrap;display:inline-flex;align-items:center;gap:6px;background:var(--tinta);color:#fff;text-decoration:none;font-weight:500;font-size:15px;padding:10px 20px;border-radius:100px;box-shadow:var(--sombra-alta);transition:transform .25s var(--ease),box-shadow .25s}
.btn-oscuro:hover{transform:translateY(-2px);box-shadow:0 0 0 4px rgba(232,103,138,.18),var(--sombra-alta)}
.btn-claro{display:inline-flex;align-items:center;gap:6px;background:var(--vidrio);color:var(--tinta);text-decoration:none;font-weight:500;padding:10px 20px;border-radius:100px;box-shadow:var(--sombra);transition:transform .25s var(--ease)}
.btn-claro:hover{transform:translateY(-2px)}
/* etiquetas en píldora */
.pildora{display:inline-flex;align-items:center;gap:8px;background:var(--vidrio);border-radius:100px;padding:6px 16px;box-shadow:var(--sombra);font-size:13px;font-weight:500;color:var(--suave);letter-spacing:.02em;text-transform:uppercase}
.punto{position:relative;width:7px;height:7px;border-radius:50%;background:var(--tinta)}
.punto::after{content:"";position:absolute;inset:-4px;border-radius:50%;border:1.5px solid var(--rosa);animation:pulso 2s var(--ease) infinite}
@keyframes pulso{0%{transform:scale(.4);opacity:1}100%{transform:scale(1.8);opacity:0}}
/* hero */
.hero{text-align:center;padding:72px 0 24px}
.hero h1{font-weight:400;font-size:clamp(38px,6.4vw,72px);line-height:1.04;letter-spacing:-.04em;margin:22px auto 18px;max-width:900px}
.hero h1 .rosa{color:var(--rosa)}
.hero p{max-width:600px;margin:0 auto;color:var(--suave);font-weight:500;font-size:17px}
.hero .hero-nota{margin-top:10px;color:var(--tinta);font-size:15px}
.palabra{display:inline-block;opacity:0;filter:blur(8px);transform:translateY(18px);animation:aparecer .9s var(--ease) forwards}
@keyframes aparecer{to{opacity:1;filter:blur(0);transform:none}}
/* vitrina: cuatro recursos en miniatura que se muestran trabajando (prompt, checklist, plantilla, ejercicio) */
.vitrina{position:relative;height:340px;max-width:880px;margin:34px auto 0;perspective:1500px}
.mini{position:absolute;top:34px;left:50%;width:214px;height:256px;margin-left:-107px;border-radius:18px;background:var(--vidrio);
 box-shadow:var(--sombra),0 30px 50px -20px rgba(60,20,140,.22);padding:16px 16px 14px;display:flex;flex-direction:column;gap:10px;text-align:left;
 transform:translateX(var(--x)) translateY(var(--y,0)) rotateY(var(--ry)) rotateZ(var(--rz,0deg)) scale(var(--e,.94));transition:transform .9s var(--ease),box-shadow .9s,opacity .9s;opacity:.9}
.mini::before{content:"";position:absolute;inset:-1px;border-radius:18px;padding:1.5px;background:linear-gradient(135deg,var(--rosa),var(--violeta));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .9s}
.mini.activa{--e:1.06;--y:-18px;opacity:1;z-index:5;box-shadow:var(--sombra),0 44px 70px -22px rgba(124,58,237,.38)}
.mini.activa::before{opacity:1}
.m1{--x:-330px;--ry:22deg;--rz:-2deg;z-index:1}.m2{--x:-110px;--ry:8deg;z-index:2}.m3{--x:110px;--ry:-8deg;z-index:2}.m4{--x:330px;--ry:-22deg;--rz:2deg;z-index:1}
.mini-top{display:flex;justify-content:space-between;align-items:center}
.mini-top .tipo{box-shadow:none;background:var(--lila);font-size:11px;padding:3px 10px}
.mini-top .icono{color:var(--rosa);display:flex}
.mini h4{font-size:14px;font-weight:600;line-height:1.25;letter-spacing:-.01em}
.mini-pie{white-space:nowrap;margin-top:auto;font-size:11px;color:var(--suave);font-weight:500}
/* prompt que se escribe */
.term{background:var(--tinta);border-radius:12px;padding:10px 11px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;line-height:1.55;color:#EDE9F6;flex:1;position:relative;overflow:hidden}
.term .lin{display:block;white-space:nowrap;overflow:hidden;width:0;border-right:2px solid transparent}
.activa .term .lin{animation:escribir 1.1s steps(26) forwards}
.activa .term .l2{animation-delay:1.1s}.activa .term .l3{animation-delay:2.2s}
.activa .term .l3{border-right-color:var(--rosa)}
@keyframes escribir{to{width:100%}}
.term .gris{color:rgba(255,255,255,.45)}.term .rosa{color:#F5A3B9}
.copiado{position:absolute;right:8px;bottom:8px;background:#fff;color:var(--tinta);font-family:Inter,sans-serif;font-size:10px;font-weight:600;border-radius:100px;padding:3px 9px;opacity:0;transform:translateY(6px)}
.activa .copiado{animation:copiado .5s var(--ease) 3.4s forwards}
@keyframes copiado{to{opacity:1;transform:none}}
/* checklist que se marca */
.check{list-style:none;display:grid;gap:7px;font-size:11.5px;font-weight:500;color:#3b3843}
.check li{display:flex;gap:8px;align-items:center}
.check b{flex:0 0 16px;height:16px;border-radius:5px;border:1.5px solid #D6CFE6;display:grid;place-items:center;transition:all .3s}
.check b::after{content:"";width:7px;height:4px;border-left:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-45deg) scale(0);margin-top:-2px;transition:transform .3s var(--ease)}
.activa .check li b{animation:marca .4s var(--ease) forwards}
.activa .check li:nth-child(1) b{animation-delay:.3s}.activa .check li:nth-child(2) b{animation-delay:1s}.activa .check li:nth-child(3) b{animation-delay:1.7s}
@keyframes marca{to{background:var(--rosa);border-color:var(--rosa)}}
.activa .check li:nth-child(1) b::after{transform:rotate(-45deg) scale(1);transition-delay:.4s}
.activa .check li:nth-child(2) b::after{transform:rotate(-45deg) scale(1);transition-delay:1.1s}
.activa .check li:nth-child(3) b::after{transform:rotate(-45deg) scale(1);transition-delay:1.8s}
.puntaje{white-space:nowrap;gap:6px;display:flex;justify-content:space-between;align-items:center;font-size:11px;font-weight:600;background:var(--lila);border-radius:10px;padding:6px 10px}
.puntaje span{color:var(--rosa);opacity:0}.activa .puntaje span{animation:copiado .5s var(--ease) 2.4s forwards}
/* plantilla que se llena */
.tab{display:grid;gap:6px}
.fila{display:grid;grid-template-columns:74px 1fr;gap:8px;align-items:center;font-size:10.5px;font-weight:600;color:var(--suave)}
.fila i{display:block;height:9px;border-radius:5px;background:linear-gradient(90deg,var(--lavanda),var(--rosa));transform-origin:left;transform:scaleX(.06);opacity:.55}
.activa .fila i{animation:llenar .7s var(--ease) forwards}
.activa .fila:nth-child(2) i{animation-delay:.6s}.activa .fila:nth-child(3) i{animation-delay:1.2s}.activa .fila:nth-child(4) i{animation-delay:1.8s}
@keyframes llenar{to{transform:scaleX(var(--w,1));opacity:1}}
/* ejercicio paso a paso */
.paso{display:flex;gap:9px;align-items:center;font-size:11.5px;font-weight:500;color:#3b3843}
.paso b{flex:0 0 22px;height:22px;border-radius:50%;background:#fff;box-shadow:var(--sombra);display:grid;place-items:center;font-size:10.5px;color:var(--suave)}
.activa .paso b{animation:paso .4s var(--ease) forwards}
.activa .paso:nth-child(2) b{animation-delay:.9s}.activa .paso:nth-child(3) b{animation-delay:1.8s}
@keyframes paso{to{background:var(--tinta);color:#fff}}
.barra-progreso{height:6px;border-radius:6px;background:var(--lila);overflow:hidden}
.barra-progreso i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--violeta),var(--rosa));border-radius:6px}
.activa .barra-progreso i{animation:progreso 2.6s var(--ease) forwards}
@keyframes progreso{to{width:100%}}
/* leyenda bajo la vitrina */
.leyenda{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:6px}
.leyenda button{border:0;background:none;font:inherit;font-size:13px;font-weight:500;color:var(--suave);padding:6px 12px;border-radius:100px;cursor:pointer;transition:all .3s}
.leyenda button[aria-pressed="true"]{background:var(--tinta);color:#fff}
@keyframes flota{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
/* buscador y filtros */
.herramientas{position:relative;margin:56px auto 28px;max-width:980px;background:#fff;border-radius:28px;padding:40px 44px 36px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 24px 60px -20px rgba(60,20,140,.18);border:1px solid rgba(124,58,237,.08)}
.panel-cabeza{text-align:center;margin-bottom:26px}
.panel-cabeza h2{font-weight:400;font-size:clamp(28px,3.6vw,38px);letter-spacing:-.035em;line-height:1.1;margin:16px 0 8px}
.panel-cabeza p{color:var(--suave);font-weight:500;max-width:520px;margin:0 auto}
.buscador{position:relative}
.buscador input{width:100%;padding:18px 22px 18px 54px;border-radius:100px;border:1px solid rgba(124,58,237,.12);background:var(--lila);box-shadow:none;font:inherit;font-size:16px;color:var(--tinta)}
.buscador input:focus{outline:2px solid var(--lavanda)}
.buscador svg{position:absolute;left:20px;top:50%;transform:translateY(-50%);color:var(--suave)}
.filtros{display:grid;gap:0;margin-top:26px}
.grupo{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:12px;padding:18px 0;border-top:1px solid var(--borde)}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.grupo-titulo{font-size:12px;font-weight:600;color:var(--suave);text-transform:uppercase;letter-spacing:.06em;margin-right:10px;min-width:130px}
.chip{border:1px solid rgba(21,19,26,.08);background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.04);color:var(--tinta);font:inherit;font-size:14px;font-weight:500;padding:9px 17px;border-radius:100px;cursor:pointer;transition:transform .2s var(--ease),background .2s,color .2s}
.chip:hover{transform:translateY(-1px);border-color:var(--lavanda)}
.chip[aria-pressed="true"]{background:var(--tinta);color:#fff}
.estado{display:flex;justify-content:space-between;align-items:center;margin:28px auto 18px;max-width:980px;font-size:14px;color:var(--suave)}
.limpiar{background:none;border:0;font:inherit;color:var(--violeta);cursor:pointer;text-decoration:underline}
/* tarjetas de vidrio */
.grilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;padding-bottom:30px}
.tarjeta{position:relative;display:flex;flex-direction:column;gap:12px;padding:28px 28px 26px;border-radius:16px;background:var(--vidrio);box-shadow:var(--sombra);text-decoration:none;color:var(--tinta);overflow:hidden;transition:transform .35s var(--ease),box-shadow .35s}
.tarjeta::before{content:"";position:absolute;inset:-1px;border-radius:16px;padding:1px;background:linear-gradient(135deg,rgba(232,103,138,.0),rgba(232,103,138,.55),rgba(124,58,237,.45));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .35s}
.tarjeta:hover{transform:translateY(-6px);box-shadow:0 30px 60px -18px rgba(60,20,140,.25)}
.tarjeta:hover::before{opacity:1}
.tarjeta .icono{color:var(--rosa)}
.tarjeta .min{position:absolute;top:22px;right:22px;font-size:12px;font-weight:500;color:var(--suave);background:#fff;border-radius:100px;padding:3px 10px;box-shadow:var(--sombra)}
.tarjeta h3{font-size:20px;font-weight:600;line-height:1.22;letter-spacing:-.02em}
.tarjeta p{color:var(--suave);font-weight:500;font-size:15px;flex:1}
.tipo{display:inline-block;font-size:12px;font-weight:600;color:var(--tinta);background:#fff;border-radius:100px;padding:4px 12px;box-shadow:var(--sombra);align-self:flex-start}
.para{font-size:13px;color:var(--suave)}
.vacio{display:none;text-align:center;padding:40px;border-radius:16px;background:var(--vidrio);box-shadow:var(--sombra);margin-bottom:40px}
/* aparición al hacer scroll */
.revela{opacity:0;transform:translateY(28px);filter:blur(6px);transition:opacity .8s var(--ease),transform .8s var(--ease),filter .8s var(--ease)}
.revela.visto{opacity:1;transform:none;filter:none}
/* página de recurso */
.migas{margin:42px 0 14px;font-size:14px}.migas a{text-decoration:none;color:var(--suave)}.migas a:hover{color:var(--tinta)}
.articulo h1{font-weight:400;font-size:clamp(32px,5vw,52px);line-height:1.08;letter-spacing:-.035em;margin:16px 0 14px}
.bajada{font-size:18px;color:var(--suave);font-weight:500}
.ficha{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:28px 0 34px}
.ficha div{background:var(--vidrio);box-shadow:var(--sombra);border-radius:16px;padding:14px 18px;font-weight:500}
.ficha span{display:block;font-size:12px;color:var(--suave);text-transform:uppercase;letter-spacing:.06em;font-weight:600;margin-bottom:2px}
.seccion{margin:34px 0}
.seccion h2,.seccion h3{font-size:22px;font-weight:600;letter-spacing:-.02em;margin-bottom:12px}
.seccion p{color:#3b3843}
.caja{background:var(--vidrio);box-shadow:var(--sombra);border-radius:16px;padding:22px 24px;margin:14px 0}
ol.numerada{counter-reset:n var(--inicio,0);list-style:none;display:grid;gap:10px}
ol.numerada li{counter-increment:n;position:relative;padding:14px 18px 14px 58px;background:var(--vidrio);box-shadow:var(--sombra);border-radius:14px;font-weight:500}
ol.numerada li::before{content:counter(n);position:absolute;left:16px;top:50%;transform:translateY(-50%);width:28px;height:28px;border-radius:50%;background:#fff;box-shadow:var(--sombra);display:grid;place-items:center;font-size:13px;font-weight:600;color:var(--rosa)}
ol.pasos{list-style:none;counter-reset:p;display:grid;gap:14px}
ol.pasos li{counter-increment:p;position:relative;padding-left:48px}
ol.pasos li::before{content:counter(p);position:absolute;left:0;top:-2px;width:32px;height:32px;border-radius:50%;background:var(--tinta);color:#fff;display:grid;place-items:center;font-weight:600;font-size:14px}
.tabla-caja{background:var(--vidrio);box-shadow:var(--sombra);border-radius:16px;overflow-x:auto}
.tabla{width:100%;border-collapse:collapse;font-size:15px}
.tabla th,.tabla td{text-align:left;padding:14px 18px;border-bottom:1px solid var(--borde);vertical-align:top}
.tabla tr:last-child td{border-bottom:0}
.tabla th{color:var(--suave);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.tabla td:first-child{font-weight:600;width:38%}
.cita{font-size:clamp(22px,3vw,30px);line-height:1.25;letter-spacing:-.025em;text-align:center;padding:26px 10px;margin:28px 0}
.cita b{color:var(--rosa);font-weight:400}
.dato{display:flex;gap:22px;align-items:center;background:var(--tinta);color:#fff;border-radius:20px;padding:26px 28px;margin:28px 0;box-shadow:var(--sombra-alta)}
.dato strong{font-size:52px;font-weight:500;letter-spacing:-.04em;line-height:1;background:linear-gradient(120deg,#fff,var(--lavanda) 50%,var(--rosa));-webkit-background-clip:text;background-clip:text;color:transparent}
.dato small{display:block;opacity:.6;margin-top:6px;font-size:13px}
.prompt{background:var(--tinta);border-radius:18px;box-shadow:var(--sombra-alta);overflow:hidden;margin:14px 0}
.prompt-barra{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.08);font-size:13px;color:rgba(255,255,255,.55)}
.prompt-barra .puntos{display:flex;gap:6px}.prompt-barra .puntos i{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.18)}
.prompt-barra .puntos i:first-child{background:var(--rosa)}
.copiar{border:0;background:#fff;color:var(--tinta);font:inherit;font-size:13px;font-weight:600;padding:7px 14px;border-radius:100px;cursor:pointer;transition:transform .2s}
.copiar:hover{transform:translateY(-1px)}
.prompt pre{white-space:pre-wrap;word-wrap:break-word;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;line-height:1.65;padding:20px 22px;color:#EDE9F6;min-height:3em}
.prompt pre .cursor{display:inline-block;width:.55em;background:var(--rosa);animation:parpadeo 1s steps(1) infinite}
@keyframes parpadeo{50%{opacity:0}}
.conv{display:grid;gap:14px}
.conv .caja{margin:0}
.conv h3{font-size:19px;margin:8px 0 10px}
.conv .no{color:#9a3b55;font-weight:500}.conv .si{color:#1f7a55;font-weight:500;margin-top:6px}
.criterio{position:relative;background:var(--vidrio);box-shadow:var(--sombra);border-radius:20px;padding:26px 28px 24px 30px;margin:36px 0;overflow:hidden}
.criterio::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(var(--rosa),var(--violeta))}
.criterio h2{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--rosa);margin-bottom:8px}
.criterio p{font-size:18px;line-height:1.55;letter-spacing:-.015em}
.firma{display:flex;align-items:center;gap:12px;margin-top:16px;font-size:14px;color:var(--suave)}
.firma img{width:40px;height:40px;border-radius:50%;object-fit:cover;box-shadow:var(--sombra)}
.pregunta{font-size:clamp(24px,3.4vw,34px);line-height:1.2;letter-spacing:-.03em;text-align:center;margin:48px auto 10px;max-width:640px}
.siguiente{text-align:center;padding:30px 24px 34px;margin:24px 0 56px;border-radius:24px;background:radial-gradient(80% 120% at 50% 0%,#F1E9FB,#fff 70%);box-shadow:var(--sombra)}
.siguiente p{color:var(--suave);font-weight:500;max-width:540px;margin:0 auto 18px}
.botones{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.relacionados h2{font-size:28px;font-weight:400;letter-spacing:-.03em;margin-bottom:18px}
.cierre{text-align:center;margin:30px auto 70px;max-width:760px;padding:40px 24px;border-radius:24px;background:var(--tinta);color:#fff;box-shadow:var(--sombra-alta)}
.cierre h2{font-weight:400;font-size:clamp(28px,4vw,40px);letter-spacing:-.035em;line-height:1.1}
.cierre p{opacity:.7;margin:12px auto 22px;max-width:520px}
.cierre .btn-claro{background:#fff}
.pie{padding:36px 0 26px;border-top:1px solid var(--borde);background:rgba(255,255,255,.7)}
.pie-inner{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
.pie-tag{color:var(--rosa);font-weight:500;margin:10px 0 2px}
.pie-links{display:flex;gap:18px;flex-wrap:wrap}.pie-links a{text-decoration:none;color:var(--suave);font-weight:500}.pie-links a:hover{color:var(--tinta)}
.pie-bajo{font-size:13px;margin-top:20px}
@media (max-width:720px){
 .nav-link:not(.activo){display:none}.nav-pill{padding:8px 8px 8px 16px;gap:6px}.nav-pill .btn-oscuro{font-size:14px;padding:10px 16px}.herramientas{padding:28px 18px 22px;border-radius:22px;margin-top:36px}
 .hero{padding-top:44px}.vitrina{height:300px;margin-top:20px}.m1,.m2,.m3,.m4{--x:0px;--ry:0deg;--rz:0deg}.mini{opacity:0;--e:.9;--y:24px;pointer-events:none}.mini.activa{pointer-events:auto}.vitrina{height:310px}.mini.activa{opacity:1;z-index:5;--x:0px;--ry:0deg;--rz:0deg}
 .grupo{grid-template-columns:1fr;gap:10px}
 .tabla td:first-child{width:45%}
 .dato{flex-direction:column;align-items:flex-start}
 .nube{width:340px}
}
@media (prefers-reduced-motion:reduce){.term .lin{width:100%!important}.check b{background:var(--rosa)!important;border-color:var(--rosa)!important}.check b::after{transform:rotate(-45deg) scale(1)!important}.puntaje span,.copiado{opacity:1!important;transform:none!important}.barra-progreso i{width:100%!important}.paso b{background:var(--tinta)!important;color:#fff!important}.fila i{transform:scaleX(var(--w,1))!important;opacity:1!important}*,*::before,*::after{animation:none!important;transition:none!important}.palabra,.revela{opacity:1;filter:none;transform:none}}
'''

JS = r'''// Biblioteca de recursos HEI01 · generado por recursos/_fuente/build.py
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
'''


def vitrina():
    t = lambda k: f'<span class="icono">{icono(k, 18)}</span>'
    return f"""<div class="vitrina" id="vitrina" aria-label="Así son los recursos: prompts, checklists, plantillas y ejercicios">
      <div class="mini m1" data-i="0"><div class="mini-top"><span class="tipo">Prompt</span>{t('prompt')}</div>
        <h4>Tu informe de IA para el directorio</h4>
        <div class="term"><span class="lin l1"><span class="gris">&gt;</span> Actúa como asesor del CEO.</span><span class="lin l2"><span class="gris">&gt;</span> Arma 1 página: gobernanza,</span><span class="lin l3"><span class="rosa">estrategia, personas.</span></span><span class="copiado">Copiado ✓</span></div>
        <span class="mini-pie">Listo para copiar · 20 min</span></div>
      <div class="mini m2" data-i="1"><div class="mini-top"><span class="tipo">Checklist</span>{t('checklist')}</div>
        <h4>10 preguntas para tu directorio</h4>
        <ul class="check"><li><b></b>¿Quién responde si sale mal?</li><li><b></b>¿Qué datos se pueden usar?</li><li><b></b>¿Qué 3 iniciativas van primero?</li></ul>
        <div class="puntaje">Tu puntaje <span>8/10 · a escalar</span></div>
        <span class="mini-pie">Sí, a medias o no · 15 min</span></div>
      <div class="mini m3" data-i="2"><div class="mini-top"><span class="tipo">Plantilla</span>{t('plantilla')}</div>
        <h4>Política de uso de IA en una página</h4>
        <div class="tab"><div class="fila">Para qué sí<i style="--w:.9"></i></div><div class="fila">Qué datos no<i style="--w:.7"></i></div><div class="fila">Quién revisa<i style="--w:.55"></i></div><div class="fila">A quién preguntar<i style="--w:.8"></i></div></div>
        <span class="mini-pie">Se completa en equipo · 30 min</span></div>
      <div class="mini m4" data-i="3"><div class="mini-top"><span class="tipo">Ejercicio</span>{t('ejercicio')}</div>
        <h4>El mapa de tareas de un rol</h4>
        <div class="tab"><div class="paso"><b>1</b>Lista sus 10 tareas</div><div class="paso"><b>2</b>Clasifícalas con la IA</div><div class="paso"><b>3</b>Elige una para probar</div></div>
        <div class="barra-progreso"><i></i></div>
        <span class="mini-pie">Paso a paso · 30 min</span></div>
    </div>
    <div class="leyenda" role="group" aria-label="Ver un tipo de recurso">
      <button type="button" data-i="0">Prompts</button><button type="button" data-i="1">Checklists</button><button type="button" data-i="2">Plantillas</button><button type="button" data-i="3">Ejercicios</button>
    </div>"""


def etiquetas(r):
    return ' · '.join(PARA[p] for p in r['para'])


def palabras(texto, retraso=0):
    """Envuelve cada palabra para la entrada escalonada con desenfoque, como el titular de la portada."""
    out = []
    for i, w in enumerate(texto.split(' ')):
        out.append(f'<span class="palabra" style="animation-delay:{retraso + i * 70}ms">{w}</span>')
    return ' '.join(out)


def bloque(b):
    t = b['tipo']
    tit = f'<h3>{e(b["titulo"])}</h3>' if b.get('titulo') else ''
    if t == 'lista_numerada':
        ini = b.get('inicio', 1) - 1
        return f'<div class="seccion revela">{tit}<ol class="numerada" style="--inicio:{ini}">' + ''.join(f'<li>{e(i)}</li>' for i in b['items']) + '</ol></div>'
    if t == 'pasos':
        return f'<div class="seccion revela"><h3>{e(b.get("titulo", "Paso a paso"))}</h3><ol class="pasos">' + ''.join(f'<li>{e(i)}</li>' for i in b['items']) + '</ol></div>'
    if t == 'cita':
        txt = e(b['texto'])
        if '. ' in txt:
            a, z = txt.split('. ', 1)
            txt = f'{a}. <b>{z}</b>'
        return f'<blockquote class="cita revela">{txt}</blockquote>'
    if t == 'texto':
        return f'<div class="seccion revela">{tit}<p>{e(b["texto"])}</p></div>'
    if t == 'tabla':
        enc = ''.join(f'<th>{e(c)}</th>' for c in b['encabezado']) if b.get('encabezado') else ''
        enc = f'<thead><tr>{enc}</tr></thead>' if enc else ''
        filas = ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in f) + '</tr>' for f in b['filas'])
        return f'<div class="seccion revela">{tit}<div class="tabla-caja"><table class="tabla">{enc}<tbody>{filas}</tbody></table></div></div>'
    if t == 'dato':
        return f'<div class="dato revela"><strong>{e(b["cifra"])}</strong><div>{e(b["texto"])}<small>Fuente: {e(b["fuente"])}</small></div></div>'
    if t == 'prompt':
        return ('<div class="seccion revela"><h3>El prompt</h3><div class="prompt"><div class="prompt-barra">'
                '<span class="puntos"><i></i><i></i><i></i></span><span>Cambia lo que está entre [corchetes]</span>'
                '<button class="copiar" type="button">Copiar prompt</button></div>'
                f'<pre>{e(b["texto"])}</pre></div></div>')
    if t == 'ejemplo':
        return f'<div class="caja revela">{tit}<p class="suave">{e(b["texto"])}</p></div>'
    if t == 'boton':
        return f'<p class="revela"><a class="btn-oscuro" href="{e(b["url"])}" target="_blank" rel="noopener">{e(b["texto"])} ↗</a></p>'
    if t == 'conversaciones':
        out = '<div class="seccion conv">'
        for n, c in enumerate(b['items'], 1):
            out += (f'<div class="caja revela"><span class="tipo">Conversación {n}</span><h3>{e(c["titulo"])}</h3>'
                    f'<p class="no">✕ En vez de: {e(c["no"])}</p><p class="si">✓ Prueba con: {e(c["si"])}</p></div>')
        return out + '</div>'
    raise ValueError('tipo de bloque desconocido: ' + t)


def tarjeta(r, revela=True):
    datos = f'data-para="{" ".join(r["para"])}" data-necesidad="{" ".join(r["necesidad"])}" data-tipo="{r["tipo"]}"'
    busqueda = ' '.join([r['titulo'], r['resumen'], r['para_que'], etiquetas(r), TIPO[r['tipo']], r['herramienta'], r.get('palabra', '')]).lower()
    return (f'<a class="tarjeta{" revela" if revela else ""}" href="{r["slug"]}.html" {datos} data-texto="{e(busqueda)}">'
            f'<span class="icono">{icono(r["tipo"], 26)}</span><span class="min">{r["minutos"]} min</span>'
            f'<span class="tipo">{e(TIPO[r["tipo"]])}</span>'
            f'<h3>{e(r["titulo"])}</h3><p>{e(r["resumen"])}</p>'
            f'<span class="para">{e(etiquetas(r))}</span></a>')


def pagina_recurso(r, todos):
    url = f'{DOMINIO}/recursos/{r["slug"]}.html'
    rel = [x for x in todos if x['slug'] != r['slug'] and set(x['para']) & set(r['para'])][:3]
    sig = r['siguiente']
    sig_url = AGENDA if sig['url'] == '../contact/' else sig['url']
    externo = ' target="_blank" rel="noopener"' if sig_url.startswith('http') else ''
    s = cabeza(f'{r["titulo"]} · Recursos HEI01', r['resumen'], url)
    s += f'''<main class="contenedor angosto articulo">
  <div class="migas"><a href="./">← Biblioteca de recursos</a></div>
  <span class="pildora"><span class="punto"></span>{e(TIPO[r["tipo"]])} · gratis</span>
  <h1>{palabras(e(r["titulo"]))}</h1>
  <p class="bajada revela">{e(r["resumen"])}</p>
  <div class="ficha revela">
    <div><span>Para</span>{e(etiquetas(r))}</div>
    <div><span>Tiempo</span>{r["minutos"]} minutos</div>
    <div><span>Herramienta</span>{e(r["herramienta"])}</div>
  </div>
  <div class="seccion revela"><h2>Para qué sirve</h2><p>{e(r["para_que"])}</p></div>
  <div class="seccion revela"><h2>Qué necesitas</h2><p>{e(r["necesitas"])}</p></div>
  {''.join(bloque(b) for b in r["bloques"])}
  <aside class="criterio revela"><h2>Mi criterio</h2><p>{e(r["criterio"])}</p>
    <div class="firma"><img src="../assets/portrait.png" alt="" width="40" height="40">Heileen Goodson · HEI01</div></aside>
  <p class="pregunta revela">{e(r["pregunta"])}</p>
  <div class="siguiente revela"><p>{e(sig["texto"])}</p>
    <div class="botones"><a class="btn-oscuro" href="{e(sig_url)}"{externo}>{e(sig["cta"])} →</a>
    <a class="btn-claro" href="https://linkedin.com/in/heileengoodson" target="_blank" rel="noopener">Cuéntame qué te salió</a></div>
  </div>
  <section class="relacionados"><h2 class="revela">Más para ti</h2><div class="grilla">{''.join(tarjeta(x) for x in rel)}</div>
  <p class="revela" style="text-align:center;margin-bottom:40px"><a class="btn-claro" href="./">Ver toda la biblioteca</a></p></section>
</main>
{PIE}
</body></html>
'''
    return s


def grupo(clave, titulo, dic):
    return (f'<div class="grupo" data-grupo="{clave}"><span class="grupo-titulo">{titulo}</span><div class="chips">'
            + ''.join(f'<button class="chip" type="button" data-valor="{k}" aria-pressed="false">{e(v)}</button>' for k, v in dic.items())
            + '</div></div>')


def pagina_indice(todos):
    url = f'{DOMINIO}/recursos/'
    titulo = 'Biblioteca de recursos de IA para líderes · HEI01'
    desc = 'Prompts, plantillas, checklists y ejercicios de IA para directorios, líderes de transformación y de personas. Gratis, sin registro, listos para usar.'
    tipos = {k: v for k, v in TIPO.items() if any(r['tipo'] == k for r in todos)}
    s = cabeza(titulo, desc, url)
    s += f'''<main class="contenedor">
  <section class="hero">
    <span class="pildora"><span class="punto"></span>Biblioteca de recursos</span>
    <h1>{palabras('Recursos de IA con')} <span class="rosa">{palabras('criterio ejecutivo.', 280)}</span></h1>
    <p class="revela" data-retraso="500">Sin caos, sin hype, con orden y método. Prompts, plantillas y ejercicios para gobernar, priorizar y llevar la IA a las personas.</p>
    <p class="hero-nota revela" data-retraso="650">Gratis, sin registro y listos para usar de inmediato.</p>
    {vitrina()}
  </section>
  <div class="herramientas revela" id="buscar">
    <div class="panel-cabeza">
      <span class="pildora"><span class="punto"></span>Encuentra tu recurso</span>
      <h2>¿Qué necesitas hoy?</h2>
      <p>Escribe un tema o selecciona uno o varios criterios. Los recursos se filtran al instante.</p>
    </div>
    <div class="buscador">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Busca: directorio, priorizar, equipos, prompt…" aria-label="Buscar recursos" autocomplete="off">
    </div>
    <div class="filtros">
      {grupo('para', 'Para quién', PARA)}
      {grupo('necesidad', 'Qué necesitas', NECESIDAD)}
      {grupo('tipo', 'Tipo', tipos)}
    </div>
  </div>
  <div class="estado"><span id="cuenta" aria-live="polite"></span><button class="limpiar" id="limpiar" type="button" hidden>Limpiar filtros</button></div>
  <div class="grilla" id="grilla">{''.join(tarjeta(r) for r in todos)}</div>
  <div class="vacio" id="vacio"><p>No encontré recursos con esos filtros.</p><p class="suave">Prueba con menos filtros o <a href="../contact/">cuéntame qué necesitas</a>.</p></div>
  <section class="cierre revela">
    <h2>¿Quieres que tu equipo lo haga con método?</h2>
    <p>Formaciones diseñadas con los procesos reales de tu organización, y acompañamiento para gobernar, priorizar y llevar la IA a las personas.</p>
    <div class="botones"><a class="btn-claro" href="../formaciones.html">Ver formaciones</a><a class="btn-claro" href="{AGENDA}" target="_blank" rel="noopener">Agendar sesión ejecutiva →</a></div>
  </section>
</main>
{PIE}
</body></html>
'''
    return s


def sitemap(todos):
    p = os.path.join(RAIZ, 'sitemap.xml')
    s = leer(p)
    s = re.sub(r'\s*<url>\s*<loc>https://hei01\.com/recursos/[^<]*</loc>.*?</url>', '', s, flags=re.S)
    urls = [f'{DOMINIO}/recursos/'] + [f'{DOMINIO}/recursos/{r["slug"]}.html' for r in todos]
    add = ''.join(f'\n  <url>\n    <loc>{u}</loc>\n    <lastmod>{HOY}</lastmod>\n    <priority>{"0.8" if u.endswith("/") else "0.6"}</priority>\n  </url>' for u in urls)
    s = s.replace('</urlset>', add.lstrip('\n') + '\n</urlset>')
    escribir(p, s)


def main():
    todos = json.loads(leer(os.path.join(DIR, '_fuente', 'recursos.json')))
    slugs = [r['slug'] for r in todos]
    assert len(slugs) == len(set(slugs)), 'slugs repetidos'
    for r in todos:
        for v in r['para']:
            assert v in PARA, (r['slug'], v)
        for v in r['necesidad']:
            assert v in NECESIDAD, (r['slug'], v)
        assert r['tipo'] in TIPO, r['slug']
        crudo = json.dumps(r, ensure_ascii=False)
        assert '{{' not in crudo and '{%' not in crudo, 'Jekyll interpretaría {{ o {%'
    for viejo in ('sitio.css',):
        if os.path.exists(os.path.join(DIR, viejo)):
            os.remove(os.path.join(DIR, viejo))
    escribir(os.path.join(DIR, 'recursos.css'), CSS)
    escribir(os.path.join(DIR, 'recursos.js'), JS)
    escribir(os.path.join(DIR, 'index.html'), pagina_indice(todos))
    for r in todos:
        escribir(os.path.join(DIR, r['slug'] + '.html'), pagina_recurso(r, todos))
    sitemap(todos)
    print(f'{len(todos)} recursos · index.html · recursos.css · recursos.js · sitemap actualizado')


if __name__ == '__main__':
    main()
