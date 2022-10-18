import psycopg2

username = 'Bozhenko_Anna'
password = 'anna'
database = 'Bozhenko_Anna_DB'
host = 'localhost'
port = '5432'

query_1 = '''
SELECT cust_id, TRIM(cust_name) FROM customers
'''
query_2 = '''select TRIM(cust_name), coalesce(sum(item_price*quantity), 0) 
from customers left join orders using(cust_id) left join orderitems using (order_num)
group by cust_id;
'''



conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
print(type(conn))

with conn:

    print ("Database opened successfully")
    cur = conn.cursor()
    cur.execute(query_1)

    print('1.  Using simple iteration over cursor:\n')
    for row in cur:
        print(row)

    cur.execute(query_1)
    print('\n2.  Using \'fetchall\':\n')
    for row in cur.fetchall():
       print(row)

    cur.execute(query_1)
    print('\n3.  Using \'fetchone\' 20 times:\n')
    limit = 20
    for idx in range(limit):
        row = cur.fetchone()
        print(row)

    cur.execute(query_1)
    print('\n4.  Using \'fetchmany(20)\':\n')
    for row in cur.fetchmany(size=20):
        print(row)    	    