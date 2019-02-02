drop schema public cascade;
create schema public;

create type item_type AS ENUM ('man', 'exec', 'package', 'builtin');
create table raw_items (
  id serial primary key,
  type item_type not null,
  ref varchar(255) not null,
  version smallint not null default 0,
  name varchar(255) not null,
  hash varchar(127),
  man_id smallint,
  extra JSON,
  raw bytea,
  primary_text text,
  secondary_text text,
  unique (type, ref, version)
  -- TODO tsv?
);

create table built_items (
  id serial primary key,
  item int not null references raw_items unique,
  uri varchar(255) not null,
  intermediate bytea,
  html text
  -- TODO tsv?
);

create table links (
  from_item int not null references built_items,
  to_item int not null references built_items,
  primary key (from_item, to_item)
);
