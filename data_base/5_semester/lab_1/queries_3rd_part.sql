-- Яка назва проданого найдорожчого товару?

-- select 
	-- distinct prod_name 
	-- from products 
	-- inner join orderitems using(prod_id)  
-- where item_price = (select 
						-- max(item_price)
						-- from orderitems)

-- Як звуть покупця з найдовшим іменем – поле назвати long_name

-- select 
	-- cust_name as long_name 
	-- from customers
-- where length(cust_name) = (select 
						   	-- max(length(cust_name))
						   	-- from customers)


-- Вивести PROD_ID товарів та імена постачальників для тих товарів, 
-- які були продані. Результат вивести у верхньому регістрі, як єдине
-- поле products_sold

-- select distinct
	-- upper(products.prod_id || ' - ' || vend_name) as products_sold
	-- from orderitems inner join products using(prod_id)
	-- inner join vendors using(vend_id)
