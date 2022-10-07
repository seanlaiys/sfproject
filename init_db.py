import psycopg2
import os
from dotenv import load_dotenv

def init_db():
    path = './tweets.sql'
    env_path = os.path.join('env_var', 'userdb.env')
    load_dotenv(env_path)
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    conn = psycopg2.connect(
            host="localhost",
            database="sf_db",
            user=user,
            password=password)

    # Open cursor and insert data into the table
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Tweets')
    create_statement = ('CREATE TABLE Tweets (username VARCHAR(255),'
            ' retweets int,'
            ' likes int,'
            ' replies int,' 
            ' total_engagement int,'
            ' url VARCHAR(255)')
    cur.execute(create_statement)
    cur.execute(open(path, "r").read())
    conn.commit()

    cur.close()

    return conn

if __name__ == "__main__":
    init_db()
