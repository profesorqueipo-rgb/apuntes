#!/usr/bin/env python3
"""Reconstruye la web de GitHub Pages con todos los apuntes.

Uso:  python3 construir_web.py
Copia los HTML y PDF de cada asignatura (Apuntes/<nivel>/...) a esta carpeta
con nombres limpios, les añade la cabecera HTML que necesita un navegador y un
enlace de vuelta a la portada, y genera index.html (la portada).
Vuelve a ejecutarlo cada vez que añadas o cambies apuntes.
"""
import html
import re
import shutil
from pathlib import Path

WEB = Path(__file__).resolve().parent
SRC = WEB.parent  # carpeta Apuntes

CURSO = "2026-27"

ASIGNATURAS = [
    {
        "id": "eso4",
        "corto": "Mat. B · 4º ESO",
        "carpeta": "4eso-matematicas-b",
        "origen": "4º ESO Matemáticas B",
        "nivel": "4º ESO",
        "nombre": "Matemáticas B",
        "color": "violet",
        "completo": {
            "html": "Apuntes/apuntes-4eso-matB-curso-completo.html",
            "pdf_sin": "Apuntes/Apuntes 4ESO MatB - curso completo (sin soluciones).pdf",
            "pdf_con": "Apuntes/Apuntes 4ESO MatB - curso completo (con soluciones).pdf",
        },
        "partes": [
            {"titulo": "1ª evaluación", "slug": "1eval", "html": "Apuntes/apuntes-4eso-matB-1eval.html",
             "temas": [("t11", "La realidad en números"), ("t31", "Un lenguaje universal"),
                       ("t32", "La igualdad es la clave"), ("t33", "No me da igual")]},
            {"titulo": "2ª evaluación", "slug": "2eval", "html": "Apuntes/apuntes-4eso-matB-2eval.html",
             "temas": [("t21a", "Semejanza"), ("t21b", "Trigonometría"),
                       ("t21c", "Resolución de triángulos"), ("t22", "Orientando el plano")]},
            {"titulo": "3ª evaluación", "slug": "3eval", "html": "Apuntes/apuntes-4eso-matB-3eval.html",
             "temas": [("t34a", "Características de las funciones"), ("t34b", "Funciones elementales"),
                       ("t41", "Correlaciones"), ("t42", "Las leyes del azar")]},
        ],
        "extras": [
            {"titulo": "Colección de ejercicios por tema", "slug": "coleccion",
             "html": "Colección de ejercicios/coleccion-ejercicios-4eso-matB.html",
             "pdf_sin": "Colección de ejercicios/Colección ejercicios 4ESO MatB (sin soluciones).pdf",
             "pdf_con": "Colección de ejercicios/Colección ejercicios 4ESO MatB (con soluciones).pdf"},
            {"titulo": "Cuadernillo UP1", "slug": "cuadernillo-up1",
             "html": "Cuadernillos/cuadernillo-UP1-4eso-matB.html",
             "pdf_sin": "Cuadernillos/Cuadernillo UP1 4ESO MatB (sin soluciones).pdf",
             "pdf_con": "Cuadernillos/Cuadernillo UP1 4ESO MatB (con soluciones).pdf"},
        ],
    },
    {
        "id": "mat2",
        "corto": "Mat. II · 2º Bach",
        "carpeta": "2bach-matematicas-ii",
        "origen": "2º Bachillerato Matemáticas II",
        "nivel": "2º Bachillerato",
        "nombre": "Matemáticas II",
        "color": "red",
        "completo": {
            "html": "Apuntes/apuntes-2bach-matII-curso-completo.html",
            "pdf_sin": "Apuntes/Apuntes 2Bach Mat II - curso completo (sin soluciones).pdf",
            "pdf_con": "Apuntes/Apuntes 2Bach Mat II - curso completo (con soluciones).pdf",
        },
        "partes": [
            {"titulo": "UP1 · Números y álgebra", "slug": "up1", "html": "Apuntes/apuntes-2bach-matII-up1.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach Mat II - UP1 Números y álgebra (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach Mat II - UP1 Números y álgebra (con soluciones).pdf",
             "temas": [("t1", "Matrices"), ("t2", "Determinantes"), ("t3", "Sistemas de ecuaciones lineales")]},
            {"titulo": "UP2 · Geometría", "slug": "up2", "html": "Apuntes/apuntes-2bach-matII-up2.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach Mat II - UP2 Geometría (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach Mat II - UP2 Geometría (con soluciones).pdf",
             "temas": [("t4", "Vectores en el espacio"), ("t5", "Rectas y planos en el espacio"),
                       ("t6", "Ángulos, distancias, proyecciones y simétricos")]},
            {"titulo": "UP3 · Estadística y probabilidad", "slug": "up3", "html": "Apuntes/apuntes-2bach-matII-up3.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach Mat II - UP3 Estadística y probabilidad (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach Mat II - UP3 Estadística y probabilidad (con soluciones).pdf",
             "temas": [("t7", "Probabilidad"), ("t8", "Distribuciones binomial y normal")]},
            {"titulo": "UP4 · Análisis", "slug": "up4", "html": "Apuntes/apuntes-2bach-matII-up4.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach Mat II - UP4 Análisis (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach Mat II - UP4 Análisis (con soluciones).pdf",
             "temas": [("t9", "Límites y continuidad"), ("t10", "Derivadas"), ("t11", "Aplicaciones de las derivadas"),
                       ("t12", "Integrales indefinidas"), ("t13", "Integral definida y áreas")]},
        ],
        "extras": [],
    },
    {
        "id": "ccss2",
        "corto": "CCSS II · 2º Bach",
        "carpeta": "2bach-matematicas-ccss-ii",
        "origen": "2º Bachillerato Matemáticas CCSS II",
        "nivel": "2º Bachillerato",
        "nombre": "Matemáticas Aplicadas a las CCSS II",
        "color": "green",
        "completo": {
            "html": "Apuntes/apuntes-2bach-ccssII-curso-completo.html",
            "pdf_sin": "Apuntes/Apuntes 2Bach CCSS II - curso completo (sin soluciones).pdf",
            "pdf_con": "Apuntes/Apuntes 2Bach CCSS II - curso completo (con soluciones).pdf",
        },
        "partes": [
            {"titulo": "1ª evaluación", "slug": "1eval", "html": "Apuntes/apuntes-2bach-ccssII-1eval.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach CCSS II - 1ª evaluación (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach CCSS II - 1ª evaluación (con soluciones).pdf",
             "temas": [("t1", "Matrices"), ("t2", "Determinantes"), ("t3", "Sistemas de ecuaciones lineales"),
                       ("t4", "Programación lineal")]},
            {"titulo": "2ª evaluación", "slug": "2eval", "html": "Apuntes/apuntes-2bach-ccssII-2eval.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach CCSS II - 2ª evaluación (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach CCSS II - 2ª evaluación (con soluciones).pdf",
             "temas": [("t5", "Probabilidad"), ("t6", "Distribuciones binomial y normal"),
                       ("t7", "Inferencia estadística")]},
            {"titulo": "3ª evaluación", "slug": "3eval", "html": "Apuntes/apuntes-2bach-ccssII-3eval.html",
             "pdf_sin": "Apuntes/Apuntes 2Bach CCSS II - 3ª evaluación (sin soluciones).pdf",
             "pdf_con": "Apuntes/Apuntes 2Bach CCSS II - 3ª evaluación (con soluciones).pdf",
             "temas": [("t8", "Límites y continuidad"), ("t9", "Derivadas y aplicaciones"), ("t10", "Integrales")]},
        ],
        "extras": [],
    },
]

VOLVER_CSS = (
    "<style>.volver-portada{font-family:var(--f-head,cursive);font-weight:700;font-size:16px;"
    "text-decoration:none;color:var(--pencil,#5a5f68);padding:4px 10px 2px;white-space:nowrap}"
    ".volver-portada:hover{text-decoration:underline}"
    ".volver-suelto{display:block;max-width:900px;margin:12px auto 0}</style>"
)
VOLVER_A = '<a class="volver-portada" href="../">↩ todos los apuntes</a>'


def preparar_pagina(origen: Path, destino: Path):
    """Copia una página de apuntes añadiéndole cabecera HTML y enlace a la portada."""
    s = origen.read_text(encoding="utf-8")
    if '<nav class="tabs"' in s:
        s = re.sub(r'(<nav class="tabs".*?)(</nav>)', lambda m: m.group(1) + VOLVER_A + "\n" + m.group(2),
                   s, count=1, flags=re.S)
        extra_top = ""
    else:
        extra_top = VOLVER_A.replace('class="volver-portada"', 'class="volver-portada volver-suelto"')
    if s.lstrip().lower().startswith("<!doctype"):
        s = s.replace("<body>", "<body>\n" + VOLVER_CSS + extra_top, 1)
    else:
        s = ("<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
             "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
             "</head>\n<body>\n" + VOLVER_CSS + extra_top + "\n" + s + "\n</body>\n</html>\n")
    destino.write_text(s, encoding="utf-8")


def copiar_pdf(origen: Path, destino: Path):
    if not origen.exists():
        raise FileNotFoundError(origen)
    shutil.copy2(origen, destino)


def e(t):
    return html.escape(t, quote=True)


def construir():
    fuentes = None
    tarjetas, pestanas = [], []
    for a in ASIGNATURAS:
        base = SRC / a["origen"]
        dest = WEB / a["carpeta"]
        if dest.exists():
            shutil.rmtree(dest)
        (dest / "pdf").mkdir(parents=True)
        c = a["carpeta"]

        # curso completo
        preparar_pagina(base / a["completo"]["html"], dest / "curso-completo.html")
        copiar_pdf(base / a["completo"]["pdf_sin"], dest / "pdf" / "curso-completo.pdf")
        copiar_pdf(base / a["completo"]["pdf_con"], dest / "pdf" / "curso-completo-soluciones.pdf")
        if fuentes is None:
            txt = (base / a["completo"]["html"]).read_text(encoding="utf-8")
            fuentes = re.search(r'<style id="fuentes-incrustadas".*?</style>', txt, re.S).group(0)

        filas = []
        for p in a["partes"]:
            preparar_pagina(base / p["html"], dest / f'{p["slug"]}.html')
            pdfs = ""
            if "pdf_sin" in p:
                copiar_pdf(base / p["pdf_sin"], dest / "pdf" / f'{p["slug"]}.pdf')
                copiar_pdf(base / p["pdf_con"], dest / "pdf" / f'{p["slug"]}-soluciones.pdf')
                pdfs = (f'<a class="chip pdf" href="{c}/pdf/{p["slug"]}.pdf">PDF</a>'
                        f'<a class="chip pdf sol" href="{c}/pdf/{p["slug"]}-soluciones.pdf">PDF con soluciones</a>')
            temas = "".join(
                f'<li><a href="{c}/curso-completo.html#{tid}" data-buscar="{e(t.lower())}">{e(t)}</a></li>'
                for tid, t in p["temas"])
            filas.append(
                f'<div class="parte"><div class="parte-cab"><a class="parte-tit" href="{c}/{p["slug"]}.html">{e(p["titulo"])}</a>'
                f'<span class="chips"><a class="chip" href="{c}/{p["slug"]}.html">web</a>{pdfs}</span></div>'
                f'<ul class="temas">{temas}</ul></div>')

        extras = []
        for x in a["extras"]:
            preparar_pagina(base / x["html"], dest / f'{x["slug"]}.html')
            copiar_pdf(base / x["pdf_sin"], dest / "pdf" / f'{x["slug"]}.pdf')
            copiar_pdf(base / x["pdf_con"], dest / "pdf" / f'{x["slug"]}-soluciones.pdf')
            extras.append(
                f'<li><a class="extra-tit" href="{c}/{x["slug"]}.html">{e(x["titulo"])}</a>'
                f'<span class="chips"><a class="chip" href="{c}/{x["slug"]}.html">web</a>'
                f'<a class="chip pdf" href="{c}/pdf/{x["slug"]}.pdf">PDF</a>'
                f'<a class="chip pdf sol" href="{c}/pdf/{x["slug"]}-soluciones.pdf">PDF con soluciones</a></span></li>')
        extras_html = (f'<h3 class="r">Ejercicios para practicar</h3><ul class="extras">{"".join(extras)}</ul>'
                       if extras else "")

        n_temas = sum(len(p["temas"]) for p in a["partes"])
        pestanas.append(f'<a href="#{a["id"]}" class="c-{a["color"]}">{e(a["corto"])}</a>')
        tarjetas.append(f'''
<section class="sheet asignatura c-{a["color"]}" id="{a["id"]}">
  <span class="kicker">{e(a["nivel"])} · {n_temas} temas</span>
  <h2>{e(a["nombre"])}</h2>
  <div class="completo">
    <a class="boton" href="{c}/curso-completo.html">Abrir el curso completo</a>
    <span class="chips"><a class="chip pdf" href="{c}/pdf/curso-completo.pdf">PDF para imprimir</a><a class="chip pdf sol" href="{c}/pdf/curso-completo-soluciones.pdf">PDF con soluciones</a></span>
  </div>
  <div class="partes">{"".join(filas)}</div>
  {extras_html}
</section>''')

    pagina = PORTADA.format(
        fuentes=fuentes, curso=CURSO, pestanas="\n  ".join(pestanas), tarjetas="\n".join(tarjetas))
    (WEB / "index.html").write_text(pagina, encoding="utf-8")
    (WEB / ".nojekyll").write_text("", encoding="utf-8")
    print("Web generada en", WEB)


PORTADA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Apuntes de Matemáticas</title>
<meta name="description" content="Apuntes de Matemáticas B (4º ESO), Matemáticas II y Matemáticas Aplicadas a las CCSS II (2º Bachillerato): teoría, ejemplos y ejercicios resueltos.">
{fuentes}
<style>
@font-face{{font-family:"BarFix";src:local("Arial"),local("Helvetica"),local("Roboto"),local("DejaVu Sans");unicode-range:U+007C}}
:root{{
  --desk:#e6ebef; --paper:#fbfcf8; --grid:#d5e4ee; --grid2:#bfd3e1; --margin:#ef9a9a;
  --ink:#24429c; --red:#cf3535; --green:#1d8655; --violet:#7a46b8; --pencil:#5a5f68;
  --hl:#fff07a; --postit:#fff4a3; --shadow:rgba(30,40,60,.16);
  --f-body:"BarFix","Patrick Hand","Comic Sans MS","Segoe Print",cursive;
  --f-head:"Kalam","Patrick Hand","Comic Sans MS",cursive;
  --f-note:"Caveat","Kalam","Comic Sans MS",cursive;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
  --desk:#10141c; --paper:#1b2130; --grid:#262f42; --grid2:#303c54; --margin:#7c3a46;
  --ink:#9fc2ff; --red:#ff8d88; --green:#79dba6; --violet:#c9a7ff; --pencil:#aeb6c4;
  --hl:rgba(255,226,70,.30); --postit:#4a4424; --shadow:rgba(0,0,0,.5); color-scheme:dark }}}}
:root[data-theme="dark"]{{
  --desk:#10141c; --paper:#1b2130; --grid:#262f42; --grid2:#303c54; --margin:#7c3a46;
  --ink:#9fc2ff; --red:#ff8d88; --green:#79dba6; --violet:#c9a7ff; --pencil:#aeb6c4;
  --hl:rgba(255,226,70,.30); --postit:#4a4424; --shadow:rgba(0,0,0,.5); color-scheme:dark }}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion: reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--desk);color:var(--ink);font-family:var(--f-body);font-size:20px;line-height:1.5;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 48px}}
a{{color:inherit}}
a:focus-visible,input:focus-visible{{outline:3px dashed var(--red);outline-offset:3px}}
.c-violet{{--acc:var(--violet)}} .c-red{{--acc:var(--red)}} .c-green{{--acc:var(--green)}}

.tabs{{position:sticky;top:0;z-index:5;background:var(--desk);display:flex;gap:6px;flex-wrap:wrap;justify-content:center;padding-block:10px 8px;max-width:940px;margin:0 auto}}
.tabs a{{font-family:var(--f-head);font-weight:700;font-size:16px;text-decoration:none;color:var(--acc,var(--ink));background:var(--paper);
  padding:4px 12px 2px;border:2px solid currentColor;border-radius:14px 4px 12px 5px/5px 12px 4px 14px;white-space:nowrap}}

.sheet{{position:relative;max-width:900px;margin:22px auto 0;background-color:var(--paper);
  background-image:linear-gradient(var(--grid2) 1px,transparent 1px),linear-gradient(90deg,var(--grid2) 1px,transparent 1px),
   linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:100px 100px,100px 100px,20px 20px,20px 20px;
  box-shadow:0 1px 0 var(--grid2),0 8px 22px var(--shadow);border-radius:3px;padding:34px 34px 40px 74px;scroll-margin-top:60px}}
.sheet::before{{content:"";position:absolute;left:52px;top:0;bottom:0;width:2px;background:var(--margin);opacity:.8}}
.sheet::after{{content:"";position:absolute;left:14px;top:16px;bottom:16px;width:16px;
  background:radial-gradient(circle at 8px 10px,var(--desk) 5px,transparent 6px) 0 0/16px 40px repeat-y}}
@media (max-width:620px){{.sheet{{padding:26px 16px 30px 40px}}.sheet::before{{left:30px}}.sheet::after{{left:6px;width:14px;background-size:14px 34px}}body{{font-size:18px}}}}

h1,h2,h3{{font-family:var(--f-head);font-weight:700;line-height:1.15;margin:0;text-wrap:balance}}
h1{{font-size:clamp(34px,6vw,54px);color:var(--violet)}}
h2{{font-size:clamp(26px,4.4vw,36px);text-transform:uppercase;letter-spacing:1.5px;color:var(--acc);margin-top:4px}}
h3{{font-size:21px;text-transform:uppercase;letter-spacing:1px;margin:26px 0 8px;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}}
h3.r{{color:var(--red)}}
.kicker{{font-family:var(--f-note);font-size:24px;color:var(--pencil);display:block}}
.date{{position:absolute;right:26px;top:12px;font-family:var(--f-note);font-size:21px;color:var(--pencil)}}
.hl{{background:linear-gradient(transparent 45%,var(--hl) 45%,var(--hl) 92%,transparent 92%);padding:0 3px}}
p{{margin:8px 0;max-width:68ch}}

.buscador{{margin:18px 0 4px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.buscador label{{font-family:var(--f-note);font-size:23px;color:var(--red)}}
.buscador input{{font:inherit;color:var(--ink);background:transparent;border:none;border-bottom:2px solid var(--ink);padding:2px 4px;min-width:0;flex:1 1 220px;max-width:420px}}
.sin-resultados{{font-family:var(--f-note);font-size:22px;color:var(--pencil);max-width:900px;margin:18px auto 0;text-align:center}}

.indice{{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}}
.indice a{{display:block;text-decoration:none;color:var(--acc);border:2.2px solid currentColor;padding:8px 14px;
  border-radius:255px 14px 225px 14px/14px 225px 14px 255px;font-family:var(--f-head);font-weight:700;line-height:1.2}}
.indice a small{{display:block;font-family:var(--f-note);font-weight:500;font-size:20px;color:var(--pencil)}}
.indice a:hover{{background:color-mix(in srgb,var(--acc) 8%,transparent)}}

.completo{{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;margin:14px 0 6px}}
.boton{{font-family:var(--f-head);font-weight:700;font-size:19px;text-decoration:none;background:var(--postit);color:var(--ink);
  padding:6px 16px 4px;transform:rotate(-1.2deg);box-shadow:1px 3px 0 var(--shadow);display:inline-block}}
.boton:hover{{transform:rotate(0)}}
.chips{{display:inline-flex;flex-wrap:wrap;gap:6px}}
.chip{{font-family:var(--f-head);font-weight:700;font-size:15px;text-decoration:none;color:var(--ink);
  border:1.8px solid currentColor;padding:1px 10px 0;border-radius:12px 4px 10px 5px/5px 10px 4px 12px;white-space:nowrap;background:var(--paper)}}
.chip.pdf{{color:var(--pencil)}} .chip.sol{{color:var(--green)}}
.chip:hover,.parte-tit:hover,.temas a:hover,.extra-tit:hover{{text-decoration:underline}}

.partes{{display:grid;gap:4px;margin-top:10px}}
.parte{{padding:10px 0 4px;border-top:1.5px dashed var(--grid2)}}
.parte-cab{{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline}}
.parte-tit{{font-family:var(--f-head);font-weight:700;font-size:21px;text-decoration:none;color:var(--acc)}}
.temas{{list-style:none;margin:4px 0 0;padding:0}}
.temas li{{padding-left:26px;position:relative;margin:2px 0}}
.temas li::before{{content:"→";position:absolute;left:0;color:var(--red)}}
.temas a{{text-decoration:none}}
.temas li.oculto,.parte.oculto,.asignatura.oculto,.extras li.oculto{{display:none}}
.temas a mark{{background:var(--hl);color:inherit;padding:0 2px}}
.extras{{list-style:none;padding:0;margin:6px 0 0;display:grid;gap:8px}}
.extras li{{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline}}
.extra-tit{{font-family:var(--f-head);font-weight:700;font-size:19px;text-decoration:none}}
.pie{{max-width:900px;margin:26px auto 0;text-align:center;font-family:var(--f-note);font-size:21px;color:var(--pencil)}}
@media print{{.tabs,.buscador{{display:none}}body{{background:#fff}}.sheet{{box-shadow:none;break-inside:avoid}}}}
</style>
</head>
<body>
<nav class="tabs" aria-label="Asignaturas">
  <a href="#inicio">Inicio</a>
  {pestanas}
</nav>

<header class="sheet" id="inicio">
  <span class="date">curso {curso}</span>
  <span class="kicker">mi libreta de clase</span>
  <h1>Apuntes de Matemáticas</h1>
  <p>Teoría, ejemplos y ejercicios resueltos, <span class="hl">ordenados como los vemos en clase</span>. Cada tema se puede leer en la web (las soluciones se despliegan al pulsar) o descargar en PDF para imprimir, con o sin soluciones.</p>
  <ul class="indice">
    <li class="c-violet"><a href="#eso4">Matemáticas B<small>4º ESO</small></a></li>
    <li class="c-red"><a href="#mat2">Matemáticas II<small>2º Bachillerato</small></a></li>
    <li class="c-green"><a href="#ccss2">Matemáticas Aplicadas a las CCSS II<small>2º Bachillerato</small></a></li>
  </ul>
  <div class="buscador">
    <label for="buscar">¿Buscas un tema?</label>
    <input id="buscar" type="search" placeholder="derivadas, matrices, trigonometría…" autocomplete="off">
  </div>
</header>
{tarjetas}
<p class="sin-resultados" id="sinRes" hidden>No encuentro ningún tema con ese nombre.</p>
<p class="pie">Si encuentras una errata, avísame en clase ✎</p>

<script>
(function(){{
  var input=document.getElementById('buscar'), sinRes=document.getElementById('sinRes');
  function norm(t){{return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
  input.addEventListener('input',function(){{
    var q=norm(input.value.trim()), total=0;
    document.querySelectorAll('.asignatura').forEach(function(sec){{
      var visibles=0;
      sec.querySelectorAll('.parte').forEach(function(p){{
        var n=0;
        p.querySelectorAll('.temas li').forEach(function(li){{
          var ok=!q||norm(li.textContent).indexOf(q)>-1; li.classList.toggle('oculto',!ok); if(ok)n++;
        }});
        var titOk=q&&norm(p.querySelector('.parte-tit').textContent).indexOf(q)>-1;
        if(titOk){{p.querySelectorAll('.temas li').forEach(function(li){{li.classList.remove('oculto');}});n=1;}}
        p.classList.toggle('oculto',!!q&&n===0); visibles+=n;
      }});
      sec.querySelectorAll('.extras li').forEach(function(li){{
        var ok=!q||norm(li.textContent).indexOf(q)>-1; li.classList.toggle('oculto',!ok); if(ok&&q)visibles++;
      }});
      if(q&&norm(sec.querySelector('h2').textContent).indexOf(q)>-1){{
        sec.querySelectorAll('.oculto').forEach(function(el){{el.classList.remove('oculto');}}); visibles=1;
      }}
      sec.classList.toggle('oculto',!!q&&visibles===0); total+=visibles;
    }});
    sinRes.hidden=!q||total>0;
  }});
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    construir()
