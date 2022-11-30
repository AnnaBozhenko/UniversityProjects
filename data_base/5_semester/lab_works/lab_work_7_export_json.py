import json
import psycopg2

username = 'Bozhenko_Anna'
password = 'anna'
database = 'Bozhenko_Anna_DB'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:

    cur = conn.cursor()
    
    for table in ('vendors', 'customers', 'orders', 'products', 'orderitems'):
        cur.execute('SELECT * FROM ' + table)
        fields = [x[0] for x in cur.description]
        rows = [dict(zip(fields, row)) for row in cur]

        data[table] = rows

with open('Bozhenko_Anna_DB.json', 'w') as outf:
    json.dump(data, outf, default = str)
    