create table if not exists public.health_log (
  id bigint generated always as identity primary key,
  source text not null,
  note text,
  created_at timestamptz not null default now()
);
alter table public.health_log enable row level security;
drop policy if exists health_log_anon_all on public.health_log;
create policy health_log_anon_all on public.health_log
  for all to anon using (true) with check (true);
