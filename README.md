# Porra — web portfolio

Sitio de José Fernando Carrillo · Director creativo IA · **https://porra.studio**
Es una web estática: no necesita servidor ni base de datos. Se publica gratis en Cloudflare con el dominio porra.studio.

---

## Qué hay en esta carpeta

```
porra-web/
├── content/          ← LOS TEXTOS. Esto es lo que vas a editar.
│   ├── home.json        dominio, orden de casos, tarjetas del home, reels
│   └── casos-ia.json    textos de los casos IA (Up Sí Vale, Totis, Santo's, etc.)
├── public/           ← LA WEB TERMINADA (lo que se publica)
│   ├── index.html       se genera solo: no lo edites a mano
│   └── assets/          imágenes, videos, logos, tipografías
└── src/              ← el motor (plantilla, diseño de placas, armado)
    ├── build.py         arma public/index.html a partir de content/
    ├── cases.py         casos de marca (Lollapalooza, VUSE, NAS, Camel, La Nación, OXXO) y placas
    ├── plantilla.html   estructura y estilos de la página
    └── plates.css       estilos de las placas (sirven también para Behance)
```

---

## Puesta en línea (una sola vez)

### 1. Comprar el dominio
La forma más simple es comprarlo directo en **Cloudflare** (Domain Registration → Register Domains): queda conectado a la web sin configurar nada más. Si ya lo tenés en otro lado (GoDaddy, NIC Argentina para .com.ar, etc.), también sirve: en el paso 4 Cloudflare te dice qué registros cambiar.

### 2. Subir esta carpeta a GitHub
1. Creá una cuenta gratis en github.com.
2. Creá un repositorio nuevo, por ejemplo `porra-web` (puede ser **privado**).
3. Para subir la carpeta, lo más fácil es **GitHub Desktop** (app gratuita): *File → Add local repository* → elegís esta carpeta → como todavía no es un repositorio, la app te ofrece *create a repository* → aceptás → *Publish repository*.
   La subida por el navegador tiene límite de 100 archivos por vez; esta carpeta tiene más, por eso conviene la app.

> Alternativa: creá el repositorio vacío y conectá GitHub en Claude. Claude puede subir todo directamente y, de ahí en más, hacer los cambios en el repositorio.

### 3. Publicación en Cloudflare (ya hecho)
El proyecto **porra-web** está en Cloudflare → *Compute → Workers & Pages*, conectado a este repositorio:
- **Build command:** `python3 src/build.py`
- **Deploy command:** `npx wrangler deploy` (usa `wrangler.jsonc`, que publica la carpeta `public`)
- Dirección técnica: `porra-web.porracarrillo.workers.dev`

### 4. Dominio (ya hecho)
`porra.studio` y `www.porra.studio` están conectados en la pestaña **Domains** del proyecto.

### 5. Avisarle a la web cuál es su dominio
En `content/home.json`, cambiá la primera línea:
```json
"dominio": "https://tudominio.com",
```
Sirve para que al compartir el link en WhatsApp, LinkedIn, etc. aparezca la imagen de vista previa.

---

## Cómo editar

**Cada vez que se guarda un cambio en GitHub, Cloudflare vuelve a armar y publicar la web sola (≈1 minuto).**

### Cambios chicos (vos mismo, desde el navegador)
En github.com, abrí `content/home.json` o `content/casos-ia.json` → ícono del lápiz (*Edit*) → cambiás el texto → *Commit changes*.

Ejemplos:
- Completar un dato: buscá `[a confirmar]` y reemplazalo por el dato real. Lo que quede como `[a confirmar]` se ve marcado en la web.
- Cambiar el orden de los casos: reordená la lista `orden_de_casos`.
- Cambiar el orden de la galería del home: reordená los bloques dentro de `tarjetas_home`.
- Corregir un título, una bajada o una descripción de tarjeta.

Reglas para no romper nada:
- Respetá las comillas `"…"` y las comas entre elementos.
- `<br>` dentro de un texto es un salto de línea en el titular.
- Si algo queda mal escrito, Cloudflare no publica el cambio y la web sigue como estaba. En *Deployments* vas a ver el error, en castellano (por ejemplo: `no encuentro el archivo …`).

### Cambios grandes (con Claude)
Casos nuevos, imágenes nuevas, diseño, placas para Behance, videos: pedíselo a Claude en el proyecto PORRA_IA. Si el repositorio está conectado, Claude hace el cambio y lo sube; si no, te devuelve la carpeta actualizada.

### Probar en tu compu antes de subir (opcional)
Con Python instalado, desde esta carpeta:
```
python3 src/build.py
python3 -m http.server 8000 --directory public
```
y abrís http://localhost:8000

---

## Videos en calidad original

Cloudflare Pages acepta archivos de hasta 25 MB, por eso los reels de `public/assets/reels/` están comprimidos (1080p, ~2 Mbps). Para mostrarlos en calidad original, el paso siguiente es subirlos a **Vimeo** (sin marca de agua desde el plan pago) o a **Cloudflare R2**, y cambiar en `content/home.json` la ruta del video por el link. Pedíselo a Claude cuando lo tengas.

---

## Antes de lanzar
- [ ] Completar los `[a confirmar]` (roles, años, resultados).
- [ ] Confirmar que podés usar los logos de clientes del loop (Coca-Cola, VUSE, Volkswagen, Netflix, La Nación, Volvo, KFC, Shell).
- [ ] Revisar la web en el celular.
