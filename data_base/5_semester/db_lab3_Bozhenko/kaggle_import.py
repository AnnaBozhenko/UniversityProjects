import csv
import psycopg2
import random
from urllib.parse import quote

"""https://www.kaggle.com/datasets/gspmoreira/articles-sharing-reading-from-cit-deskdrop?select=users_interactions.csv"""

username = 'Bozhenko_Anna'
password = 'anna'
database = 'DeskDrop_DB'

USER_CONTENT_FILE = 'users_interactions.csv'
AUTHOR_CONTENT_FILE = 'shared_articles.csv'

conn = psycopg2.connect(user=username, password=password, dbname=database)
DISTINCT = 100

with conn:
    cur = conn.cursor()

    # declare lists to store already existing rows to avoid 'duplicate key error' while inserting rows
    cur.execute("""select * from regioncountry;""")
    regions_countries = [(row[0].strip(), row[1].strip()) for row in cur.fetchall()]    
    cur.execute("""select * from author;""")
    authors = cur.fetchall()

    cur.execute("""select * from content_;""")
    contents = cur.fetchall()

    cur.execute("""select * from session_;""")
    sessions = cur.fetchall()

    cur.execute("""select * from user_;""")
    users = cur.fetchall()

    cur.execute("""select * from userinteraction;""")
    interactions = cur.fetchall()

    with open(AUTHOR_CONTENT_FILE, 'r', encoding='utf-8') as inf:        
        reader = csv.DictReader(inf)
        for row in reader:
            author_id = int(row['authorPersonId'])
            content_id = int(row['contentId'])
            content_url = row['url']
            content_url = None if content_url == '' or len(content_url) > 200 else content_url
            
            if author_id not in [row[0] for row in authors]:
                cur.execute("""INSERT INTO Author (author_id) VALUES (%s)""", [author_id])
                authors.append((author_id, None))
            values = (content_id, content_url)
            if values not in contents:
                cur.execute("""INSERT INTO Content_ (content_id, content_url) VALUES (%s, %s)""", values)
                contents.append(values)
                values = (author_id, content_id)
                cur.execute("""INSERT INTO AuthorContent (author_id, content_id) VALUES (%s, %s)""", values)
        
    with open(USER_CONTENT_FILE, 'r', encoding='utf-8') as inf:
        reader = csv.DictReader(inf)
        count = 0
        for row in reader:
            user_id = int(row['personId'])
            content_id = int(row['contentId'])
            session_id = int(row['sessionId'])
            session_agent = row['userAgent']
            session_agent = None if session_agent == '' else session_agent
            event_type = str(row['eventType'])
            timestamp = int(row['timestamp'])
            country = row['userCountry']
            country = None if country == '' else country
            region = row['userRegion']
            region = None if region == '' else region

            values = (region, country)
            if region != None and country != None and region not in [row[0] for row in regions_countries] and (region + country).isalpha():
                cur.execute(f"""insert into RegionCountry (region, country) values (%s, %s)""", values)
                regions_countries.append(values)
                if user_id not in [row[0] for row in users]:
                    values = (user_id, region)
                    cur.execute(f"""insert into User_ (user_id_, user_geo_origin) values (%s, %s)""", values)
                    users.append(values)
                if content_id in [row[0] for row in contents]:
                    if session_id not in [row[0] for row in sessions]:
                        values = (session_id, session_agent)
                        cur.execute(f"""insert into Session_ (session_id, session_agent) values (%s, %s)""", values)
                        sessions.append(values)
                    interaction = (user_id, content_id, session_id, event_type, timestamp)
                    if interaction not in interactions:
                        cur.execute(f"""insert into UserInteraction (user_id_, content_id, session_id, event_type, timestamp_) values (%s, %s, %s, %s, %s)""", interaction)
                        interactions.append(interaction)
                    count += 1

    # put random countries to authors (no such info in kaggle but for queries from the 2nd lab)
    for author_id in [row[0] for row in authors]:
        region = random.choice(regions_countries)[0]
        cur.execute("""update Author 
            set author_geo_origin =  %s
            where author_id = %s;""", [region, author_id])
    conn.commit()
    