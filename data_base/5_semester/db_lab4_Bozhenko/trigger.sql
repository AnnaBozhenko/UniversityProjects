-- Опис тригеру: перед видаленням запису певного контенту з таблиці Content_ видалити 
-- всі записи, пов'язані з цим контентом в таблицях AuthorContent, UserInteraction
create function delete_everywhere()
returns trigger
language 'plpgsql'
as $$
declare 
    content_id_to_delete bigint;
begin 
    content_id_to_delete := Old.content_id;
    delete from authorcontent where content_id = content_id_to_delete;

    delete from userinteraction where content_id = content_id_to_delete;
    return Old;
end;
$$

create trigger clean_content_data
before delete
on content_
for each row
execute procedure delete_everywhere();

-- Приклад виконання
-- delete from content_ where content_id = -8142430000000000000

-- insert into content_ (content_id, content_url)
-- values (-8142430000000000000, 'https://cloudplatform.googleblog.com/2016/03/Google-Data-Center-360-Tour.html');

-- insert into authorcontent (author_id, content_id)
-- values (-1032020000000000000, -8142430000000000000);

-- insert into userinteraction (user_id_, content_id, session_id, event_type, timestamp_)
-- values (1908340000000000000, -8142430000000000000, 9121880000000000000, 'LIKE', 1465415756);
