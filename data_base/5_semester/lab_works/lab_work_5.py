import psycopg2
import matplotlib.pyplot as plt

username = 'Bozhenko_Anna'
password = 'anna'
database = 'Bozhenko_Anna_DB'
host = 'localhost'
port = '5432'

query1 = """select 
    vend_id,
    sum(quantity * item_price) as total_vend_products_price
    from orderitems
    join products using(prod_id)
    join vendors using(vend_id)
group by vend_id;"""

query2 = """select 
    quantity,
    item_price
    from orderitems
where prod_id = 'BR03'
order by quantity;"""

vendors = []
vendors_sum = []

quantities = []
prices = []

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    cur.execute(query1)

    for row in cur:
        vendors.append(row[0])
        vendors_sum.append(row[1])
    
    cur.execute(query2)

    for row in cur:
        quantities.append(row[0])
        prices.append(row[1])


# 5	Стовпчикова діаграма: вивести постачальників та загальну суму продажів кожного постачальника. 

# plt.bar(vendors, vendors_sum)
# plt.xlabel("Vendors")
# plt.ylabel("Total sum")
# plt.show()

# 6	Кругова діаграма: відобразити частку суми продажів кожного постачальника серед загальної суми продажів
# plt.pie(vendors_sum, labels=vendors, autopct='%1.1f%%')
# plt.title("Prices of vendors' products")
# plt.show()

# 7	Графік залежності ціни товару BR03 від кількості штук у замовленні. Побудувати попередньо запит: Вивести кількість та ціну проданого товару BR03. 
# plt.plot(quantities, prices, marker = 'o')
# plt.xlabel("quantity, items number")
# plt.ylabel("price per item")
# plt.show()

# 8	Побудувати (5), (6), (7) на одному графіку. Виконати налаштування підписів на малюнках.
figure, (graph1, graph2, graph3) = plt.subplots(1, 3)

graph1.bar(vendors, vendors_sum)
graph1.set_xlabel("Vendors")
graph1.set_ylabel("Total sum")
graph1.set_title("Sum of sold products of each vendor")

graph2.pie(vendors_sum, labels=vendors, autopct='%1.1f%%')
graph2.set_title("Portion of sum of vendors products")

graph3.plot(quantities, prices, marker = 'o')
graph3.set_xlabel("quantity, items number")
graph3.set_ylabel("price per item")
graph3.set_title("Dependency of price from quantity of BR03 product")
for qnt, price in zip(quantities, prices):
        graph3.annotate(price, xy=(qnt, price), xytext=(3, 3), textcoords='offset points')

plt.show()
