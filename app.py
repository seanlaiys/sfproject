from flask import Flask, render_template, url_for, redirect, request
from forms import SearchForm
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

def get_db_connection():
    env_path = os.path.join('env_var', 'userdb.env')
    load_dotenv(env_path)
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    conn = psycopg2.connect(
        host="localhost",
        database="sf_db",
        user=user,
        password=password)
    return conn

def get_user_url(conn, arg):
    cur = conn.cursor()
    query = ('SELECT DISTINCT t.username FROM Tweets t')
    cur.execute(query)
    users = cur.fetchall()
    if arg:
        users = [user for user in users if arg.lower() in str(user).lower()]
    cur.close()
    cur = conn.cursor()
    query = ('SELECT DISTINCT t.username, t.url FROM Tweets t')
    cur.execute(query)
    urls = cur.fetchall()
    conn.close()
    return users, urls

def get_most_tweets_users(conn):
    cur = conn.cursor()
    query = ('SELECT t.username, COUNT(*) FROM Tweets t'
            ' GROUP BY t.username'
            ' ORDER BY COUNT(*) DESC'
            ' LIMIT 20')
    cur.execute(query)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def get_most_engagement_url(conn):
    cur = conn.cursor()
    query = ('SELECT t.url, SUM(t.total_engagement) AS engagement, SUM(t.retweets), SUM(t.likes), SUM(t.replies)' 
            ' FROM Tweets t'
            ' GROUP BY t.url'
            ' ORDER BY engagement DESC'
            ' LIMIT 20')
    cur.execute(query)
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return urls

def get_most_engagement_users(conn):
    cur = conn.cursor()
    query = ('SELECT t.username, SUM(t.total_engagement) AS engagement, SUM(t.retweets), SUM(t.likes), SUM(t.replies)' 
            ' FROM Tweets t'
            ' GROUP BY t.username'
            ' ORDER BY engagement DESC'
            ' LIMIT 20')
    cur.execute(query)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/users', methods=['GET', 'POST'])
def users():
    form = SearchForm(request.form)
    if request.method == 'POST':
        return redirect((url_for('users_query', query=form.search.data)))
    conn = get_db_connection()
    users, urls = get_user_url(conn, '')
    conn.close()
    return render_template('user.html', users=users, urls=urls, form=form)

@app.route('/users/<query>', methods=['GET', 'POST'])
def users_query(query):
    form = SearchForm(request.form)
    if request.method == 'POST':
        return redirect((url_for('users', query=form.search.data)))
    conn = get_db_connection()
    users, urls = get_user_url(conn, query)
    conn.close()
    return render_template('user.html', users=users, urls=urls, form=form)

@app.route('/most_tweets/')
def most_tweets():
    conn = get_db_connection()
    users = get_most_tweets_users(conn)
    conn.close()
    return render_template('most_tweets.html', users=users)

@app.route('/most_engagement_url/')
def most_engagement_url():
    conn = get_db_connection()
    urls = get_most_engagement_url(conn)
    conn.close()
    return render_template('most_engagement_url.html', urls=urls)

@app.route('/most_engagement_user/')
def most_engagement_user():
    conn = get_db_connection()
    users = get_most_engagement_users(conn)
    conn.close()
    return render_template('most_engagement_user.html', users=users)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)