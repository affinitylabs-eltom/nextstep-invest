create table if not exists visitor_tracking (
  id uuid default gen_random_uuid() primary key,
  ref text not null,
  event text not null,
  page_url text,
  referrer text,
  user_agent text,
  scroll_depth integer,
  time_on_page integer,
  password_entered boolean default false,
  created_at timestamptz default now()
);

create index if not exists idx_visitor_tracking_ref on visitor_tracking(ref);
create index if not exists idx_visitor_tracking_created on visitor_tracking(created_at);

alter table visitor_tracking enable row level security;

create policy "Allow anonymous inserts" on visitor_tracking
  for insert with check (true);

create policy "Allow service role select" on visitor_tracking
  for select using (true);
