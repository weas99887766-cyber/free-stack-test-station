export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/health') {
      const checks = {
        worker: 'ok',
        openrouter: env.OPENROUTER_API_KEY ? 'configured' : 'not_configured',
        supabase: env.SUPABASE_URL ? 'configured' : 'not_configured',
        r2: env.TEST_BUCKET ? 'configured' : 'not_configured',
      };
      return Response.json({ ok: true, ts: new Date().toISOString(), checks });
    }
    if (url.pathname === '/api/chat' && request.method === 'POST') {
      if (!env.OPENROUTER_API_KEY) return Response.json({ error: 'openrouter_not_configured' }, { status: 501 });
      const body = await request.json().catch(() => ({}));
      const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.OPENROUTER_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: body.model || 'openrouter/free', messages: body.messages || [{ role: 'user', content: 'ping' }] }),
      });
      return new Response(await r.text(), { status: r.status, headers: { 'Content-Type': 'application/json' } });
    }
    if (url.pathname === '/api/db-check') {
      if (!env.SUPABASE_URL || !env.SUPABASE_ANON_KEY) return Response.json({ error: 'supabase_not_configured' }, { status: 501 });
      const r = await fetch(`${env.SUPABASE_URL}/rest/v1/health_log?select=id&limit=1`, {
        headers: { apikey: env.SUPABASE_ANON_KEY, Authorization: `Bearer ${env.SUPABASE_ANON_KEY}` },
      });
      return Response.json({ supabase_status: r.status });
    }
    return new Response('not found', { status: 404 });
  },
};
