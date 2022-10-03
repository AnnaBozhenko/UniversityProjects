create table person (
	person_id int not null,
	person_name char(50) not null,
	person_gender char(5) check (person_gender = 'woman' or person_gender = 'man') not null,
	person_birth_date date not null
);

	
create table author (
	author_id int not null,
	author_name char(50),
	author_email char(100),
	person_id int not null
);


create table coursebook (
	cb_ISBN bigint not null,
	cb_title char[100] not null,
	cb_publish_date date not null,
	cb_publisher char(50) not null,
	cb_knowledge_area char(100) not null,
	cb_pages_number int not null
);


create table author_coursebook (
	cb_ISBN bigint unique not null,
	author_id int unique not null,
	edition int,
	circulation int
);

-- defining primary keys
alter table person
	add constraint pk_person primary key (person_id);
	
alter table author 
	add constraint pk_author primary key (author_id);
	
alter table coursebook
	add constraint pk_coursebook primary key (cb_ISBN);
	
-- defining foreign keys
alter table author
	add constraint fk_author_person 
	foreign key (person_id) 
	references person (person_id) on update cascade on delete cascade;

alter table author_coursebook
	add constraint fk_author_coursebook 
	foreign key (author_id) 
	references author (author_id) on update cascade on delete cascade;

alter table author_coursebook
	add constraint fk_coursebook_author 
	foreign key (cb_ISBN) 
	references coursebook (cb_ISBN) on update cascade on delete cascade;
