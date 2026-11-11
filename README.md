# free-stack-test-station

Empty end-to-end test station built from free tiers of ten platforms. Each item is verified individually before being chained.

- `worker/` — Cloudflare Workers gateway (only public entry point): /health, /api/chat, /api/db-check
- `supabase/` — Supabase schema and connection notes (publishable key only)
- `services/health/` — minimal health service for Cloady
- `gpu/`, `notebooks/` — GPU probe script shared by Kaggle and Colab (offline batch only)
- `site/` — static site for Sakupa preview
- `.github/workflows/` — Supabase keepalive (every 5 days), daily healthcheck, manual GPU script validation
- `scripts/check_all.py` — local chain checker (unconfigured items report SKIP, never PASS)
- `STATUS.md` — verified progress log

Architecture and per-item test gates live in the project plan kept with the operator.
