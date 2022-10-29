-- Варіант 4, 2c) Вивести PROD_ID товарів та імена постачальників для тих товарів, 
-- які були продані. Результат вивести у верхньому регістрі, 
-- як єдине поле products_sold.

select distinct
	upper(products.prod_id || ' - ' || vendors.vend_name) as products_sold
from orderitems 
    join products using(prod_id)
	join vendors using(vend_id)

-- Варіант 6, 2a) Скільки продано найдешевшого товару?

select 
    orderitems.prod_id,
    sum(orderitems.quantity)
from orderitems
    join products using(prod_id)
where prod_price = (select min(prod_price) from products)
group by orderitems.prod_id


-- Варіант 6, 2c) Вивести ім’я та пошту покупця, як єдине поле client_name, для тих 
-- покупців, що не мають замовлень. Результат вивести у нижньому регістрі.

select 
    lower(cust_name || ' - ' || coalesce(cust_email, '')) as client_name
from customers left join orders using(cust_id)
where orders.cust_id is null
