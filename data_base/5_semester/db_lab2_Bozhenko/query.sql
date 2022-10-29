-- 1 Скільки якого виду взаємодій користувачів виявлено?
select 
    event_type,
    count(*) as event_number
from userinteraction
group by event_type
order by count(*) desc

-- 2 Скільки авторів є в кожній країні?
(select 
    country,
    count(*) as authors_numb 
from regioncountry
join author on region = author_geo_origin
group by country)
union
(select 
    country, 
    coalesce(null, 0) as authors_numb
from regioncountry
where region not in (select author_geo_origin from author))
order by authors_numb desc;

-- 3 Яка кількість переглядів контенту, створеного авторами з кожної країни?
select
    country,
    count(*) as views_number
from userinteraction
join authorcontent using(content_id)
join author using(author_id)
join regioncountry on region = author_geo_origin
where event_type = 'VIEW'
group by country;
