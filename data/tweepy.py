import redis
import json
import tweepy

# Initialize Redis client
redis_client = redis.Redis(
    host='redis-17941.c308.sa-east-1-1.ec2.redns.redis-cloud.com', 
    port=17941, 
    password='okjCxnSNLBIrsQ3PuaQyjLmlSPVDoDgn'
)

# Twitter API credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

async def fetch_tweet_data(query, type, max_tweets=100):
    cache_key = query + type + str(max_tweets)

    # Check if data is cached in Redis
    data_cache = redis_client.lrange(cache_key, 0, -1)
    
    if not data_cache:
        # Fetch tweets using Tweepy
        tweets = api.search_tweets(q=query, count=max_tweets, result_type=type)

        tweet_data_list = []

        for tweet in tweets:
            tweet_data = {
                'id': tweet.id,
                'text': tweet.text,
                'view_count': tweet.user.followers_count,  # Note: Twitter API does not provide view count directly
                'retweet_count': tweet.retweet_count,
                'quote_count': 0,  # Not available directly from search results
                'reply_count': 0,  # Not available directly from search results
                'favorite_count': tweet.favorite_count,
                'user_screen_name': tweet.user.screen_name,
                'lang': tweet.lang,
                'user_name': tweet.user.name,
                'created_at': str(tweet.created_at),
                'sensitive': False  # Not available directly from search results
            }
            tweet_data_list.append(tweet_data)

        # Format and push the data into Redis
        formatted_tweet_data = [json.dumps(tweet) for tweet in tweet_data_list]
        redis_client.lpush(cache_key, *formatted_tweet_data)  # Pass the list as separate arguments
    else:
        # Return cached data if available
        return [json.loads(data) for data in data_cache]

    return tweet_data_list