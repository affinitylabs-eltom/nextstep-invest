create table if not exists heyreach_events (
  id uuid default gen_random_uuid() primary key,
  event_type text not null,
  lead_name text,
  lead_linkedin text,
  campaign_name text,
  campaign_id integer,
  message_text text,
  raw_payload jsonb,
  created_at timestamptz default now()
);

create index idx_heyreach_events_type on heyreach_events(event_type);
create index idx_heyreach_events_lead on heyreach_events(lead_linkedin);
create index idx_heyreach_events_created on heyreach_events(created_at);

alter table heyreach_events enable row level security;

create policy "Allow anonymous inserts" on heyreach_events
  for insert with check (true);

create policy "Allow reads" on heyreach_events
  for select using (true);
