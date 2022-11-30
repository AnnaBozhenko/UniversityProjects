-- Цикли
-- 1.1 Створити таблицю OrdersCopy як копію таблиці Orders. Видалити всі записи з таблиці OrdersCopy. 

create table OrdersCopy 
as select * from Orders;

select * from orderscopy;

delete from orderscopy;


-- 1.2 Заповнити в циклі таблицю OrdersCopy: поле order_num - значеннями 30001 .. 30020, 
-- поле cust_id - значеннями cust_101 .. cust_120, поле order_date - датами: сьогоднішньою, вчорашньою, ... 19 днів тому. 
DO $$
    DECLARE
        order_id   orderscopy.order_num%TYPE;
        customer_id orderscopy.cust_id%TYPE;

    BEGIN
        order_id := 30000;
        customer_id := 'cust_';
        FOR counter IN 1..20
            LOOP
                INSERT INTO orderscopy (order_num, cust_id, order_date)
                VALUES (counter + order_id, customer_id || 100+counter, current_date - counter + 1);
            END LOOP;
    END;
$$
LANGUAGE plpgsql;

-- 1.3 Видалити таблицю OrdersCopy.

drop table orderscopy;

-- Курсори
-- 2.1 Визначити курсор CustCursor  як  "Всі покупці, що НЕ мають e-mail".
do $$
	declare CustCursor cursor FOR
		select 
			cust_name
		from customers
		where cust_email is null;
	BEGIN
	end;
$$

-- 2.2 Вивести перший рядок курсору CustCursor в змінну CustRecord. Закрити курсор.
do $$
	declare 
		CustRecord customers.cust_name%type; 
		CustCursor cursor FOR
		select 
			cust_name
		from customers
		where cust_email is null;
	
	BEGIN
	    open CustCursor;
	    fetch next from CustCursor into CustRecord;
        raise notice 'Customer without email: %', CustRecord;
	    close CustCursor;
	end;
$$

-- 2.3 Вивести в циклі всі рядки з курсору CustCursor в змінну CustRecord.
do $$
	declare 
		CustRecord customers.cust_name%type; 
		CustCursor cursor FOR
		select 
			cust_name
		from customers
		where cust_email is null;
	
	begin
		open CustCursor;
		loop
			fetch next from CustCursor into CustRecord;
			exit when not found;
			raise notice 'Customer without email: %', CustRecord;
		end loop;
		close CustCursor;
	end;
$$

