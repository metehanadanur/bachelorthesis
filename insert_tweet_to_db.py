import json

import psycopg2
from psycopg2.extras import execute_batch


def insert_tweets_into_db(json_file='tweets_data.json'):

    with open(json_file, 'r') as f:
        tweets_data = json.load(f)

    dbname = 'DBNAME'
    user = 'USERNAME'
    password = 'PASSWORD'
    host = 'HOST '


    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id SERIAL PRIMARY KEY,
            full_text TEXT,
            conversation_id_str VARCHAR(255),
            created_at TIMESTAMP
        )
    ''')


    tweet_records = [(tweet['full_text'], tweet['conversation_id_str'], tweet['created_at']) for tweet in tweets_data]


    execute_batch(cur, '''
        INSERT INTO tweets (full_text, conversation_id_str, created_at)
        VALUES (%s, %s, %s)
    ''', tweet_records)


    conn.commit()
    cur.close()
    conn.close()