// Porra · Worker: sirve la web (public/) + mini CRM
//   POST /api/lead            → guarda la consulta en D1 y avisa por mail
//   /admin                    → panel privado (login con el secreto ADMIN_PASSWORD, cookie 30 días)
//   /admin/api/leads[/:id]    → API del panel (GET, PATCH, DELETE)
import { EmailMessage } from 'cloudflare:email';

const ETAPAS = ['nuevo', 'contactado', 'reunion', 'propuesta', 'ganado', 'perdido'];

const SCHEMA = `CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  nombre TEXT, email TEXT, empresa TEXT, telefono TEXT,
  tipo TEXT, presupuesto TEXT, mensaje TEXT,
  origen TEXT, pagina TEXT, casos_vistos TEXT, referrer TEXT, pais TEXT, idioma TEXT,
  etapa TEXT DEFAULT 'nuevo', valor_usd REAL, proximo_paso TEXT, fecha_seguimiento TEXT, notas TEXT,
  updated_at TEXT
)`;

let schemaReady = false;
async function db(env) {
  if (!schemaReady) { await env.DB.prepare(SCHEMA).run(); schemaReady = true; }
  return env.DB;
}

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

const clip = (v, n = 2000) => (v == null ? '' : String(v)).trim().slice(0, n);

// ── Acceso al panel: login propio con cookie firmada (HMAC con ADMIN_PASSWORD) ──
const COOKIE = 'porra_crm';
const enc8 = new TextEncoder();
async function sign(env, msg) {
  const key = await crypto.subtle.importKey('raw', enc8.encode('porra-crm:' + env.ADMIN_PASSWORD), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc8.encode(msg));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/[+/=]/g, c => ({ '+': '-', '/': '_', '=': '' }[c]));
}
function safeEq(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
async function authorized(request, env) {
  if (!env.ADMIN_PASSWORD) return false;
  const c = (request.headers.get('cookie') || '').split(/;\s*/).find(x => x.startsWith(COOKIE + '='));
  if (!c) return false;
  const [exp, sig] = c.slice(COOKIE.length + 1).split('.');
  if (!exp || !sig || Number(exp) < Date.now()) return false;
  return safeEq(sig, await sign(env, exp));
}
const loginPage = (error = '', status = 200) => new Response(`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Porra CRM · Ingresar</title>
<style>*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f3f1ec;font:15px/1.4 Inter,system-ui,-apple-system,sans-serif;color:#111}
form{width:min(340px,90vw);background:#fff;border-radius:14px;padding:32px;box-shadow:0 1px 3px rgba(0,0,0,.06)}h1{font-size:18px;margin:0 0 4px}p{margin:0 0 22px;color:#777;font-size:13px}
label{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#888;margin-bottom:6px}input{width:100%;padding:12px 14px;border:1px solid #ddd;border-radius:8px;font:inherit;margin-bottom:16px}
button{width:100%;padding:12px;border:0;border-radius:999px;background:#111;color:#fff;font:inherit;font-weight:600;cursor:pointer}.err{color:#c0392b;font-size:13px;margin:-6px 0 14px}</style></head>
<body><form method="post" action="/admin/login"><h1>Porra CRM</h1><p>Panel privado de consultas</p>
<label for="pw">Contraseña</label><input id="pw" name="password" type="password" autocomplete="current-password" autofocus required>
${error ? `<div class="err">${error}</div>` : ''}<button type="submit">Ingresar</button></form></body></html>`,
  { status, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' } });

async function login(request, env) {
  if (!env.ADMIN_PASSWORD) return loginPage('Falta configurar la contraseña del panel en Cloudflare.', 503);
  let pw = '';
  try { pw = String((await request.formData()).get('password') || ''); } catch {}
  if (!safeEq(await sign(env, 'pw:' + pw), await sign(env, 'pw:' + env.ADMIN_PASSWORD))) {
    await new Promise(r => setTimeout(r, 800));
    return loginPage('Contraseña incorrecta.', 401);
  }
  const exp = String(Date.now() + 30 * 864e5);
  return new Response(null, { status: 303, headers: { location: '/admin', 'cache-control': 'no-store',
    'set-cookie': `${COOKIE}=${exp}.${await sign(env, exp)}; Path=/admin; Max-Age=2592000; HttpOnly; Secure; SameSite=Strict` } });
}
const logout = () => new Response(null, { status: 303, headers: { location: '/admin',
  'set-cookie': `${COOKIE}=; Path=/admin; Max-Age=0; HttpOnly; Secure; SameSite=Strict` } });

async function notify(env, lead, id) {
  if (!env.AVISO) return;
  const from = 'crm@porra.studio', to = env.AVISO_DESTINO || 'porracarrillo@gmail.com';
  const lines = [
    `Nueva consulta #${id} desde porra.studio`, '',
    `Nombre: ${lead.nombre}`, `Email: ${lead.email}`, `Empresa: ${lead.empresa || '-'}`, `Teléfono: ${lead.telefono || '-'}`,
    `Tipo de proyecto: ${lead.tipo || '-'}`, `Presupuesto: ${lead.presupuesto || '-'}`, '', 'Mensaje:', lead.mensaje || '-', '',
    `Casos que miró: ${lead.casos_vistos || '-'}`, `Origen: ${lead.origen || '-'} · País: ${lead.pais || '-'}`, '',
    'Ver en el CRM: https://porra.studio/admin',
  ];
  const subject = `Nueva consulta: ${lead.nombre}${lead.empresa ? ' · ' + lead.empresa : ''}`;
  const enc = s => '=?UTF-8?B?' + btoa(unescape(encodeURIComponent(s))) + '?=';
  const raw = [
    `From: Porra CRM <${from}>`, `To: ${to}`, `Reply-To: ${lead.email}`, `Subject: ${enc(subject)}`,
    `Message-ID: <lead-${id}-${Date.now()}@porra.studio>`, `Date: ${new Date().toUTCString()}`,
    'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8', 'Content-Transfer-Encoding: base64', '',
    btoa(unescape(encodeURIComponent(lines.join('\n')))).replace(/(.{76})/g, '$1\r\n'),
  ].join('\r\n');
  try { await env.AVISO.send(new EmailMessage(from, to, raw)); } catch (e) { console.log('aviso error', e.message); }
}

async function newLead(request, env, ctx) {
  let b;
  try { b = await request.json(); } catch { return json({ ok: false, error: 'Formato inválido' }, 400); }
  if (b.web) return json({ ok: true });                       // honeypot: bots
  const lead = {
    nombre: clip(b.nombre, 120), email: clip(b.email, 160), empresa: clip(b.empresa, 160), telefono: clip(b.telefono, 60),
    tipo: clip(b.tipo, 80), presupuesto: clip(b.presupuesto, 80), mensaje: clip(b.mensaje, 4000),
    origen: clip(b.origen, 300), pagina: clip(b.pagina, 300), casos_vistos: clip(b.casos_vistos, 600),
    referrer: clip(request.headers.get('referer'), 300),
    pais: clip(request.cf && request.cf.country, 8), idioma: clip(request.headers.get('accept-language'), 40),
  };
  if (!lead.nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(lead.email)) return json({ ok: false, error: 'Completá nombre y un mail válido' }, 400);
  const now = new Date().toISOString();
  const r = await (await db(env)).prepare(`INSERT INTO leads (created_at,nombre,email,empresa,telefono,tipo,presupuesto,mensaje,origen,pagina,casos_vistos,referrer,pais,idioma,etapa,updated_at)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'nuevo', ?)`)
    .bind(now, lead.nombre, lead.email, lead.empresa, lead.telefono, lead.tipo, lead.presupuesto, lead.mensaje,
          lead.origen, lead.pagina, lead.casos_vistos, lead.referrer, lead.pais, lead.idioma, now).run();
  const id = r.meta && r.meta.last_row_id;
  ctx.waitUntil(notify(env, lead, id));
  return json({ ok: true, id });
}

async function adminApi(request, env, url) {
  const D = await db(env);
  const m = url.pathname.match(/^\/admin\/api\/leads(?:\/(\d+))?$/);
  if (!m) return json({ error: 'no encontrado' }, 404);
  const id = m[1];
  if (request.method === 'GET' && !id) {
    const { results } = await D.prepare('SELECT * FROM leads ORDER BY created_at DESC LIMIT 1000').all();
    return json({ leads: results, etapas: ETAPAS });
  }
  if (request.method === 'PATCH' && id) {
    const b = await request.json();
    const allowed = ['etapa', 'valor_usd', 'proximo_paso', 'fecha_seguimiento', 'notas', 'empresa', 'telefono', 'nombre', 'email', 'tipo', 'presupuesto'];
    const sets = [], vals = [];
    for (const k of allowed) if (k in b) {
      if (k === 'etapa' && !ETAPAS.includes(b[k])) continue;
      sets.push(`${k}=?`); vals.push(k === 'valor_usd' ? (b[k] === '' || b[k] == null ? null : Number(b[k])) : clip(b[k], 4000));
    }
    if (!sets.length) return json({ ok: false }, 400);
    sets.push('updated_at=?'); vals.push(new Date().toISOString());
    await D.prepare(`UPDATE leads SET ${sets.join(',')} WHERE id=?`).bind(...vals, id).run();
    return json({ ok: true });
  }
  if (request.method === 'DELETE' && id) {
    await D.prepare('DELETE FROM leads WHERE id=?').bind(id).run();
    return json({ ok: true });
  }
  if (request.method === 'POST' && !id) {                    // alta manual desde el panel
    const b = await request.json(); const now = new Date().toISOString();
    const r = await D.prepare(`INSERT INTO leads (created_at,nombre,email,empresa,telefono,tipo,mensaje,origen,etapa,valor_usd,proximo_paso,fecha_seguimiento,notas,updated_at)
       VALUES (?,?,?,?,?,?,?,'manual',?,?,?,?,?,?)`)
      .bind(now, clip(b.nombre, 120), clip(b.email, 160), clip(b.empresa, 160), clip(b.telefono, 60), clip(b.tipo, 80), clip(b.mensaje, 4000),
            ETAPAS.includes(b.etapa) ? b.etapa : 'nuevo', b.valor_usd ? Number(b.valor_usd) : null, clip(b.proximo_paso, 300),
            clip(b.fecha_seguimiento, 20), clip(b.notas, 4000), now).run();
    return json({ ok: true, id: r.meta && r.meta.last_row_id });
  }
  return json({ error: 'método no permitido' }, 405);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    try {
      if (url.pathname === '/api/lead') {
        if (request.method !== 'POST') return json({ error: 'método no permitido' }, 405);
        return await newLead(request, env, ctx);
      }
      if (url.pathname === '/admin' || url.pathname.startsWith('/admin/')) {
        if (url.pathname === '/admin/login' && request.method === 'POST') return await login(request, env);
        if (url.pathname === '/admin/logout') return logout();
        if (!(await authorized(request, env))) {
          if (url.pathname.startsWith('/admin/api/')) return json({ ok: false, error: 'Sesión vencida' }, 401);
          return loginPage();
        }
        if (url.pathname.startsWith('/admin/api/')) return await adminApi(request, env, url);
        const page = await env.ASSETS.fetch(new Request(new URL('/_crm/admin', url), request));
        return new Response(page.body, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' } });
      }
      if (url.pathname.startsWith('/_crm/')) return new Response('No encontrado', { status: 404 });
    } catch (e) {
      return json({ ok: false, error: 'Error del servidor', detail: e.message }, 500);
    }
    return env.ASSETS.fetch(request);
  },
};
