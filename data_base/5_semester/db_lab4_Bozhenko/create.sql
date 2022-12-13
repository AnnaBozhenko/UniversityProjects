create table User_ (
	user_id_ bigint not null,
	user_geo_origin char(50)
);

create table RegionCountry (
	region char(50) not null,
	country char(50) not null
);

create table Content_ (
	content_id bigint not null,
	content_url char(200)
);

create table Session_ (
	session_id bigint not null,
	session_agent char(200)
);

create table UserInteraction (
	user_id_ bigint not null,
	content_id bigint not null,
	session_id bigint not null,
	event_type char(50) not null,
	timestamp_ bigint
);

create table Author (
	author_id bigint not null,
	author_geo_origin char(50)
);

create table AuthorContent (
	author_id bigint not null,
	content_id bigint not null
);

-- primary keys declaration
alter table User_
	add constraint pk_user primary key (user_id_);
alter table RegionCountry
	add constraint pk_region_country primary key (region);
alter table Content_ 
	add constraint pk_content primary key (content_id);
alter table Session_
	add constraint pk_session primary key (session_id);
alter table UserInteraction
	add constraint pk_user_interaction primary key (user_id_, content_id, session_id, event_type);
alter table Author 
	add constraint pk_author primary key (author_id);
alter table AuthorContent 
	add constraint pk_author_content primary key (author_id, content_id);


-- foreign keys declaration
alter table User_
	add constraint fk_user_origin 
	foreign key (user_geo_origin) references RegionCountry (region);
	
alter table Author
	add constraint fk_author
	foreign key (author_geo_origin) references RegionCountry (region);
	
alter table UserInteraction
	add constraint fk_user
	foreign key (user_id_) references User_ (user_id_);

alter table UserInteraction
	add constraint fk_content 
	foreign key (content_id) references Content_ (content_id);

alter table UserInteraction
	add constraint fk_session 
	foreign key (session_id) references Session_ (session_id);

alter table AuthorContent
	add constraint fk_author 
	foreign key (author_id) references Author (author_id);

alter table AuthorContent
	add constraint fk_content 
	foreign key (content_id) references Content_ (content_id);

-- drop table if exists author CASCADE;
-- drop table if exists user_ CASCADE;
-- drop table if exists authorcontent CASCADE;
-- drop table if exists content_ CASCADE;
-- drop table if exists regioncountry CASCADE;
-- drop table if exists session_ CASCADE;
-- drop table if exists userinteraction cascade;