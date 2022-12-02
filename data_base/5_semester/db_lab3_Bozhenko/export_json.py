import json
import psycopg2

username = 'Bozhenko_Anna'
password = 'anna'
database = 'DeskDrop_DB'
host = 'localhost'
port = '5432'
TABLES = [
    'author',
    'regioncountry',
    'user_',
    'session_',
    'content_',
    'authorcontent',
    'userinteraction'
]

FILE_NAME = 'DeskDrop_DB.json'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:
    cur = conn.cursor()
    
    for table in TABLES:
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open(FILE_NAME, 'w') as outf:
    json.dump(data, outf, default = str)
    