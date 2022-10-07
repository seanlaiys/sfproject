from unittest import result
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

def init_db():
    path = './tweets.sql'
#     env_path = os.path.join('env_var', 'userdb.env')
#     load_dotenv(env_path)
#     user = os.getenv('DB_USERNAME')
#     password = os.getenv('DB_PASSWORD')

    DATABASE_URL = urlparse("postgres://my_app_slys_1811:29uk9MajSTOg2peEnDB9@my-app-slys-1811.postgresql.a.osc-fr1.scalingo-dbs.com:38763/my_app_slys_1811?sslmode=prefer")
    username = DATABASE_URL.username
    password = DATABASE_URL.password
    database = DATABASE_URL.path[1:]
    hostname = DATABASE_URL.hostname
    port = DATABASE_URL.port

    conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port)

    # Open cursor and insert data into the table
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Tweets')
    create_statement = ('CREATE TABLE Tweets (username VARCHAR(255),'
            ' retweets int,'
            ' likes int,'
            ' replies int,' 
            ' total_engagement int,'
            ' url VARCHAR(255))')
    cur.execute(create_statement)
    cur.execute(open(path, "r").read())
    conn.commit()

    cur.close()

    return conn

if __name__ == "__main__":
    init_db()
