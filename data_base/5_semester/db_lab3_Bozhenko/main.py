import psycopg2
from matplotlib import pyplot as plt

username = 'Bozhenko_Anna'
password = 'anna'
database = 'DeskDrop_DB'
host = 'localhost'
port = '5432'

query_01 = 'drop view if exists type_interactions_count'
query_02 = 'drop view if exists country_authors_count'
query_03 = 'drop view if exists readable_countries_count'

query_1 = '''create view type_interactions_count as
    select 
        event_type,
        count(*) as event_number
    from userinteraction
    group by event_type
    order by count(*) desc'''

query_2 = '''create view country_authors_count as
    (select 
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

query_3 = '''create view readable_countries_count as
    select
        country,
        count(*) as views_number
    from userinteraction
    join authorcontent using(content_id)
    join author using(author_id)
    join regioncountry on region = author_geo_origin
    where event_type = 'VIEW'
    group by country;'''

query_4 = 'select * from type_interactions_count'

query_5 = 'select * from country_authors_count'

query_6 = 'select * from readable_countries_count'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

def create_views():
    with conn:
        cur = conn.cursor()
        # make sure views don't exist
        cur.execute(query_01)
        cur.execute(query_02)
        cur.execute(query_03)
        # creation of views
        cur.execute(query_1)
        cur.execute(query_2)
        cur.execute(query_3)
    
    conn.commit()

def draw_views(name_to_save):
    with conn:
        cur = conn.cursor()
        fig, (pie_q1, bar_q2, bar_q3) = plt.subplots(1, 3, figsize = (12, 9), gridspec_kw={'width_ratios': [1, 2, 2]})
        cur.execute(query_4)
        events = []
        events_count = []
        for row in cur.fetchall():
            events.append(row[0].strip())
            events_count.append(row[1])
        
        wedges, texts, autotexts = pie_q1.pie(events_count, autopct='%1.1f%%')
        pie_q1.legend(wedges, events, title="Events", loc="best", bbox_to_anchor=(1, 0))
        pie_q1.set_title("Скільки якого виду взаємодій \n користувачів виявлено?")

        cur.execute(query_5)
        countries = []
        authors_count = []
        for row in cur.fetchall():
            countries.append(row[0].strip())
            authors_count.append(row[1])
        bar_q2.bar(countries, authors_count)
        bar_q2.set_title("Скільки авторів є в кожній країні?")

        cur.execute(query_6)
        countries = []
        views_number = []
        for row in cur.fetchall():
            countries.append(row[0].strip())
            views_number.append(row[1])
        bar_q3.bar(countries, views_number)
        bar_q3.set_title("Яка кількість переглядів контенту,\n створеного авторами з кожної країни?")
        plt.savefig(name_to_save)
        plt.show()
        plt.close()

if __name__ == "__main__":
    # create_views()

    draw_views("new_graphs.png")
