
create table users (
	user_id serial primary key,
	username text not null,
	password text not null,
	last_login timestamp default current_timestamp
);
create table finite_automata (
	fa_id serial primary key,
	name text not null,
	type text check ( type in ('DFA', 'NFA', 'Unknown')),
	states text[],
	alphabet text[],
	start_state text,
	final_states text[],
	user_id integer references users(user_id) on delete cascade
);
create table transitions (
	t_id serial primary key,
	fa_id integer references finite_automata(fa_id) on delete cascade,
	from_state text,
	input_symbol text,
	to_states text[]
);

select * from finite_automata;
select * from transitions;
