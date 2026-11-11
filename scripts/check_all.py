import json
import os
import urllib.request


def probe(name, url, headers=None):
    if not url:
        print(f"SKIP  {name}: not configured")
        return
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"PASS  {name}: HTTP {r.status}")
    except Exception as e:
        print(f"FAIL  {name}: {e}")


probe("OpenRouter models (public)", "https://openrouter.ai/api/v1/models")
key = os.environ.get("OPENROUTER_API_KEY")
probe("OpenRouter key", "https://openrouter.ai/api/v1/key" if key else None, {"Authorization": f"Bearer {key}"} if key else None)
probe("Worker /health", os.environ.get("WORKER_HEALTH_URL"))
probe("Cloady /health", os.environ.get("CLOADY_HEALTH_URL"))
probe("Site (Sakupa)", os.environ.get("SITE_URL"))
su = os.environ.get("SUPABASE_URL")
probe("Supabase REST", f"{su}/rest/v1/health_log?select=id&limit=1" if su else None,
      {"apikey": os.environ.get("SUPABASE_ANON_KEY", ""), "Authorization": f"Bearer {os.environ.get('SUPABASE_ANON_KEY','')}"} if su else None)
