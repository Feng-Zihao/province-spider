

create table url_pool(
	url string primary key,
	level integer,
	scanned boolean,
	code string,
	name string
);

create table district(
	code string primary key,
	name string,
	level integer,
	parent_code string,
	parent_name string,
	page_url string,
	href string,
	class_code string
);
