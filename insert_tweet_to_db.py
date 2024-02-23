import json

import psycopg2
from psycopg2.extras import execute_batch


def insert_tweets_into_db(json_file='tweets_data.json'):
    # Load the JSON data
    with open(json_file, 'r') as f:
        tweets_data = json.load(f)

    dbname = 'yoxmqypd'  # This is often the same as the username for ElephantSQL
    user = 'yoxmqypd'
    password = 'bCBG4Dt9XW-rnx8UOlqZDgOCUea9AeOb'  # Replace with your actual password
    host = 'trumpet.db.elephantsql.com'

    # Connect to the ElephantSQL database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()

    # Create a table for tweets if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id SERIAL PRIMARY KEY,
            full_text TEXT,
            conversation_id_str VARCHAR(255),
            created_at TIMESTAMP
        )
    ''')

    # Prepare data for insertion
    tweet_records = [(tweet['full_text'], tweet['conversation_id_str'], tweet['created_at']) for tweet in tweets_data]

    # Insert data into the table
    execute_batch(cur, '''
        INSERT INTO tweets (full_text, conversation_id_str, created_at)
        VALUES (%s, %s, %s)
    ''', tweet_records)

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()