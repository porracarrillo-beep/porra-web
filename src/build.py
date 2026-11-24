"""Arma public/index.html a partir de la plantilla, los casos y los textos de content/.

Uso (desde la carpeta raíz del proyecto):  python3 src/build.py
Cloudflare Pages lo corre solo en cada actualización del repositorio.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

# Si un archivo de textos quedó mal escrito, avisar en castellano y no publicar
for _name in ('home.json', 'casos-ia.json'):
    try:
        with open(os.path.join(ROOT, 'content', _name), encoding='utf-8') as _f:
            json.load(_f)
    except json.JSONDecodeError as e:
        print(f'ERROR en content/{_name}, línea {e.lineno}, columna {e.colno}: falta o sobra una coma o unas comillas cerca de ahí.')
        sys.exit(1)

from cases import CASES, fragment, BEH, beh_fragment  # noqa: E402
import paginas  # noqa: E402
import shutil  # noqa: E402

def load(name):
    with open(os.path.join(ROOT, 'content', name), encoding='utf-8') as f:
        return json.load(f)

home = load('home.json')
ORDER = home['orden_de_casos']
TITLES = home['titulos_de_casos']

# Claves en castellano (content/home.json) -> claves que usa el código de la página
WK = {'titulo': 'title', 'bajada': 'sub', 'categoria': 'cat', 'descripcion': 'desc', 'filtro': 'f', 'proporcion': 'r',
      'imagen': 'img', 'video': 'video', 'video_completo': 'full', 'caso': 'caso', 'posicion': 'pos', 'tipo': 'kind',
      'color': 'color', 'link': 'href', 'reel': 'reel', 'pais': 'pais'}
RK = {'video': 'src', 'titulo': 'title', 'descripcion': 'desc', 'tipo': 'kind'}
WORKS = [{WK[k]: v for k, v in w.items()} for w in home['tarjetas_home']]
REELS = [{RK[k]: v for k, v in r.items()} for r in home['reels']]

# Chequeos para que un error de tipeo no rompa la web en silencio
errors = []
for c in ORDER:
    if c not in CASES and c not in BEH:
        errors.append(f'orden_de_casos: "{c}" no existe como caso')
    if c not in TITLES:
        errors.append(f'titulos_de_casos: falta el título de "{c}"')
for w in WORKS:
    if w.get('caso') and w['caso'] not in ORDER:
        errors.append(f'tarjeta "{w.get("title")}": el caso "{w["caso"]}" no está en orden_de_casos')
    for key in ('img', 'video', 'full'):
        if w.get(key) and not os.path.exists(os.path.join(ROOT, 'public', w[key].split('?')[0])):
            errors.append(f'tarjeta "{w.get("title")}": no encuentro el archivo {w[key]}')
if errors:
    print('ERRORES:\n - ' + '\n - '.join(errors))
    sys.exit(1)

SITE = home.get('dominio', '').rstrip('/')
CARDS = {t['caso']: t for t in home['tarjetas_home'] if t.get('caso')}

# Fragmento de cada caso (placas), con texto alternativo en las imágenes
FRAG, INFO = {}, {}
for c in ORDER:
    raw = beh_fragment(c) if c in BEH else fragment(c)
    INFO[c] = paginas.info_caso(c, raw, TITLES, CARDS)
    FRAG[c] = paginas.alts(raw, f"{INFO[c]['titulo']} · {INFO[c]['bajada']}".strip(' ·'))

templates = '\n'.join(f'<template id="tpl-{c}">{FRAG[c]}</template>' for c in ORDER)

# Tarjetas del home: miniatura liviana con medidas
for w in WORKS:
    if w.get('img'):
        t = paginas.card_thumb(w['img'])
        if t:
            w['thumb'] = t
            d = paginas.DIMS.get(t)
            if d: w['w'], w['h'] = d
        w['alt'] = f"{paginas.plano(w['title'])} · {paginas.plano(w.get('sub', ''))}".strip(' ·')

with open(os.path.join(ROOT, 'src', 'plantilla.html'), encoding='utf-8') as f:
    html = f.read()
with open(os.path.join(ROOT, 'src', 'plates.css'), encoding='utf-8') as f:
    css = f.read()
for k, v in {'%%TEMPLATES%%': templates, '%%WORKS%%': json.dumps(WORKS, ensure_ascii=False),
             '%%REELS%%': json.dumps(REELS, ensure_ascii=False), '%%ORDER%%': json.dumps(ORDER),
             '%%TITLES%%': json.dumps(TITLES, ensure_ascii=False), '%%PLATES_CSS%%': css,
             '%%SITE_URL%%': SITE, '%%SCHEMA%%': paginas.schema_home(SITE),
             '%%CASE_LINKS%%': ''.join(f'<li><a href="/trabajos/{c}">{INFO[c]["titulo"]}</a></li>' for c in ORDER)}.items():
    html = html.replace(k, v)
html = paginas.medidas(paginas.webp(html))

with open(os.path.join(ROOT, 'public', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print('ok · public/index.html', len(html), 'caracteres ·', len(ORDER), 'casos ·', len(WORKS), 'tarjetas')

# Una página indexable por caso: /trabajos/<caso>
out = os.path.join(ROOT, 'public', 'trabajos')
shutil.rmtree(out, ignore_errors=True)
os.makedirs(out)
for i, c in enumerate(ORDER):
    frag = FRAG[c]
    if c == 'lollapalooza':  # el video 360 va después de la sexta placa, igual que en la ventana del home
        cut = 0
        for _ in range(6):
            cut = frag.find('</section>', cut) + len('</section>')
        frag = frag[:cut] + '<video class="vmod" src="assets/lolla/360.mp4" muted loop playsinline autoplay controls preload="metadata"></video>' + frag[cut:]
    page = paginas.pagina_caso(INFO[c], frag, INFO[ORDER[i - 1]], INFO[ORDER[(i + 1) % len(ORDER)]], SITE, css)
    with open(os.path.join(out, f'{c}.html'), 'w', encoding='utf-8') as f:
        f.write(page)
print('ok · public/trabajos/', len(ORDER), 'páginas de caso')

with open(os.path.join(ROOT, 'public', 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(paginas.sitemap(SITE, ORDER))
with open(os.path.join(ROOT, 'public', 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write(paginas.llms(SITE, [INFO[c] for c in ORDER]))
print('ok · sitemap.xml y llms.txt')
