-- 1  Вивести prod_id всіх товарів, які пропонує постачальник DLL01.

-- select 
--   prod_id 
--   from products
-- where vend_id = 'DLL01'

-- 2  Вивести кількість товарів, які пропонує постачальник DLL01. Відповідь позначити як num_prods.

-- select 
--   count(prod_id) as num_prods
--   from products
-- where vend_id = 'DLL01'

-- 3  Вивести кількість товарів, які пропонує кожен з постачальників. 
-- Поля у відповіді позначити vend_id, num_prods.

-- select 
--   vend_id, 
--   count(*) as num_prods
--   from products
-- group by vend_id

-- 4  На основі таблиці orders вивести cust_id та кількість замовлень кожного покупця. 
-- Поля у відповіді позначити cust_id, num_orders.

-- select 
--   cust_id,
--   count(*) as num_orders
--   from orders
-- group by cust_id

-- 5  Вивести кількість товарів (кількість елементів) в кожному замовленні. 
-- Поля у відповіді позначити order_num, num_items.

-- select 
--   order_num,
--   count(order_num) as num_items
--   from orders
-- group by order_num

-- 6  Вивести vend_id та кількість товарів, яку пропонує кожен з постачальників,
-- якщо ця кількість більше 2. Поля у відповіді позначити vend_id, num_prods.

-- select 
--   vend_id, 
--   count(*) as num_prods
--   from products
-- group by vend_id
-- having count(*) > 2

-- 7  Вивести vend_id та кількість товарів за ціною $4 і вище, 
-- яку пропонуєкожен з постачальників, якщо пропонована кількість 
-- товарів >= 2. Поля у відповіді позначити vend_id, num_prods.

-- select 
--   vend_id, 
--   count(*) as num_prods
--   from products
-- where prod_price >= 4
-- group by vend_id
-- having count(*) > 2

-- 8  Вивести cust_id та кількість замовлень кожного покупця,
-- якщо замовлень більше одного. Поля у відповіді позначити cust_id, num_orders.

-- select 
--   cust_id,
--   count(*) as num_orders
--   from orders
-- group by cust_id
-- having count(*) > 1

-- 9  Вивести кількість товарів (кількість елементів) в кожному замовленні,
-- якщо товарів >= 3. Поля у відповіді позначити order_num, num_items

-- select 
-- 	order_num,
-- 	sum(quantity) as num_items
-- 	from orderitems
-- group by order_num
-- having sum(quantity) >= 3

-- 10  Вивести vend_id та кількість товарів, яку пропонує кожен з постачальників,
-- якщо ця кількість більше 2. Поля у відповіді позначити vend_id, num_prods. 
-- Відповідь впорядкувати за полем vend_id

-- select 
--   vend_id,
--   count (*) as num_prods
--   from products
-- group by vend_id
-- having count(*) > 2
-- order by vend_id

-- 11  Вивести кількість товарів (кількість елементів) в кожному замовленні, 
-- якщо товарів >= 3. Поля у відповіді позначити order_num, num_items. 
-- Відповідь впорядкувати за полем num_items.

-- select 
--   order_num,
--   sum(quantity) as num_items
--   from orderitems
-- group by order_num
-- having count(quantity) >= 3
-- order by num_items

-- 12  Вивести назву та ім'я контактної особи всіх покупців,
-- що замовляли товар RGAN01 (в 12.1 підзапиті вивести order_num замовлень,
-- в яких prod_id ='RGAN01', в 12.2 підзапиті вивести cust_id відповідних покупців) 

-- 12.1

-- select 
--   orders.order_num
--   from orders 
--   inner join orderitems using(order_num)
-- where orderitems.prod_id = 'RGAN01'

-- 12.2

-- select 
--   cust_id,
--   cust_name,
--   cust_contact
--   from customers
--   inner join orders using(cust_id)
--   inner join orderitems using(order_num)
-- where orderitems.prod_id = 'RGAN01'


-- 14  Вивести імена та країни покупців, а також кількість замовлень
-- кожного покупця. Поля у відповіді позначити cust_name, cust_state, num_orders. 
-- Відповідь впорядкувати за полем cust_name.

-- select 
--   count(*) as num_orders,
--   cust_name,
--   cust_country
--   from customers
--   inner join orders using(cust_id)
-- group by cust_id
-- order by cust_name

-- 15  Вивести імена постачальників та назви й ціни товарів, які вони пропонують.
-- 18  Виконати запит 15 за допомогою INNER JOIN.

-- select 
--   vend_name,
--   prod_name,
--   prod_price
--   from products 
--   inner join vendors using(vend_id)

-- 19 Дослідити LEFT JOIN, RIGHT JOIN, FULL JOIN для таблиць 
-- Vendors, Products. Проаналізувати діаграми Венна.

-- 19.1 Обрати назви всіх наявних товарів та відповідних їм постачальників

-- select 
-- 	vendors.vend_id,
-- 	prod_name
-- 	from products 
-- 	left join vendors using(vend_id)

-- 19.2 Обрати всіх постачальників та назви їх продукцій, що є в наявності

-- select 
-- 	vendors.vend_id,
-- 	prod_name
-- 	from products
-- 	right join vendors using(vend_id)

-- 19.3 Обрати всі наявні товари з відповідними їм постачальниками
-- та всіх відомих постачальників та товари, що вони пропонують

-- select 
-- 	vendors.vend_id,
-- 	prod_name
-- 	from products
-- 	full join vendors using(vend_id)
