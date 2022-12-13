-- Опис процедури: повідомлення про вид користувацької взаємодії та його кількість для даного контенту
create or replace procedure watch_interactions (content_id_arg bigint) 
language 'plpgsql'
as $$
declare 
    interaction_type userinteraction.event_type%type;
    interaction_number bigint;
    interaction_cursor cursor(content_id_arg bigint) for
    (select 
        event_type,
        count(*)
        from userinteraction 
        where content_id = content_id_arg
        group by event_type);
BEGIN
    open interaction_cursor(content_id_arg);
    fetch interaction_cursor into interaction_type, interaction_number;
    if not found then
        raise notice 'No interactions were found.';
    else  
        loop 
            raise notice '%s: % interaction(s)', trim(interaction_type), interaction_number;
            fetch interaction_cursor into interaction_type, interaction_number;
            exit when not found;
        end loop;
    end if;
end;
$$

-- Приклади використання
-- Call watch_interactions (310515000000000000);
-- Call watch_interactions (-4765711818183276269);
-- Call watch_interactions (-8085935119790093311);