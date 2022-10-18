-- 1	Вивести vend_id, vend_name постачальників, 
-- що постачають товари та prod_id відповідних товарів.
select
    vend_id,
    vend_name,
    prod_id
from vendors
inner join products using(vend_id)

-- 2	Вивести vend_id, vend_name усіх постачальників 
-- та prod_id товарів, які вони постачають.
select 
    vend_id,
    vend_name,
    prod_id
from vendors
left join products using(vend_id)

-- 3	Вивести vend_id, vend_name постачальників, що не постачають товари.
select 
    vend_id,
    vend_name
from vendors
left join products using(vend_id)
where prod_id is null

-- 4	Вивести vend_id, vend_name та кількість товарів, 
-- яку пропонує кожен з постачальників. Поля у відповіді 
-- позначити vend_id, vend_name, num_prods.
select 
    vend_id,
    vend_name,
    count(prod_id) as num_prods
from vendors
inner join products using(vend_id)
group by vend_id

-- 5	Виконати запит 4, відповідь впорядкувати за полем vend_name.
select 
    vend_id,
    vend_name,
    count(prod_id) as num_prods
from vendors
inner join products using(vend_id)
group by vend_id
order by vend_name

-- 6	Вивести vend_name та кількість товарів, яку пропонує кожен 
-- з постачальників, якщо ця кількість більше 2. Поля у відповіді 
-- позначити vend_name, num_prods. Відповідь впорядкувати за полем vend_name.
select 
    vend_name,
    count(prod_id) as num_prods
from vendors
inner join products using(vend_id)
group by vend_id
having count(prod_id) > 2

-- 7	Вивести cust_id, cust_name покупців, що купували товари, та номери їх замовлень
select 
    cust_id,
    cust_name,
    order_num
from customers
inner join orders using(cust_id)

-- 8	Вивести cust_id, cust_name усіх покупців та номери відповідних замовлень
select 
    cust_id,
    cust_name,
    order_num
from customers
left join orders using(cust_id)

-- 9	Вивести cust_id, cust_name покупців, що не мають замовлень
select 
    cust_id,
    cust_name
from customers
left join orders using(cust_id)
where order_num is null

-- 10	Вивести cust_id, cust_name та кількість замовлень кожного покупця.
select 
    cust_id,
    cust_name,
    count(order_num) as orders_number
from customers
left join orders using(cust_id)
group by cust_id

-- 11	Виконати запит 10, відповідь впорядкувати за полем cust_name.
select 
    cust_id,
    cust_name,
    count(order_num) as orders_number
from customers
left join orders using(cust_id)
group by cust_id
order by cust_name

-- 12	Вивести cust_id, cust_name покупців, що мають рівно 1 замовлення.
--  Відповідь впорядкувати за полем cust_name.
select 
    cust_id,
    cust_name
from customers
left join orders using(cust_id)
group by cust_id
having count(order_num) = 1
order by cust_name

-- 13	Вивести cust_id, cust_name усіх покупців та кількість і ціну товарів, які вони замовляли.
select 
    cust_id,
    cust_name,
    quantity,
    item_price
from customers
left join orders using(cust_id)
inner join orderitems using (order_num)
order by cust_id

-- 14	Вивести cust_id, cust_name усіх покупців та на яку загальну суму 
-- вони замовили товарів. Поля у відповіді позначити cust_id, cust_name, total.
select 
    cust_id,
    cust_name,
    sum(quantity * item_price) as total
from customers
left join orders using(cust_id)
inner join orderitems using(order_num)
group by cust_id

-- 15	Виконати запит 14. Відповідь впорядкувати за cust_name. 
select 
    cust_id,
    cust_name,
    sum(quantity * item_price) as total
from customers
left join orders using(cust_id)
inner join orderitems using (order_num)
group by cust_id
order by cust_name

-- 16	На основі запиту 14 вивести лише тих покупців, які замовили 
-- товарів на суму більшу, ніж $3000. Позначити поле cust_name як vip_client. 
select 
    cust_id,
    cust_name as vip_client,
    sum(quantity * item_price) as total
from customers
left join orders using(cust_id)
inner join orderitems using (order_num)
group by cust_id
having sum(quantity * item_price) > 3000

-- 17	На основі запиту 14 вивести тих покупців, які замовили товарів 
-- на суму меншу, ніж $1000. Позначити поле cust_name як common_client. 
select 
    cust_id,
    cust_name as common_client,
    sum(quantity * item_price) as total
from customers
left join orders using(cust_id)
inner join orderitems using (order_num)
group by cust_id
having sum(quantity * item_price) < 1000

-- 18	Виконати запит 17. Відповідь впорядкувати за загальною сумою.
select 
    cust_id,
    cust_name as common_client,
    sum(quantity * item_price) as total
from customers
left join orders using(cust_id)
inner join orderitems using (order_num)
group by cust_id
having sum(quantity * item_price) < 1000
order by sum(quantity * item_price)
