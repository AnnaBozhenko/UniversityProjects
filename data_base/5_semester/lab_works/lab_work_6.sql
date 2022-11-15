select * from customers
-- Додати в таблицю Customers новий рядок: ('1000000006', 'Toy Land', '123 Any Street', 'New York', 'NY' , '11111', 'USA' , NULL, NULL). Переконатися, що дані додалися.
insert into customers values ('1000000006', 'Toy Land', '123 Any Street', 'New York', 'NY' , '11111', 'USA' , NULL)

-- Те саме що й в 1, але явно задати імена стовпчиків, в які вставляються дані. 
-- (попередньо видалити рядок, який був створений в п. 1:  DELETE FROM Customers WHERE cust_id = '1000000006';)
insert into customers (cust_id, cust_name, cust_email) values('1000000006', 'Toy Land', 'xxx@gmail.com')

-- Те саме, що й в 1, але ввести поля в іншому порядку. 
insert into customers (cust_name, cust_id, cust_email) values( 'yyy', '1000000007', 'yyy@gmail.com')

-- Те саме, що й в 1, але ввести частину даних, наприклад, без двох останніх полів.
insert into customers (cust_name, cust_id, cust_email) values( 'yyy', '1000000007', 'yyy@gmail.com')

-- Створити нову таблицю з іменем CustCopy за допомогою оператора: 
-- SELECT * INTO CustCopy FROM Customers. Переконатися, що таблиця CustCopy створена.
select * INTO CustCopy FROM Customers
select * from custcopy

-- Створити нову таблицю з іменем CustCopy за допомогою оператора:
--  CREATE TABLE CustCopy AS SELECT * FROM Customers. Переконатися, що таблиця CustCopy створена.
CREATE TABLE CustCopy AS SELECT * FROM Customers

-- Видалити таблицю CustCopy за допомогою оператора DROP TABLE CustCopy
drop table custcopy

-- Оновлення і видалення даних 
-- Для покупця з cust_id = '1000000005' змінити e-mail на 'kim@thetoystore.com'
update customers set cust_email = 'kim@thetoystore.com' where cust_id = '1000000005'

-- Для покупця з cust_id = '1000000006' змінити поле cust_contact на Sam Roberts, 
-- а поле cust_email на 'sam@toyland.com'
update customers set cust_contact = 'Sam Roberts', cust_email = 'sam@toyland.com' where cust_id = '1000000006' 

-- Для покупця з cust_id = '1000000005' змінити поле cust_email на NULL
update customers set  cust_email = null where cust_id = '1000000005' 

-- Видалити покупця з cust_id = '1000000006'
delete from customers 
    where cust_id = '1000000006'

-- Виконати 5, після чого видалити всі рядки з таблиці CustCopy
delete from custcopy

-- Видалити таблицю CustCopy
drop table custcopy

-- Додавання і видалення полів 

-- Додати в таблицю Vendors поле vend_phone, що має тип char(20). 
-- Переконатися, що поле присутнє
alter table vendors add vend_phone char(20)

select * from vendors
-- Видалити з таблиці Vendors поле vend_phone
alter table vendors drop column vend_phone

-- Додати в таблицю Orders поля cur_date, cur_time
alter table orders add cur_date date, add cur_time time

-- alter table orders drop column cur_date;
-- alter table orders drop column cur_time
-- select * from orders

-- Для всіх рядків таблиці Orders заповнити поле cur_date поточною датою, cur_time - поточним часом
update orders set cur_date = current_date, cur_time = current_time


-- Використання зрізів (VIEW)
-- Створити VIEW ProductCustomers: (cust_name, cust_contact, prod_id) 
-- з інформацією про тих покупців, що купували товари
create view products_customers as
select 
    cust_name,
    cust_contact, 
    prod_id
from customers 
    join orders using(cust_id)
    join orderitems using(order_num)


select * from products_customers

-- Користуючись VIEW ProductCustomers вивести тих покупців, що купували товар з prod_id = 'RGAN01'
select * from products_customers 
where prod_id = 'RGAN01'

-- Створити VIEW VendorLocations, в якому міститься наступна інформація: 
-- vend_name, vend_country. 
-- Вивести всі рядки з VendorLocations 
create view VendorLocations as 
select 
    vend_name,
    vend_country
from vendors

select * from vendorlocations


-- Створити VIEW OrderItemsExpanded, в якому міститься наступна інформація: 
-- order_num, …, expanded_price. Вивести всі рядки з OrderItemExpanded
create view orderitemsexpanded as 
SELECT
    order_num,
    order_item,
    prod_id,
    quantity,
    item_price,
    quantity*item_price as expanded_price
from orderitems

select * from orderitemsexpanded
