// Porra · Worker: sirve la web (public/) + mini CRM
//   POST /api/lead            → guarda la consulta en D1 y avisa por mail
//   /admin                    → panel privado (usuario: porra · clave: secreto ADMIN_PASSWORD)
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

function authorized(request, env) {
  if (!env.ADMIN_PASSWORD) return false;
  const h = request.headers.get('authorization') || '';
  if (!h.startsWith('Basic ')) return false;
  try {
    const [user, pass] = atob(h.slice(6)).split(':');
    return user === 'porra' && pass === env.ADMIN_PASSWORD;
  } catch { return false; }
}
const askAuth = () => new Response('Acceso restringido', {
  status: 401, headers: { 'www-authenticate': 'Basic realm="Porra CRM", charset="UTF-8"' } });

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
        if (!authorized(request, env)) return askAuth();
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
