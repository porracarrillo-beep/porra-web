"""Crea versiones .webp livianas de las imágenes de public/assets.

Uso (desde la carpeta raíz):  python3 src/optimizar_imagenes.py      (solo las nuevas o cambiadas)
                              python3 src/optimizar_imagenes.py --todo  (rehace todas)
Se corre en tu compu o con Claude cuando se suman imágenes; Cloudflare no lo necesita.

- foto.jpg  → foto.webp        hasta 2000 px, para las placas de los casos
- foto.jpg  → foto-card.webp   900 px, solo para las fotos de las tarjetas del home (más livianas)

build.py usa el .webp automáticamente cuando existe; si no existe, sigue usando el original.
Los originales no se tocan (sirven para las placas de Behance).
"""
import json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
ASSETS = os.path.join(PUBLIC, 'assets')
SALTEAR = ('logos', 'fonts')   # logos y tipografías quedan como están
TODO = '--todo' in sys.argv

# Fotos que se ven en el home (tarjetas, menú, poster del video): llevan además versión -card
home = json.load(open(os.path.join(ROOT, 'content', 'home.json'), encoding='utf-8'))
CARDS = {t['imagen'] for t in home['tarjetas_home'] if t.get('imagen')}
CARDS |= {'assets/lolla/r13.jpg', 'assets/vuse/06.jpg', 'assets/ia/donatella-poster.jpg', 'assets/ia/up-si-vale.jpg', 'assets/reels/hero-poster.jpg'}

def guardar(im, dst, lado, calidad):
    im = im.copy()
    if max(im.size) > lado:
        im.thumbnail((lado, lado), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=calidad, method=6)

def vigente(src, dst):
    return not TODO and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)

antes = despues = n = 0
for dirpath, dirs, files in os.walk(ASSETS):
    if any(os.sep + s in dirpath for s in SALTEAR):
        continue
    for f in sorted(files):
        base, ext = os.path.splitext(f)
        if ext.lower() not in ('.jpg', '.jpeg', '.png'):
            continue
        src = os.path.join(dirpath, f)
        rel = os.path.relpath(src, PUBLIC).replace(os.sep, '/')
        salidas = [(os.path.join(dirpath, base + '.webp'), 2000, 75)]
        if rel in CARDS:
            salidas.append((os.path.join(dirpath, base + '-card.webp'), 900, 72))
        pendientes = [s for s in salidas if not vigente(src, s[0])]
        if not pendientes:
            continue
        im = Image.open(src)
        im.load()
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if im.mode in ('LA', 'P') else 'RGB')
        for dst, lado, calidad in pendientes:
            guardar(im, dst, lado, calidad)
        antes += os.path.getsize(src); despues += os.path.getsize(pendientes[0][0]); n += 1

print(f'ok · {n} imágenes · {antes/1e6:.1f} MB → {despues/1e6:.1f} MB' if n else 'ok · no había imágenes nuevas')

# Medidas de todas las imágenes (ancho, alto) para que build.py escriba width/height sin librerías externas
dims = {}
for dirpath, dirs, files in os.walk(ASSETS):
    for f in files:
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg', '.png', '.webp'):
            p = os.path.join(dirpath, f)
            with Image.open(p) as im:
                dims[os.path.relpath(p, PUBLIC).replace(os.sep, '/')] = list(im.size)
with open(os.path.join(ROOT, 'src', 'img_dims.json'), 'w', encoding='utf-8') as fh:
    json.dump(dict(sorted(dims.items())), fh, separators=(',', ':'))
print(f'ok · medidas de {len(dims)} imágenes en src/img_dims.json')
