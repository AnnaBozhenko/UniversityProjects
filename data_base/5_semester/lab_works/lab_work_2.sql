-- #1
-- select 
-- 	vend_name || ' - ' || vend_country as vendor_country 
-- from 
-- 	vendors

-- #2
-- select 
-- 	prod_id, 
-- 	quantity, 
-- 	item_price, 
-- 	quantity * item_price as expanded_price
-- from
-- 	orderitems
-- where 
-- 	order_num = 20008

-- #3
-- select 
-- 	lower(cust_name || ' - ' || cust_country) as customers_countris
-- from 
-- 	customers

-- #4
-- select 
-- 	upper(vend_name || ' - ' || vend_country) as vendor_name
-- from 
-- 	vendors

-- #5
-- select 
-- avg(prod_price) as avg_price
-- from products

-- #6
-- select
-- avg(item_price) as sale_avg_price
-- from orderitems

-- #7
-- select
-- 	max(prod_price) as max_price
-- from
-- 	products

-- #8
-- select
-- 	min(prod_price) as min_price
-- from 
-- 	products

-- #9
-- select
-- 	min(item_price) as sale_min_price
-- from 
-- 	orderitems

-- #10
-- select 
-- 	prod_name as cheapest_product
-- from 
-- 	products
-- where 
-- 	prod_price = (select 
-- 					min(prod_price) as min_price
-- 				from 
-- 					products)

-- #11
-- select 
-- 	prod_name as expensive_product
-- FROM
-- 	products
-- WHERE
-- 	prod_id in (select
-- 			  	prod_id
-- 			  from 
-- 			   	orderitems
-- 			  where
-- 			   item_price = (select 
-- 								max(item_price)
-- 							from
-- 								orderitems
-- 							)
-- 			   )

-- #12
-- select 
-- 	count(distinct cust_name) as distinct_customers_names_number
-- from customers

-- #13
-- select 
-- 	count(cust_email) as customers_with_email_number
-- from 
-- 	customers
-- where
-- 	cust_email is not null

-- #14
-- SELECT
-- 	count(*) as USA_vendors_number
-- from 
-- 	vendors
-- where vend_country = 'USA'

-- #15
-- select
-- 	count(*) as sold_items_number_at_20008
-- from 
-- 	orderitems
-- where
-- 	order_num = 20005
	
-- #16
-- select
-- 	sum(item_price * quantity) as total_price_at_20005
-- from 
-- 	orderitems
-- where 
-- 	order_num = 20005

	
-- #17
-- select
-- 	sum(quantity) as sold_most_expensive_item_number
-- from 
-- 	orderitems
-- where 
-- 	item_price = (select
-- 					max(item_price)
-- 				   from orderitems)

-- #18
-- select
-- sum(quantity) as sold_the_cheapest_item_number
-- from orderitems
-- where item_price = (select
-- 					min(item_price)
-- 				   	from orderitems)
