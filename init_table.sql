

create table url_pool(
	url string primary key,
	scanned boolean
);

create table district(
	code string primary key,
	level integer,
	name string,
	page_url string,
	href string,
	class_code string
);
