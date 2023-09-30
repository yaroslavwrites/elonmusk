import asyncio
from twscrape import API
from csv import DictWriter

async def get_elonmusk_tweets():
    api = API() 
    # Add accounts (the more accounts you have, the faster you will be able to scrap)
    await api.pool.add_account("twitter_username", "twitter_password", "email", "email_password")
    await api.pool.add_account("twitter_username", "twitter_password", "email", "email_password")
    await api.pool.add_account("twitter_username", "twitter_password", "email", "email_password")

    await api.pool.login_all()

    # Fetch tweets
    elon_tweets = []
    # Here, I scrap all tweets from 2012
    async for tweet in api.search("from:elonmusk since:2012-01-01 until:2013-01-01"):
        tweet_data = tweet.dict()
        
        # Remove the fields you don't want
        tweet_data.pop('lang', None)
        tweet_data.pop('_type', None)
        
        elon_tweets.append(tweet_data)

    return elon_tweets

def save_to_csv(tweets, filename="2012.csv"):
    if not tweets:
        return
    
    # Fields of the CSV file (exclude 'lang' and '_type')
    fields = [key for key in tweets[0].keys()]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)

if __name__ == "__main__":
    tweets = asyncio.run(get_elonmusk_tweets())
    save_to_csv(tweets)





