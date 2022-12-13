-- Опис функції: знаходження кількості авторів з даної країни
create or replace function get_authors_numb_from(country_name character(50))
returns integer
language 'plpgsql'
as $$
BEGIN
    return (select count(*) 
                from author join regioncountry on author_geo_origin = region
                where country = country_name);
end;
$$

-- Приклади використання
-- select get_authors_numb_from('US');
-- select get_authors_numb_from('BR');
-- select get_authors_numb_from('AU');
