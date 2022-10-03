-- Яка назва проданого найдорожчого товару?

-- select 
-- 	distinct prod_name 
-- 	from products inner join orderitems on products.prod_id = orderitems.prod_id  
-- 	where item_price = (select max(item_price) from orderitems)

-- Як звуть покупця з найдовшим іменем – поле назвати long_name

-- select 
-- 	cust_name as long_name 
-- 	from customers
-- where length(cust_name) = (select 
-- 						   	max(length(cust_name))
-- 						   	from customers)

-- Вивести PROD_ID товарів та імена постачальників для тих товарів, 
-- які були продані. Результат вивести у верхньому регістрі, як єдине
-- поле products_sold

-- select 
-- 	trim(upper(pr_v.prod_id || ' - ' || pr_v.vend_name)) as products_sold 
-- 	from (select 
-- 		  	pr.prod_id, v.vend_name
-- 			from products pr 
-- 		  	inner join vendors v on v.vend_id = pr.vend_id) pr_v
-- where pr_v.prod_id in (select 
-- 					   	prod_id 
-- 					   	from orderitems)