import psycopg2
import pickle

username = 'Bozhenko_Anna'
password = 'anna'
database = 'DeskDrop_DB'
host = 'localhost'
port = '5432'

query_1 = '''select 
    event_type,
    count(*) as event_number
from userinteraction
group by event_type
order by count(*) desc'''

query_2 = '''(select 
    country,
    count(*) as authors_numb 
from regioncountry
join author on region = author_geo_origin
group by country)
union
(select 
    country, 
    coalesce(null, 0) as authors_numb
from regioncountry
where region not in (select author_geo_origin from author))
order by authors_numb desc;'''

query_3 = '''select
    country,
    count(*) as views_number
from userinteraction
join authorcontent using(content_id)
join author using(author_id)
join regioncountry on region = author_geo_origin
where event_type = 'VIEW'
group by country;'''



conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    
    print("\nСкільки якого виду взаємодій користувачів виявлено?\n")
    cur.execute(query_1)
    q1 = cur.fetchall()

    with open("query1.pickle", "wb") as outfile:
	    pickle.dump(q1, outfile)
    
    [print(record) for record in q1]

    print("\nСкільки авторів є в кожній країні?\n")
    cur.execute(query_2)
    q2 = cur.fetchall()

    with open("query2.pickle", "wb") as outfile:
	    pickle.dump(q2, outfile)

    [print(record) for record in q2]

    print("\nЯка кількість переглядів контенту, створеного авторами з кожної країни?\n")
    cur.execute(query_3)

    q3 = cur.fetchall()

    with open("query3.pickle", "wb") as outfile:
	    pickle.dump(q3, outfile)

    [print(record) for record in q3]
      