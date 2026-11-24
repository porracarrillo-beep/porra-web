"""Piezas de SEO que arma build.py: schema, página propia por caso, sitemap y llms.txt.

Todo sale de los mismos textos de content/ y de las placas de cases.py: no hay que editar nada acá
para sumar o cambiar un caso.
"""
import html as _html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
DIMS = json.load(open(os.path.join(ROOT, 'src', 'img_dims.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'src', 'img_dims.json')) else {}

# ── Datos del estudio ────────────────────────────────────────────────────────────
# El nombre del director creativo va solo en los datos para buscadores (schema y llms.txt), no en la página.
PERSONA = {'nombre': 'José Carrillo', 'cargo': 'Director creativo', 'id': 'jose-carrillo',
           'perfiles': ['https://www.linkedin.com/in/josecarrilloporraia', 'https://www.behance.net/JoseCarrillo']}
DESCRIPCION = ('Estudio de dirección creativa y producción visual con IA en Buenos Aires. Campañas, imágenes y videos '
               'para marcas de gastronomía, consumo y real estate.')
SERVICIOS = ['Fotografía de producto con IA', 'Fotos de comida y bebida con IA', 'Video y reels con IA',
             'Contenido para redes de restaurantes', 'Key visuals y campañas', 'Imagen para real estate', 'Packaging y branding']
REDES = ['https://www.instagram.com/porra_ia/', 'https://www.behance.net/JoseCarrillo', 'https://www.linkedin.com/in/josecarrilloporraia']


def persona_schema(site):
    return {'@type': 'Person', '@id': f'{site}/#{PERSONA["id"]}', 'name': PERSONA['nombre'], 'jobTitle': PERSONA['cargo'],
            'worksFor': {'@id': f'{site}/#estudio'}, 'sameAs': PERSONA['perfiles']}


def schema_home(site):
    return json.dumps({
        '@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': f'{site}/#estudio',
        'name': 'PORRA', 'alternateName': 'Porra Studio', 'url': f'{site}/', 'logo': f'{site}/favicon.png',
        'image': f'{site}/og-image.jpg', 'email': 'hola@porra.studio', 'description': DESCRIPCION,
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Buenos Aires', 'addressCountry': 'AR'},
        'areaServed': ['Argentina', 'México', 'Estados Unidos'],
        'founder': persona_schema(site),
        'knowsAbout': ['Producción de contenido con IA', 'Fotografía de producto con IA', 'Fotografía gastronómica con IA',
                       'Video con IA para marcas', 'Reels para restaurantes', 'Dirección creativa', 'Dirección de arte',
                       'Imagen para real estate', 'Packaging y key visuals'],
        'sameAs': REDES}, ensure_ascii=False)


# ── Optimización del HTML: WebP, medidas, alt ───────────────────────────────────
_IMG_REF = re.compile(r'(?P<pre>["\'(])(?P<path>/?assets/[^"\'()\s?]+?)\.(?:jpe?g|png)(?P<q>\?[^"\')\s]*)?(?=["\')])')

def webp(html):
    """Cambia assets/x.jpg|png por assets/x.webp donde existe la versión liviana."""
    def sub(m):
        p = m.group('path')
        if os.path.exists(os.path.join(PUBLIC, p.lstrip('/') + '.webp')):
            return f'{m.group("pre")}{p}.webp{m.group("q") or ""}'
        return m.group(0)
    return _IMG_REF.sub(sub, html)

_IMG_TAG = re.compile(r'<img\b[^>]*>')
_SRC = re.compile(r'\bsrc="(/?assets/[^"?]+)')

def medidas(html):
    """Agrega width/height a cada <img> de assets/ que no los tenga (evita saltos de diseño)."""
    def sub(m):
        tag = m.group(0)
        if ' width=' in tag or '/logo' in tag:  # los logos van con alto fijo por CSS: un width los estiraría
            return tag
        s = _SRC.search(tag)
        d = s and DIMS.get(s.group(1).lstrip('/'))
        return tag[:-1].rstrip('/').rstrip() + f' width="{d[0]}" height="{d[1]}">' if d else tag
    return _IMG_TAG.sub(sub, html)

def alts(fragment, texto):
    """Las imágenes de las placas no tenían texto alternativo: les pone el del caso, numerado."""
    n = [0]
    def sub(m):
        n[0] += 1
        return f'alt="{_html.escape(texto, quote=True)} · {n[0]}"'
    return re.sub(r'alt=""', sub, fragment)


def card_thumb(path):
    """Versión -card.webp (900 px) para las tarjetas del home, si existe."""
    base = os.path.splitext(path.split('?')[0])[0]
    return base + '-card.webp' if os.path.exists(os.path.join(PUBLIC, base + '-card.webp')) else None


# ── Textos por caso ─────────────────────────────────────────────────────────────
def plano(s):
    s = re.sub(r'<br\s*/?>', ' ', s or '')
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', _html.unescape(s)).strip()

def recortar(s, n=158):
    if len(s) <= n:
        return s
    corte = s[:n].rsplit(' ', 1)[0].rstrip(',;:·—-')
    return corte + '…'

def info_caso(cid, frag, titles, cards):
    card = cards.get(cid, {})
    titulo = plano(card.get('titulo') or titles[cid])
    bajada = plano(card.get('bajada', ''))
    cuerpo = re.search(r'<p class="body"[^>]*>(.*?)</p>', frag, re.S)
    texto = plano(cuerpo.group(1)) if cuerpo else ''
    if not texto or '[a confirmar]' in texto:
        texto = plano(card.get('descripcion', ''))
    if not texto:
        texto = f'{titulo}: {bajada}.' if bajada else titulo
    desc = texto if len(texto) >= 90 else (texto.rstrip('.') + '. Dirección creativa y producción visual de Porra, estudio en Buenos Aires.')
    cat = plano(card.get('categoria', '')).replace('Caso · ', '')
    anio = re.search(r'[Aa]ño</dt><dd>[^<]*?(20\d\d)', frag)
    img = card.get('imagen') or (re.search(r'src="(assets/[^"]+\.(?:jpe?g|png))"', frag) or [None, None])[1]
    return dict(id=cid, titulo=titulo, intro=None if cuerpo else texto, bajada=bajada, cat=cat, pais=card.get('pais', ''), desc=recortar(desc),
                texto=texto, anio=anio.group(1) if anio else None, imagen=img)


# ── Página de caso ──────────────────────────────────────────────────────────────
CSS_PAGINA = '''
:root{--bg:#0b0b0b;--fg:#f3f3ef;--mut:#8f8f89;--line:#272725;--acc:#00d9ff;--pad:clamp(16px,2.6vw,40px)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font-family:"Inter Tight",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.45;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.lbl{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);font-weight:500}
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:9px 15px;font-size:14px;font-weight:500;transition:background .2s,color .2s,border-color .2s}
.pill:hover{background:#fff;color:#000;border-color:#fff}
.pill.solid{background:#fff;color:#000;border-color:#fff}.pill.solid:hover{background:var(--acc);border-color:var(--acc)}
.cp-h{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px var(--pad);background:rgba(11,11,11,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(6px)}
.cp-h img{height:28px;width:auto;display:block}.cp-h nav{display:flex;gap:8px}
.cp-intro{max-width:1400px;margin:0 auto;padding:clamp(40px,7vh,80px) var(--pad) clamp(28px,4vh,44px)}
.cp-intro .lbl a:hover{color:var(--fg)}
.cp-intro h1{margin-top:14px;font-size:clamp(34px,5.2vw,84px);font-weight:600;letter-spacing:-.018em;line-height:.95;text-transform:uppercase}
.cp-intro h1 span{display:block;margin-top:14px;font-size:clamp(17px,1.6vw,24px);font-weight:500;letter-spacing:-.005em;line-height:1.25;text-transform:none;color:var(--mut)}
.cp-txt{margin-top:22px;max-width:62ch;font-size:clamp(16px,1.2vw,19px);line-height:1.5;color:#cfcfca}
.cp-body{max-width:1400px;margin:0 auto}
.cp-body video.vmod{width:100%;display:block;background:#000}
.cp-next{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;gap:24px;padding:60px var(--pad);border-top:1px solid var(--line)}
.cp-next a{display:block;max-width:48%}.cp-next a:last-child{text-align:right}
.cp-next b{display:block;margin-top:8px;font-size:clamp(22px,3vw,44px);font-weight:600;letter-spacing:-.012em;line-height:1}
.cp-next a:hover b{color:var(--acc)}
.cp-cta{max-width:1400px;margin:0 auto;padding:clamp(50px,8vh,90px) var(--pad);border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
.cp-cta h2{font-size:clamp(30px,4.4vw,70px);font-weight:600;letter-spacing:-.015em;line-height:.95;text-transform:uppercase;max-width:14ch}
.cp-cta p{color:var(--mut);margin-top:12px;max-width:52ch}
.cp-cta .acts{display:flex;gap:8px;flex-wrap:wrap}
.cp-f{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line);padding:16px var(--pad) 28px;font-size:13px;color:var(--mut)}
.tbd{color:var(--tbd,#00d9ff)}
@media (max-width:600px){.cp-h .hide-m{display:none}.cp-next{flex-direction:column}.cp-next a{max-width:none}.cp-next a:last-child{text-align:left}}
'''

def pagina_caso(c, frag, prev, nxt, site, plates_css):
    url = f'{site}/trabajos/{c["id"]}'
    titulo_tag = f'{c["titulo"]} · {c["bajada"]} | Porra' if c['bajada'] else f'{c["titulo"]} | Porra'
    if len(titulo_tag) > 62 and c['bajada']:  # Google corta cerca de los 60
        titulo_tag = f'{c["titulo"]} · {c["bajada"].split(" · ")[0]} | Porra'
    og_img = f'{site}/{c["imagen"]}' if c['imagen'] else f'{site}/og-image.jpg'
    obra = {'@type': 'CreativeWork', '@id': f'{url}#trabajo', 'name': c['titulo'], 'headline': f'{c["titulo"]} · {c["bajada"]}'.strip(' ·'),
            'description': c['texto'], 'url': url, 'image': og_img, 'inLanguage': 'es',
            'creator': [{'@id': f'{site}/#estudio'}, {'@id': f'{site}/#{PERSONA["id"]}'}], 'publisher': {'@id': f'{site}/#estudio'}}
    if c['cat']:
        obra['genre'] = c['cat']
    if c['anio']:
        obra['dateCreated'] = c['anio']
    schema = {'@context': 'https://schema.org', '@graph': [
        obra,
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Porra', 'item': f'{site}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Trabajos', 'item': f'{site}/#trabajos'},
            {'@type': 'ListItem', 'position': 3, 'name': c['titulo'], 'item': url}]},
        {'@type': 'ProfessionalService', '@id': f'{site}/#estudio', 'name': 'PORRA', 'url': f'{site}/', 'logo': f'{site}/favicon.png'},
        persona_schema(site)]}
    meta = ' · '.join(x for x in (c['cat'], c['pais']) if x)
    e = lambda s: _html.escape(s, quote=True)
    # La primera imagen (la portada) se carga ya; el resto, a medida que se baja
    first = [True]
    def lazy(m):
        tag = m.group(0)
        if first[0]:
            first[0] = False
            return tag.replace('<img ', '<img fetchpriority="high" ', 1).replace(' loading="lazy"', '')
        return tag if 'loading=' in tag or 'class="mark"' in tag else tag.replace('<img ', '<img loading="lazy" ', 1)
    cuerpo = re.sub(r'<img\b[^>]*>', lazy, frag)
    doc = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo_tag)}</title>
<meta name="description" content="{e(c['desc'])}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0b0b0b">
<meta property="og:type" content="article">
<meta property="og:site_name" content="PORRA">
<meta property="og:title" content="{e(titulo_tag)}">
<meta property="og:description" content="{e(c['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<style>
{plates_css}
{CSS_PAGINA}
</style>
</head>
<body>
<header class="cp-h">
  <a href="/" aria-label="Porra, inicio"><img src="assets/logo-white.png" alt="Porra"></a>
  <nav><a class="pill hide-m" href="/#trabajos">Todos los trabajos</a><a class="pill solid" href="/#contacto">Hablemos</a></nav>
</header>
<main>
  <div class="cp-intro">
    <p class="lbl"><a href="/#trabajos">Trabajos</a>{(' · ' + e(meta)) if meta else ''}</p>
    <h1>{e(c['titulo'])}{f'<span>{e(c["bajada"])}</span>' if c['bajada'] else ''}</h1>
    {f'<p class="cp-txt">{e(c["intro"])}</p>' if c.get('intro') else ''}
  </div>
  <article class="cp-body">
{cuerpo}
  </article>
  <nav class="cp-next" aria-label="Más casos">
    <a href="/trabajos/{prev['id']}"><span class="lbl">← Caso anterior</span><b>{e(prev['titulo'])}</b></a>
    <a href="/trabajos/{nxt['id']}"><span class="lbl">Siguiente caso →</span><b>{e(nxt['titulo'])}</b></a>
  </nav>
  <section class="cp-cta">
    <div><h2>¿Tenés un proyecto así?</h2><p>Dirección creativa senior y producción propia con IA: campañas, imágenes y videos listos para usar.</p></div>
    <div class="acts"><a class="pill solid" href="/#contacto">Escribinos →</a><a class="pill" href="mailto:hola@porra.studio">hola@porra.studio</a></div>
  </section>
</main>
<footer class="cp-f"><span>© 2026 Porra · Dirección creativa y producción visual con IA · Buenos Aires</span><span><a href="/">porra.studio</a></span></footer>
<script>try{{const k='porra_vistos',s=JSON.parse(sessionStorage.getItem(k)||'[]'),t={json.dumps(c['titulo'], ensure_ascii=False)};if(!s.includes(t)){{s.push(t);sessionStorage.setItem(k,JSON.stringify(s.slice(-20)))}}if(!sessionStorage.getItem('porra_origen'))sessionStorage.setItem('porra_origen',document.referrer||'directo')}}catch(e){{}}</script>
</body>
</html>
'''
    # Rutas absolutas: la página vive en /trabajos/, no en la raíz
    doc = webp(doc)
    doc = medidas(doc)
    return re.sub(r'(["\'(])assets/', r'\1/assets/', doc)


def sitemap(site, ids):
    urls = [f'{site}/'] + [f'{site}/trabajos/{i}' for i in ids]
    body = ''.join(f'<url><loc>{u}</loc></url>' for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n'


def llms(site, casos):
    lineas = [
        '# PORRA', '',
        f'> Estudio de dirección creativa y producción visual con IA en Buenos Aires, dirigido por {PERSONA["nombre"]} '
        '(25 años en Ogilvy, Geometry y Hogarth-WPP). Campañas, imágenes y videos para marcas de gastronomía, consumo '
        'y real estate en Argentina, México y Estados Unidos.', '',
        'Porra combina dirección creativa senior con producción propia de imagen y video con IA. Entrega archivos finales '
        'para pauta, redes, punto de venta o impresión; la publicación y la compra de medios quedan del lado de la marca.', '',
        '## Servicios'] + [f'- {s}' for s in SERVICIOS] + ['', '## Casos'] + [
        f'- [{c["titulo"]}]({site}/trabajos/{c["id"]}): {c["bajada"] or c["cat"]}' + (f' ({c["pais"]})' if c['pais'] and c['pais'] not in (c['bajada'] or '') else '') for c in casos] + [
        '', '## Contacto', f'- [Sitio]({site}/)', '- Email: hola@porra.studio',
        '- [Instagram](https://www.instagram.com/porra_ia/)', '- [Behance](https://www.behance.net/JoseCarrillo)',
        '- [LinkedIn](https://www.linkedin.com/in/josecarrilloporraia)', '']
    return '\n'.join(lineas)
