# Genera las placas de cada caso (HTML compartido entre el sitio y Behance)
import os as _os0
ROOT = _os0.path.dirname(_os0.path.dirname(_os0.path.abspath(__file__)))
TBD = '<span class="tbd">[a confirmar]</span>'

def P(ratio, inner, extra='', cls=''):
    return f'<section class="plate {cls}" style="aspect-ratio:{ratio};{extra}">{inner}</section>'

def ficha(rows):
    return '<dl class="ficha">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl>'

def hero(img, kicker, title, sub, label, pos='center'):
    return P('1400/880', f'''
<img class="abs cover" src="{img}" style="object-position:{pos}" alt="">
<div class="abs shade"></div>
<img class="mark" src="assets/logo-white.png" alt="Porra">
<div class="tr lbl" style="color:#e8e8e4">{label}</div>
<div class="bottom" style="color:#fff">
  <div class="lbl" style="color:#e8e8e4;margin-bottom:calc(var(--u)*18)">{kicker}</div>
  <div class="h1">{title}</div>
  <div class="h3" style="margin-top:calc(var(--u)*20);font-weight:400;color:#e8e8e4">{sub}</div>
</div>''')

def statement(label, head, es, en, rows, ratio='1400/760'):
    return P(ratio, cls='txt', inner=f'''
<div class="pad lay" style="display:grid;grid-template-columns:1.25fr 1fr;gap:calc(var(--u)*96);height:100%;align-content:center">
  <div>
    <div class="lbl" style="margin-bottom:calc(var(--u)*28)">{label}</div>
    <div class="h2" style="margin-bottom:calc(var(--u)*32)">{head}</div>
    <p class="body" style="margin-bottom:calc(var(--u)*18)">{es}</p>
    <p class="en">{en}</p>
  </div>
  <div style="align-self:center">{ficha(rows)}</div>
</div>''')

def band(label, text):
    return f'<div class="band"><div class="lbl">{label}</div><div class="h3">{text}</div></div>'

def full(img, ratio='1400/788', fit='cover', pos='center', pad=0):
    st = f'padding:calc(var(--u)*{pad})' if pad else ''
    return P(ratio, f'<div class="abs" style="{st}"><img class="{fit}" src="{img}" style="object-position:{pos}" alt=""></div>')

def row(imgs, ratio, fit='cover', gap=12, pad=0, cols=None):
    cols = cols or ' '.join(['1fr'] * len(imgs))
    cells = ''.join(f'<div style="overflow:hidden;min-height:0"><img class="{fit}" src="{i}" alt=""></div>' for i in imgs)
    return P(ratio, f'<div class="abs grid" style="grid-template-columns:{cols};gap:calc(var(--u)*{gap});padding:calc(var(--u)*{pad})">{cells}</div>')

def closing(credits, results=None):
    res = ''
    if results:
        cells = ''.join(f'<div class="metric"><div class="v">{v}</div><div class="small" style="margin-top:calc(var(--u)*10)">{r}</div></div>' for v, r in results)
        res = f'''<div><div class="lbl" style="margin-bottom:calc(var(--u)*28)">El festival</div>
<div class="grid cols2" style="grid-template-columns:1fr 1fr;gap:calc(var(--u)*28) calc(var(--u)*40)">{cells}</div>
<p class="small" style="margin-top:calc(var(--u)*24);opacity:.7">Lollapalooza Argentina 2023 · cifras del festival según la organización.</p></div>'''
    return P('1400/720', cls='txt', inner=f'''
<div class="pad lay" style="display:grid;grid-template-columns:{'1.1fr 1fr' if results else '1fr 1fr'};gap:calc(var(--u)*110);height:100%;align-content:center">
  {res or '<div><div class="lbl" style="margin-bottom:calc(var(--u)*28)">Porra</div><div class="h2">Dirección creativa<br>y producción.</div></div>'}
  <div><div class="lbl" style="margin-bottom:calc(var(--u)*28)">Créditos</div>{ficha(credits)}</div>
</div>
<img class="ft" src="assets/logo-white.png" alt="Porra" style="position:absolute;left:calc(var(--u)*72);bottom:calc(var(--u)*48);width:calc(var(--u)*96);height:auto;filter:var(--logo-filter,none)">
<div class="small ft" style="position:absolute;right:calc(var(--u)*72);bottom:calc(var(--u)*52)">hola@porra.studio · behance.net/JoseCarrillo</div>''')

# ---------------------------------------------------------------- LOLLAPALOOZA
L = 'assets/lolla/'
lolla = [
 hero(L+'r01.jpg', 'Caso 01 · Coca-Cola', 'Coca-Cola ×<br>Lollapalooza', 'Stand oficial · Lollapalooza Argentina 2023', 'Experiencia de marca'),
 statement('El proyecto', 'Dos mundos<br>en 100 m².',
   'Coca-Cola llegó a Lollapalooza Argentina 2023 con un stand de dos niveles pensado para la Generación Z. Afuera, un volumen que funciona como pantalla de día y de noche. Adentro, dos mundos: el rojo de Coke Studio, con música y streaming, y el rosa de Coca-Cola Move, la co-creación con Rosalía.',
   'Coca-Cola arrived at Lollapalooza Argentina 2023 with a two-level stand built for Gen Z. Outside, a volume that works as a screen by day and by night. Inside, two worlds: the red of Coke Studio, with music and streaming, and the pink of Coca-Cola Move, the co-creation with Rosalía.',
   [('Cliente','Coca-Cola'),('País','Argentina'),('Evento','Lollapalooza Argentina 2023'),('Pieza','Stand oficial de marca'),('Superficie','100 m² · dos niveles con terraza'),
    ('Disciplinas','Diseño de stand · Arquitectura efímera · Render 3D'),('Herramientas','3ds Max · Photoshop'),('Rol','Dirección creativa y de arte'),('Agencia','Catch'),('Stand','Liebre Studio')]),
 P('1400/900', cls='txt', inner=f'''
<div class="lay0" style="display:grid;grid-template-columns:1fr calc(var(--u)*500);height:100%">
 <div class="pad lay" style="display:flex;flex-direction:column;justify-content:space-between">
  <div>
   <div class="lbl" style="margin-bottom:calc(var(--u)*26)"><b>01</b> · El brief</div>
   <div class="small" style="margin-bottom:calc(var(--u)*14)">El objetivo del cliente</div>
   <div class="h2" style="font-size:calc(var(--u)*49);margin-bottom:calc(var(--u)*24)">“Ser un motor de reclutamiento de adolescentes.”</div>
   <p class="body" style="max-width:calc(var(--u)*640)">Crear el mayor stand de reclutamiento de jóvenes del festival, con una experiencia física y emocional.</p>
   <p class="en" style="margin-top:calc(var(--u)*10);max-width:calc(var(--u)*640)">“Become a teen recruitment engine”: the festival’s biggest youth stand, with a physical and emotional experience.</p>
  </div>
  <div>
   <div class="small" style="margin-bottom:calc(var(--u)*18)">Lo que pedía el brief</div>
   <div class="req">
    <div><span class="num">01</span>100 m², planta cuadrada</div>
    <div><span class="num">02</span>Dos pisos con terraza y baranda</div>
    <div><span class="num">03</span>Pantallas y luces que se vean de día y de noche</div>
    <div><span class="num">04</span>Mucha altura, mucho impacto</div>
    <div><span class="num">05</span>Rampa de accesibilidad</div>
    <div><span class="num">06</span>60 % Coke Studio · 40 % Rosalía Co-creations</div>
   </div>
  </div>
 </div>
 <div class="side" style="overflow:hidden"><img class="cover" src="{L}r02.jpg" style="object-position:38% center" alt=""></div>
</div>'''),
 P('1400/860', cls='txt', inner=f'''
<div class="pad lay" style="height:100%;display:flex;flex-direction:column">
 <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:calc(var(--u)*44)">
  <div><div class="lbl" style="margin-bottom:calc(var(--u)*22)"><b>02</b> · La respuesta</div><div class="h2" style="font-size:calc(var(--u)*47)">Tres ejes, un solo recorrido.</div></div>
  <p class="en" style="max-width:calc(var(--u)*380);text-align:right">Three axes, one journey: music, co-creation and brand experience.</p>
 </div>
 <div class="grid cols" style="grid-template-columns:repeat(3,1fr);gap:calc(var(--u)*28);flex:1;min-height:0">
  <div style="display:flex;flex-direction:column"><div style="aspect-ratio:4/3;overflow:hidden;margin-bottom:calc(var(--u)*20)"><img class="cover" src="{L}r10.jpg" alt=""></div><span class="num">01</span><div class="h4" style="margin:calc(var(--u)*8) 0 calc(var(--u)*10)">Coke Studio</div><p class="small">La música como punto de encuentro: cabina, espacio de streaming y lounge para amplificar lo que pasa en vivo.</p></div>
  <div style="display:flex;flex-direction:column"><div style="aspect-ratio:4/3;overflow:hidden;margin-bottom:calc(var(--u)*20)"><img class="cover" src="{L}r07.jpg" alt=""></div><span class="num">02</span><div class="h4" style="margin:calc(var(--u)*8) 0 calc(var(--u)*10)">Co-creations · Rosalía</div><p class="small">El mundo rosa de Coca-Cola Move: maquillaje, beauty, tattoo y la moto como photo opportunity.</p></div>
  <div style="display:flex;flex-direction:column"><div style="aspect-ratio:4/3;overflow:hidden;margin-bottom:calc(var(--u)*20)"><img class="cover" src="{L}r11.jpg" alt=""></div><span class="num">03</span><div class="h4" style="margin:calc(var(--u)*8) 0 calc(var(--u)*10)">Experiencia Coca-Cola</div><p class="small">Dinámicas que invitan a participar, con merchandising como premio y captura de datos.</p></div>
 </div>
</div>'''),
 P('1400/1190', f'''{band('<b>03</b> · Arquitectura', 'Un volumen que se lee de lejos: ondas rojas y negras sobre las caras, líneas de luz en los bordes.')}
<div class="grid" style="grid-template-columns:1fr 1fr;gap:calc(var(--u)*12);padding:0 calc(var(--u)*64) calc(var(--u)*64);height:calc(100% - var(--u)*210)">
 <div style="overflow:hidden"><img class="cover" src="{L}r02.jpg" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}r03.jpg" alt=""></div>
 <div style="overflow:hidden"><img class="cover" src="{L}r04.jpg" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}r05.jpg" alt=""></div>
</div>'''),
 P('1400/700', f'''<div class="abs grid" style="grid-template-columns:1fr 1fr;gap:calc(var(--u)*12);padding:calc(var(--u)*64) calc(var(--u)*64) calc(var(--u)*90)">
 <div style="overflow:hidden"><img class="cover" src="{L}r17.jpg" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}r18.jpg" alt=""></div></div>
 <div class="lbl" style="position:absolute;left:calc(var(--u)*64);bottom:calc(var(--u)*44)">Vistas cenitales · recorrido entre los dos mundos</div>'''),
 P('1400/1230', f'''{band('<b>04</b> · Coke Studio', 'Rojo, cabina y lounge: el mundo de la música.')}
<div style="padding:0 calc(var(--u)*64);height:calc(var(--u)*720)"><img class="cover" src="{L}r13.jpg" alt=""></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:calc(var(--u)*12);padding:calc(var(--u)*12) calc(var(--u)*64) 0;height:calc(var(--u)*318)">
 <div style="overflow:hidden"><img class="cover" src="{L}r14.jpg" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}r15.jpg" alt=""></div></div>'''),
 P('1400/1230', f'''{band('<b>05</b> · Co-creations', 'Rosa, beauty y la moto: el mundo de Coca-Cola Move con Rosalía.')}
<div style="padding:0 calc(var(--u)*64);height:calc(var(--u)*720)"><img class="cover" src="{L}r06.jpg" alt=""></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:calc(var(--u)*12);padding:calc(var(--u)*12) calc(var(--u)*64) 0;height:calc(var(--u)*318)">
 <div style="overflow:hidden"><img class="cover" src="{L}r08.jpg" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}r09.jpg" alt=""></div></div>'''),
 P('1400/980', f'''{band('<b>06</b> · Experiencia y store', 'Merch como premio: el stand también es tienda.')}
<div class="grid" style="grid-template-columns:1.6fr 1fr;gap:calc(var(--u)*12);padding:0 calc(var(--u)*64) calc(var(--u)*64);height:calc(100% - var(--u)*210)">
 <div style="overflow:hidden"><img class="cover" src="{L}r12.jpg" alt=""></div>
 <div class="grid" style="grid-template-rows:1fr 1fr;gap:calc(var(--u)*12)"><div style="overflow:hidden"><img class="cover" src="{L}r11.jpg" alt=""></div><div style="overflow:hidden;background:#f4f1ee"><img class="contain" src="{L}osos.jpg" alt=""></div></div>
</div>'''),
 P('1400/760', f'''{band('<b>07</b> · Del render al predio', 'El mismo lenguaje, construido en el festival.')}
<div class="grid" style="grid-template-columns:1.55fr 1fr;gap:calc(var(--u)*12);padding:0 calc(var(--u)*64) calc(var(--u)*90);height:calc(100% - var(--u)*210)">
 <div style="overflow:hidden"><img class="cover" src="{L}r13.jpg" style="object-position:center 30%" alt=""></div><div style="overflow:hidden"><img class="cover" src="{L}real.jpg" alt=""></div></div>
<div class="lbl" style="position:absolute;left:calc(var(--u)*64);bottom:calc(var(--u)*44)">Render · stand en Lollapalooza Argentina 2023</div>'''),
 closing([('Cliente','Coca-Cola'),('Agencia','Catch'),('Dirección creativa y de arte','José Carrillo'),('Diseño y producción del stand','Liebre Studio'),('Año','2023')],
         [('330 mil','personas en los tres días del festival'),('110 mil','personas por jornada'),('+1 millón','siguieron los shows en vivo por Flow')]),
]

# ---------------------------------------------------------------- OTROS CASOS
V = 'assets/vuse/'
vuse = [
 hero(V+'10.jpg', 'Caso 02 · VUSE', 'VUSE USA', 'Identidad visual y packaging', 'Branding · Packaging · Punto de venta', pos='60% center'),
 statement('El proyecto', 'Un sistema de packaging,<br>dos direcciones.',
   'Sistema visual y de packaging para VUSE en Estados Unidos. Exploramos dos caminos: fotografía de ciudad con el dispositivo en mano y un sistema de formas de color sobre blanco y negro. Después lo llevamos al backbar del punto de venta y a la campaña.',
   'Visual and packaging system for VUSE in the United States: two directions, city photography and a colour-shape system on black and white, extended to the retail backbar and the campaign.',
   [('Cliente','VUSE'),('País','Estados Unidos'),('Alcance','Identidad visual · Packaging · Punto de venta'),('Año','2021'),('Rol','Dirección creativa y de arte'),('Agencia','Hogarth')]),
 row([V+'03.jpg',V+'04.jpg',V+'05.jpg'],'1400/520',fit='contain',pad=40,gap=20),
 full(V+'06.jpg','1400/676','contain',pad=40),
 full(V+'07.jpg','1400/676','contain',pad=40),
 row([V+'01.jpg',V+'08.jpg'],'1400/700',fit='contain',pad=40,gap=20),
 full(V+'09.jpg','1400/560','contain',pad=40),
 closing([('Cliente','VUSE'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo')]),
]
N = 'assets/nas/'
nas = [
 hero(N+'01.jpg', 'Caso 03 · Natural American Spirit', 'Natural American<br>Spirit · 40 años', 'Packs de edición especial y comunicación', 'Packaging · Campaña'),
 statement('El proyecto', 'Cuarenta años,<br>contados por su gente.',
   'Ediciones especiales y piezas de comunicación para los 40 años de la marca. El número 40 funciona como sistema gráfico y los retratos de productores ponen cara a la historia, con una invitación a la celebración “Free spirits for forty years”.',
   'Special-edition packs and communication for the brand’s 40th anniversary: the number 40 as a graphic system, grower portraits and an invitation to the “Free spirits for forty years” celebration.',
   [('Cliente','Natural American Spirit'),('País','Estados Unidos'),('Alcance','Packaging · Key visual · Piezas de invitación'),('Año','2021'),('Rol','Dirección creativa y de arte'),('Agencia','Hogarth')]),
 full(N+'03.jpg','1400/719','contain',pad=40),
 row([N+'02.jpg',N+'04.jpg'],'1400/420',fit='contain',pad=40,gap=20),
 row([N+'05.jpg',N+'06.jpg'],'1400/760',fit='contain',pad=40,gap=20),
 row([N+'07.jpg',N+'08.jpg'],'1400/760',fit='contain',pad=40,gap=20,cols='0.7fr 1.3fr'),
 closing([('Cliente','Natural American Spirit'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo')]),
]
K = 'assets/camel/'
camel = [
 hero(K+'02.jpg', 'Caso 04 · Camel SNUS', 'Camel SNUS', 'Identidad visual para comunicación · USA', 'Campaña · Sistema gráfico', pos='center 30%'),
 statement('El proyecto', 'La lata como protagonista.',
   'Sistema visual para la comunicación de Camel SNUS en Estados Unidos: tipografía a gran escala, la lata en primer plano y la advertencia sanitaria integrada a la grilla de cada pieza.',
   'Visual system for Camel SNUS communication in the US: large-scale type, the tin up front and the health warning built into each layout grid.',
   [('Cliente','Camel SNUS'),('País','Estados Unidos'),('Alcance','Sistema gráfico · Piezas de campaña'),('Año','2022'),('Rol','Dirección creativa y de arte'),('Agencia','Hogarth')]),
 row([K+'01.jpg',K+'02.jpg'],'1400/880',fit='contain',pad=40,gap=20),
 row([K+'03.jpg',K+'04.jpg',K+'05.jpg'],'1400/600',fit='contain',pad=40,gap=20),
 closing([('Cliente','Camel SNUS'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo')]),
]
LN = 'assets/lanacion/'
lanacion = [
 hero(LN+'p-7.jpg', 'Caso 05 · La Nación', 'La Nación · LN Campo', 'Arte y storyboard para videos institucionales', 'Dirección de arte · Storyboard'),
 statement('El proyecto', 'Del diario al campo,<br>en una sola secuencia.',
   'Dirección de arte y storyboard para los videos institucionales de LN Campo. La secuencia lleva al espectador del diario impreso al campo y de ahí a la app, con transiciones que nacen del propio paisaje.',
   'Art direction and storyboard for LN Campo institutional videos: from the printed paper to the field and on to the app, with transitions born from the landscape itself.',
   [('Cliente','La Nación · LN Campo'),('País','Argentina'),('Alcance','Dirección de arte · Storyboard · Videos institucionales'),('Año','2022'),('Rol','Dirección creativa y de arte'),('Agencia','Hogarth')]),
 row([LN+'p-1.jpg',LN+'p-2.jpg'],'1400/400',pad=40,gap=20),
 row([LN+'p-3.jpg',LN+'p-4.jpg'],'1400/400',pad=40,gap=20),
 row([LN+'p-5.jpg',LN+'p-6.jpg'],'1400/400',pad=40,gap=20),
 row([LN+'p-8.jpg',LN+'p-9.jpg'],'1400/400',pad=40,gap=20),
 closing([('Cliente','La Nación'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo')]),
]

CASES = {
 'lollapalooza': dict(plates=lolla, light=False, acc='#ff2a2a'),
 'vuse': dict(plates=vuse, light=True, acc='#d6247a'),
 'natural-american-spirit': dict(plates=nas, light=True, acc='#d9821e'),
 'camel-snus': dict(plates=camel, light=True, acc='#1f63c4'),
 'la-nacion': dict(plates=lanacion, light=False, acc='#3fb28c'),
}

def fragment(cid):
    c = CASES[cid]
    cls = 'plates light' if c['light'] else 'plates'
    style = f' style="--acc:{c["acc"]};' + ('--logo-filter:invert(1)' if c['light'] else '') + '"'
    return f'<div class="{cls}"{style}>' + '\n'.join(c['plates']) + '</div>'

if __name__ == '__main__':
    import sys
    for cid in CASES:
        open(_os0.path.join(ROOT, 'public', f'render-{cid}.html'), 'w', encoding='utf-8').write(
            '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="plates.css">'
            '<style>html,body{margin:0;background:#000}.plates{width:1400px}</style></head><body>'
            + fragment(cid) + '</body></html>')
    print('ok')

# ================================================================ CASOS IA (v4)
import json as _json, os as _os
_DIMS = _json.load(open(_os.path.join(ROOT, 'src', 'ia_dims.json')))

def jrows(items, target=2.7, pad=72, gap=22):
    rows, cur, s = [], [], 0
    for it in items:
        cur.append(it); s += it[1] / it[2]
        if s >= target: rows.append(cur); cur, s = [], 0
    if cur: rows.append(cur)
    out = []
    for r in rows:
        rs = [w / h for _, w, h in r]
        inner = 1400 - 2 * pad - gap * (len(r) - 1)
        hh = inner / sum(rs)
        if len(rows) > 1 and r is rows[-1] and sum(rs) < target * .55:
            hh = min(hh, inner / target * 1.3)
        H = hh + gap
        cells = ''.join(f'<div style="flex:{x:.4f};aspect-ratio:{x:.4f};overflow:hidden"><img class="cover" src="{p}" alt="" loading="lazy"></div>' for (p, _, _), x in zip(r, rs))
        out.append(P(f'1400/{H:.1f}', f'<div class="abs" style="display:flex;justify-content:center;gap:calc(var(--u)*{gap});padding:calc(var(--u)*{gap/2}) calc(var(--u)*{pad})">{cells}</div>'))
    return out

def ia_case(cid, num, kicker, title, sub, label, head, es, en, rows, credits=None, sections=None, hero_pos='center', hero_img=None):
    imgs = _DIMS[cid]
    plates = [hero(hero_img or imgs[0][0], f'Caso {num} · {kicker}', title, sub, label, pos=hero_pos), statement('El proyecto', head, es, en, rows)]
    if sections:
        for lab, txt, a, b in sections:
            plates.append(P('1400/170', band(lab, txt)))
            plates += jrows(imgs[a:b])
    else:
        plates += jrows(imgs[1:])
    plates.append(closing(credits or [('Estudio', 'Porra IA · Buenos Aires'), ('Dirección creativa', 'José Carrillo'), ('Producción', 'Imagen con IA bajo dirección de arte'), ('Rol / agencia', TBD)]))
    return plates

# Los textos de los casos IA viven en content/casos-ia.json (editable sin tocar código)
def _tbd(x):
    if isinstance(x, str): return x.replace('[a confirmar]', TBD)
    if isinstance(x, list): return [_tbd(i) for i in x]
    if isinstance(x, dict): return {k: _tbd(v) for k, v in x.items()}
    return x

_IA = _tbd(_json.load(open(_os.path.join(ROOT, 'content', 'casos-ia.json'), encoding='utf-8')))
IA_CASES = {}
for _cid, _d in _IA.items():
    IA_CASES[_cid] = dict(light=_d['oscuro_o_claro'] == 'claro', acc=_d['color_acento'], plates=ia_case(
        _cid, _d['numero'], _d['etiqueta_superior'], _d['titulo'], _d['subtitulo'], _d['rubro'], _d['titular'],
        _d['texto_es'], _d['texto_en'], list(_d['ficha'].items()),
        credits=list(_d['creditos'].items()) if _d.get('creditos') else None,
        sections=[(x['titulo'], x['texto'], x['desde_imagen'], x['hasta_imagen']) for x in _d['secciones']] if _d.get('secciones') else None,
        hero_pos=_d.get('portada_posicion', 'center'), hero_img=_d.get('portada_imagen')))
for k, v in IA_CASES.items(): CASES[k] = v

def oxxo_hero():
    return P('1400/880', f"""
<div class="abs" style="background:#e4002b"></div>
<img class="mark" src="assets/logo-white.png" alt="Porra">
<div class="tr lbl" style="color:#fff">Key visuals · Punto de venta</div>
<div class="abs" style="left:calc(var(--u)*560);right:calc(var(--u)*64);top:calc(var(--u)*150);bottom:calc(var(--u)*64);background:#fff;border-radius:calc(var(--u)*6);overflow:hidden">
  <img src="assets/cases/oxxo/OXXO_01.jpg" alt="" style="width:100%;height:100%;object-fit:contain;padding:calc(var(--u)*24)">
</div>
<div class="bottom" style="color:#fff;right:auto;max-width:calc(var(--u)*460)">
  <div class="lbl" style="color:#fff;margin-bottom:calc(var(--u)*18)">Caso 12 · Coca-Cola × OXXO</div>
  <div class="h1" style="font-size:calc(var(--u)*88)">Coca-Cola<br>× OXXO</div>
  <div class="h3" style="margin-top:calc(var(--u)*20);font-weight:400;color:#fff">Promociones de verano · México</div>
</div>""")

OXXO = [oxxo_hero(),
  statement('El proyecto', 'Dos promos,<br>un mismo mostrador.',
   'Key visuals y material de punto de venta para dos promociones de Coca-Cola en las tiendas OXXO de México. El reto: que el premio se entienda en un golpe de vista, entre cientos de productos. Composición de packshot con todos los premios en una sola escena, y un sistema que baja del key visual a afiches, exhibidores y cenefas con la mecánica en tres pasos.',
   'Key visuals and point-of-sale material for two Coca-Cola promotions at OXXO stores in Mexico: every prize in a single packshot composition, rolled out to posters, displays and shelf strips with a three-step mechanic.',
   [('Cliente','Coca-Cola México × OXXO'),('País','México'),('Promos','Desbloquea tu verano · Llévatela Chilloxxo'),('Alcance','Key visual · Material POP'),('Técnica','Composición y retoque de packshot'),('Herramientas','Photoshop · Illustrator'),('Rol','Dirección de arte'),('Agencia / año','Morfina · 2023')]),
  P('1400/170', band('<b>01</b> · Desbloquea tu verano', 'Gaming, tecnología y viajes: todo el verano en una sola imagen.')),
  full('assets/cases/oxxo/OXXO_01.jpg', ratio='2400/1676', fit='contain'),
  full('assets/cases/oxxo/OXXO_02.jpg', ratio='2400/1264', fit='contain'),
  P('1400/170', band('<b>02</b> · Llévatela Chilloxxo', 'Con Coca-Cola Sin Azúcar: el premio son dos Dolphin Mini.')),
  full('assets/cases/oxxo/OXXO_03.jpg', ratio='2400/1264', fit='contain'),
  full('assets/cases/oxxo/OXXO_04.jpg', ratio='2400/1264', fit='contain'),
  closing([('Cliente','Coca-Cola México'),('Retail','OXXO'),('Agencia','Morfina'),('Dirección de arte','José Carrillo'),('Año','2023')])]
CASES['oxxo'] = dict(light=True, acc='#e4002b', plates=OXXO)

def conexo_hero():
    return P('1400/880', f"""
<div class="abs" style="background:#0098b8"></div>
<img class="abs" src="assets/cases/conexo/CONEXO_01.jpg" alt="" style="left:auto;right:0;width:66%;height:100%;object-fit:cover;object-position:12% center">
<img class="mark" src="assets/logo-white.png" alt="Porra">
<div class="tr lbl" style="color:#fff">Identidad · Campaña</div>
<div class="bottom" style="color:#fff;right:auto;max-width:calc(var(--u)*440)">
  <div class="lbl" style="color:#fff;margin-bottom:calc(var(--u)*18)">Caso 13 · Conexo</div>
  <div class="h1" style="font-size:calc(var(--u)*88)">Presta<br>Conexo</div>
  <div class="h3" style="margin-top:calc(var(--u)*20);font-weight:400;color:#fff">Préstamos simples · Fintech</div>
</div>""")

CONEXO = [conexo_hero(),
  statement('El proyecto', 'Un préstamo<br>en una palabra.',
   'Identidad y campaña para Presta Conexo, la línea de préstamos de Conexo Finance. Todo el sistema se apoya en una sola idea: <b>simple</b>. Una palabra gigante, un cian propio y retratos llenos de energía, que bajan sin perder fuerza a mailings, piezas de punto de contacto, posteos, banners y un set de botones por monto, de $50 mil a $300 mil.',
   'Identity and campaign for Presta Conexo, Conexo Finance’s loan line, built on a single word, “simple”, rolled out to mailings, point-of-contact pieces, social posts, banners and a set of amount buttons.',
   [('Cliente','Conexo Finance'),('País','Argentina'),('Rubro','Fintech · Préstamos'),('Alcance','Identidad · Campaña · Piezas digitales y POP'),('Concepto','“Simple”'),('Rol','Dirección creativa y de arte'),('Año','2022 · Cliente directo')]),
  full('assets/cases/conexo/CONEXO_02.jpg', ratio='2088/1694', fit='contain'),
  full('assets/cases/conexo/CONEXO_03.jpg', ratio='2088/1694', fit='contain'),
  closing([('Cliente','Conexo Finance · cliente directo'),('Dirección creativa y de arte','José Carrillo'),('Año','2022')])]
CASES['conexo'] = dict(light=True, acc='#0098b8', plates=CONEXO)



# Casos con placas de Behance ya armadas
BEH = {
 'donatella': dict(n=15, bg='#F3ECE2', video=('assets/ia/donatella.mp4', 13)),
 'miami-restaurants': dict(n=20, bg='#F7F3EE'),
 'real-estate': dict(n=21, bg='#F5F1E6'),
 'ena': dict(n=16, bg='#F5F1E6'),
}
_PREF = {'donatella': 'DONATELLA', 'miami-restaurants': 'FOOD', 'real-estate': 'RE', 'ena': 'ENA'}
def beh_fragment(cid):
    b = BEH[cid]; out = []
    for i in range(1, b['n'] + 1):
        out.append(f'<img src="assets/cases/{cid}/{_PREF[cid]}_{i:02d}.jpg" alt="" loading="lazy" style="display:block;width:100%;height:auto">')
        if b.get('video') and i == b['video'][1]:
            out.append(f'<video class="vmod" src="{b["video"][0]}" muted loop playsinline controls autoplay style="display:block;width:100%;max-height:90vh;background:{b["bg"]}"></video>')
    return f'<div style="background:{b["bg"]}">' + ''.join(out) + '</div>'


# ================================================================ CASOS DE MARCA (v5): VW, Corona, Brahma, Prisma
# Medidas de las imágenes (src/brand_dims.json) para no depender de librerías externas en el build
_BDIMS = _json.load(open(_os.path.join(ROOT, 'src', 'brand_dims.json')))
def _dims(cid, nums):
    return [[f'assets/cases/{cid}/{n:02d}.jpg'] + _BDIMS[f'assets/cases/{cid}/{n:02d}.jpg'] for n in nums]

def brand_case(cid, num, kicker, title, sub, label, head, es, en, rows, sections, hero_n, hero_pos='center', credits=None):
    plates = [hero(f'assets/cases/{cid}/{hero_n:02d}.jpg', f'Caso {num} · {kicker}', title, sub, label, pos=hero_pos),
              statement('El proyecto', head, es, en, rows)]
    for lab, txt, nums in sections:
        plates.append(P('1400/170', band(lab, txt)))
        plates += jrows(_dims(cid, nums))
    plates.append(closing(credits or [('Cliente', kicker), ('Dirección creativa / arte', 'José Carrillo'), ('Rol / agencia / año', TBD)]))
    return plates

CASES['volkswagen'] = dict(light=False, acc='#4fb3ff', plates=brand_case('volkswagen', '14', 'Volkswagen', 'Volkswagen<br>Amarok', 'Fotografía y campaña', 'Automotriz · Campaña',
   'Una pick-up<br>con pedigree.',
   'Fotografía y piezas de campaña para la Amarok V6. Una camioneta de trabajo puesta en el mundo del polo: caballerizas, fardos, tacos y la luz baja del atardecer en la cancha, para la acción del Abierto de Polo. La misma mirada se lleva al barro, al monte y al campo abierto, donde la Amarok vuelve a su terreno. Más piezas de la marca: Camiones Delivery y la plataforma de movilidad VMove.',
   'Photography and campaign pieces for the Amarok V6, set in the world of polo for the Argentine Polo Open, and taken back to mud, woods and open fields.',
   [('Cliente','Volkswagen Argentina'),('País','Argentina'),('Producto','Amarok V6 · Camiones Delivery · VMove'),('Alcance','Fotografía · Campaña · Vía pública'),('Acción','Abierto de Polo'),('Rol','Dirección creativa y de arte'),('Agencia / año','Hogarth · 2022')],
   [('<b>01</b> · Amarok en el Abierto de Polo', 'Caballerizas, fardos y atardecer: la pick-up en un mundo premium.', [7,3,4,9,14]),
    ('<b>02</b> · Fotografía Amarok', 'Barro, monte y campo abierto.', [13,16,6,8,11,5,15,12]),
    ('<b>03</b> · Más Volkswagen', 'Camiones Delivery y la plataforma VMove.', [1,2])],
   hero_n=7, hero_pos='center 60%', credits=[('Cliente','Volkswagen Argentina'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo'),('Año','2022')]))

CASES['corona'] = dict(light=False, acc='#f2c14e', plates=brand_case('corona', '15', 'Corona', 'Corona', 'Espacios de marca · Pilar', 'Experiencia · Espacios',
   'Llevar la playa<br>a Pilar.',
   'Espacios de marca para Corona en Pilar, provincia de Buenos Aires: el parador de Sharewood y el bar del Molino Resto. Arcos de madera tallada, arena, tablas de surf, guirnaldas de luces y fibras naturales que traducen el universo Corona (sol, mar, desconexión) a un lugar donde quedarse toda la tarde.',
   'Brand spaces for Corona in Pilar, Buenos Aires: the Sharewood beach-style hangout and the Molino Resto bar, translating Corona’s sun-and-sea world into places to stay all afternoon.',
   [('Cliente','Corona'),('País','Argentina'),('Lugares','Sharewood Pilar · Molino Resto'),('Alcance','Diseño de espacios · Ambientación · Señalética'),('Rol','Dirección creativa y de arte'),('Agencia / año','Catch · 2023')],
   [('<b>01</b> · Sharewood Pilar', 'Arena, livings y barra al aire libre.', [1,2,3,10]),
    ('<b>02</b> · Molino Resto', 'El bar Corona: madera, luces y mesas largas.', [8,4,5,7,6,9])],
   hero_n=4, hero_pos='center 45%', credits=[('Cliente','Corona'),('Agencia','Catch'),('Dirección creativa y de arte','José Carrillo'),('Año','2023')]))

CASES['brahma'] = dict(light=False, acc='#e30613', plates=brand_case('brahma', '16', 'Brahma', 'Brahma', 'Experiencias de marca', 'Experiencia · BTL',
   'Rojo neón<br>y birra.',
   'Espacios y experiencias para Brahma. De noche, el rojo de la marca se vuelve luz: neones, una jaula para bandas en vivo, barras y un rincón selfie. En Konex, la marca toma la calle con un mural tipográfico de gran escala («Más birra por favor»), la barra de chopp, el puesto de producto y el espacio Brahma Lime.',
   'Brand spaces for Brahma: neon-red night experiences with live-band cages and bars, and a large-scale typographic takeover at Konex with chopp bar and the Brahma Lime area.',
   [('Cliente','Brahma'),('País','Argentina'),('Lugares','Experiencias nocturnas · Ciudad Cultural Konex'),('Alcance','Diseño de espacios · Gráfica · BTL'),('Rol','Dirección creativa y de arte'),('Agencia / año','Catch · 2023')],
   [('<b>01</b> · De noche', 'El rojo Brahma hecho luz: neón, música en vivo y barra.', [4,3,1,6,2,5]),
    ('<b>02</b> · Brahma en Konex', 'Mural tipográfico, chopp y Brahma Lime.', [11,12,7,8,10,9,13])],
   hero_n=4, hero_pos='center 40%', credits=[('Cliente','Brahma'),('Agencia','Catch'),('Dirección creativa y de arte','José Carrillo'),('Año','2023')]))

def prisma_hero():
    return P('1400/880', f"""
<div class="abs" style="background:#231f5c"></div>
<div class="abs" style="left:calc(var(--u)*520);right:calc(var(--u)*64);top:calc(var(--u)*150);bottom:calc(var(--u)*64);border-radius:calc(var(--u)*6);overflow:hidden">
  <img src="assets/cases/prisma/09.jpg" alt="" style="width:100%;height:100%;object-fit:cover">
</div>
<img class="mark" src="assets/logo-white.png" alt="Porra">
<div class="tr lbl" style="color:#fff">Naming · Identidad</div>
<div class="bottom" style="color:#fff;right:auto;max-width:calc(var(--u)*420)">
  <div class="lbl" style="color:#fff;margin-bottom:calc(var(--u)*18)">Caso 17 · Prisma</div>
  <div class="h1" style="font-size:calc(var(--u)*96)">Prisma</div>
  <div class="h3" style="margin-top:calc(var(--u)*20);font-weight:400;color:#fff">Medios de Pago · Una marca nueva para emitir tarjetas</div>
</div>""")

def _prisma():
    plates = [prisma_hero(),
      statement('El brief', 'Emitir tarjetas,<br>100% online.',
       'Prisma necesitaba una marca nueva para lanzar su servicio de procesamiento de tarjetas: que bancos, fintechs y bancos digitales puedan emitir y procesar tarjetas físicas y digitales de forma 100% online, más rápida, flexible y transparente que la tradicional. Planteamos dos caminos. <b>Línea 1, «by Prisma»</b>: apoyarse en la experiencia y la solidez de Prisma (experto, veloz, simple, confiable). <b>Línea 2, marca independiente</b>: crear una categoría nueva, con paleta e imaginario de vanguardia digital (eficiente, innovador, flexible, personalizado).',
       'A new brand for Prisma’s card-processing service, letting banks and fintechs issue physical and digital cards 100% online. Two strategic lines: endorsed “by Prisma” or a fully independent brand.',
       [('Cliente','Prisma Medios de Pago'),('País','Argentina'),('Rubro','Fintech · Pagos'),('Alcance','Estrategia de marca · Naming · Identidad · Moodboards'),('Propuestas','Nuvo · Accel · FastPay · Bamboo'),('Rol','Dirección creativa y de arte'),('Agencia / año','Hogarth · 2022')])]
    for i, (name, txt, a, b) in enumerate([('Nuvo', 'Azul profundo y tipografía redonda: lo nuevo, sin perder confianza.', 1, 2),
                                          ('Accel', 'Velocidad hecha signo: la A como flecha.', 3, 4),
                                          ('FastPay', 'Turquesa y un ícono que es tarjeta y pago a la vez.', 5, 6),
                                          ('Bamboo', 'Verde, orgánico y flexible: crecer rápido.', 7, 8)], 1):
        plates.append(P('1400/170', band(f'<b>{i:02d}</b> · {name}', txt)))
        plates += jrows(_dims('prisma', [a, b]), target=3.4)
    plates.append(closing([('Cliente','Prisma Medios de Pago'),('Agencia','Hogarth'),('Dirección creativa y de arte','José Carrillo'),('Año','2022')]))
    return plates
CASES['prisma'] = dict(light=False, acc='#4f8cff', plates=_prisma())
