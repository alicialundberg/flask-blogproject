drop table if exists posts;
create table posts (
  id integer primary key not null,
  title text not null,
  post text not null,
  author text not null
);
