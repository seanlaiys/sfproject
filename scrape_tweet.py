from minet.twitter import TwitterAPIScraper
import pandas as pd
import os

# Scrapes tweet containing urls and convert collected data to sql
def scrape_tweet():
    # Initialise variables
    scraper = TwitterAPIScraper()
    df = pd.read_csv('urls.csv')
    urls = df.iloc[:, 0].values.tolist()
    tweets = []
    path = './tweets.sql'

    # If SQL file exists, remove
    if os.path.exists(path):
        os.remove(path)

    # Scrape Tweets into Dict
    for url in urls:
        for tweet in scraper.search_tweets(url):
            tweet_dict = {'username': '', 'retweets':'', 'likes':'', 'replies':'', 'url':''}
            tweet_dict['username'] = str(tweet['user_name']).replace("'", "''")
            tweet_dict['retweets'] = int(tweet['retweet_count'])
            tweet_dict['likes'] = int(tweet['like_count'])
            tweet_dict['replies'] = int(tweet['reply_count'])
            tweet_dict['total_engagement'] = tweet_dict['retweets'] + tweet_dict['likes'] + tweet_dict['replies']
            tweet_dict['url'] = url
            tweets.append(tweet_dict)

    # Convert Tweet Dict to SQL
    for tweet_dict in tweets:
        columns = ', '.join(str(x).replace('/', '_') for x in tweet_dict.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in tweet_dict.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('Tweets', columns, values)

        # Write to File
        f = open(path, "a")
        f.write(sql + '\n')

if __name__ == "__main__":
    scrape_tweet()
