# Імпорт даних
# Створити таблицю  Products_new  як копію таблиці Products. Видалити всі рядки з таблиці Products_new.
# Переглянути файл з реальними даними products.csv.  Проаналізувати заголовки та типи даних.
# Написати код на Python для заповнення таблиці  Products_new  даними:            поле prod_id - значеннями Product_id; поле vend_id - значеннями vend_1, vend_2, … ; поле prod_name - значеннями Product_name; поле prod_price - значеннями Product_price.
# Переконатися, що в таблиці  Products_new  з'явились нові дані. 
# Видалити таблицю Products_new.

import csv
import decimal
import psycopg2

username = 'Bozhenko_Anna'
password = 'anna'
database = 'Bozhenko_Anna_DB'

INPUT_CSV_FILE = 'products.csv'

query_0 = 'drop table if exists products_new'

query_1 = '''
CREATE TABLE products_new
(
    prod_id character(10),
    vend_id character(10),
    prod_name character(255) NOT NULL,
    prod_price numeric(8,2) NOT NULL,
    prod_desc character varying(1000),
    CONSTRAINT pk_products_new PRIMARY KEY (prod_id)
);
'''

query_2 = '''
INSERT INTO products_new (prod_id, vend_id, prod_name, prod_price) VALUES (%s, %s, %s, %s);
'''

query_3 = 'drop table products_new;'

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)
    cur.execute(query_1)
    with open(INPUT_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            price = decimal.Decimal(row['Product_Price'].lstrip('$'))
            values = (row['Product_ID'], idx + 1, row['Product_Name'], price) 
            cur.execute(query_2, values)

    cur.execute('Select * from products_new;')
    [print(row) for row in cur]
    cur.execute(query_3)

    conn.commit()
