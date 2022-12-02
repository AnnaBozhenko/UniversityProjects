select * from author;
select * from content_;
select * from authorcontent;
select * from regioncountry;
select * from user_;
select * from session_;
select * from userinteraction;

select * from country_authors_count;
select * from readable_countries_count;
select * from type_interactions_count;

delete from userinteraction;
delete from session_;
delete from authorcontent;
delete from author;
delete from content_;
delete from user_;
delete from regioncountry;


insert into RegionCountry (region, country)
values('NY', 'US');
insert into RegionCountry (region, country)
values('MG', 'BR');
insert into RegionCountry (region, country)
values('SP', 'BR');
insert into RegionCountry (region, country)
values('BE', 'DE');
insert into RegionCountry (region, country)
values('CDMX', 'MX');

insert into User_ (user_id_, user_geo_origin)
values(-1.03202E+18, 'NY');
insert into User_ (user_id_, user_geo_origin)
values(-8.7634E+18, 'MG');
insert into User_ (user_id_, user_geo_origin)
values(1.90834E+18, 'SP');
insert into User_ (user_id_, user_geo_origin)
values(3.44281E+17, null);
insert into User_ (user_id_, user_geo_origin)
values(3.60919E+18, null);
insert into User_ (user_id_, user_geo_origin)
values(-1.38746E+18, null);

insert into Author (author_id, author_geo_origin) 
values(4.34031E+18, 'NY');
insert into Author (author_id, author_geo_origin) 
values(3.89164E+18, 'BE');
insert into Author (author_id, author_geo_origin) 
values(5.20684E+18, 'MG');
insert into Author (author_id, author_geo_origin) 
values(-1.03202E+18, 'SP');
insert into Author (author_id, author_geo_origin) 
values(4.67027E+18, 'CDMX');

insert into Content_ (content_id, content_url)
values(8.89072E+18, 'http://www.nytimes.com/2016/03/28/business/dealbook/ethereum-a-virtual-currency-enables-transactions-that-rival-bitcoins.html');
insert into Content_ (content_id, content_url)
values(3.10515E+17, 'http://www.coindesk.com/ieee-blockchain-oxford-cloud-computing/');
insert into Content_ (content_id, content_url)
values(3.46003E+18, 'http://cointelegraph.com/news/bitcoin-future-when-gbpcoin-of-branson-wins-over-usdcoin-of-trump');
insert into Content_ (content_id, content_url)
values(-8.14243E+18, 'https://cloudplatform.googleblog.com/2016/03/Google-Data-Center-360-Tour.html');
insert into Content_ (content_id, content_url)
values(-4.20535E+18, 'https://bitcoinmagazine.com/articles/ibm-wants-to-evolve-the-internet-with-blockchain-technology-1459189322');

insert into AuthorContent (author_id, content_id)
values(4.34031E+18, 8.89072E+18);
insert into AuthorContent (author_id, content_id)
values(3.89164E+18, 3.10515E+17);
insert into AuthorContent (author_id, content_id)
values(5.20684E+18, 3.46003E+18);
insert into AuthorContent (author_id, content_id)
values(-1.03202E+18, -8.14243E+18);
insert into AuthorContent (author_id, content_id)
values(4.67027E+18, -4.20535E+18);

insert into Session_ (session_id, session_agent)
values(3.62174E+18, '(Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.24 Safari/537.36');
insert into Session_ (session_id, session_agent)
values(1.39579E+18, '(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36');
insert into Session_ (session_id, session_agent)
values(9.12188E+18, '(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36');
insert into Session_ (session_id, session_agent)
values(-3.16764E+18, null);
insert into Session_ (session_id, session_agent)
values(1.14321E+18, null);
insert into Session_ (session_id, session_agent)
values(5.11149E+18, null);

insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values (-1.03202E+18, 8.89072E+18, 3.62174E+18, 'VIEW', 1465412560);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(-8.7634E+18, 3.10515E+17, 1.39579E+18, 'VIEW', 1465413742);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(1.90834E+18, 3.46003E+18, 9.12188E+18, 'VIEW', 1465415228);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(3.44281E+17, 3.10515E+17, -3.16764E+18, 'FOLLOW', 1465413895);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(3.60919E+18, 3.10515E+17, 1.14321E+18, 'BOOKMARK', 1465413879);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(1.90834E+18, -8.14243E+18, 9.12188E+18, 'LIKE', 1465415756);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(3.60919E+18, 3.10515E+17, 1.14321E+18, 'LIKE', 1465413867);
insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_)
values(-1.38746E+18, -4.20535E+18, 5.11149E+18, 'COMMENT CREATED', 1466034895);