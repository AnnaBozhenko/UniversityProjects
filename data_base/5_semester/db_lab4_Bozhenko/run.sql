-- Приклад виконання функції

select get_authors_numb_from('US');
select get_authors_numb_from('BR');
select get_authors_numb_from('AU');

-- Приклад виконання процедури

Call watch_interactions (310515000000000000);
Call watch_interactions (-4765711818183276269);
Call watch_interactions (-8085935119790093311);

-- Приклад запуску тригера

delete from content_ where content_id = -8142430000000000000;

select * from userinteraction where content_id = -8142430000000000000;
select * from authorcontent where content_id = -8142430000000000000

-- insert into content_ (content_id, content_url)
-- values (-8142430000000000000, 'https://cloudplatform.googleblog.com/2016/03/Google-Data-Center-360-Tour.html');

-- insert into authorcontent (author_id, content_id)
-- values (-1032020000000000000, -8142430000000000000);

-- insert into userinteraction (user_id_, content_id, session_id, event_type, timestamp_)
-- values (1908340000000000000, -8142430000000000000, 9121880000000000000, 'LIKE', 1465415756);
