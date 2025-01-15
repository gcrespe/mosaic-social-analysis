import redis
import json

redis_client = redis.Redis(host='redis-17941.c308.sa-east-1-1.ec2.redns.redis-cloud.com', port=17941, password='okjCxnSNLBIrsQ3PuaQyjLmlSPVDoDgn')

async def fetch_tweet_data(query, type, client, max_tweets=100):

    cache_key = query+type+str(max_tweets)

    data_cache = redis_client.lrange(cache_key, 0, -1)
    
    if(data_cache == None or data_cache == []):
        
        await client.login(auth_info_1='gcrespe', auth_info_2='gcrespe3@hotmail.com', password='199146658732')

        tweets = await client.search_tweet(query, count=max_tweets, product=type)
        tweet_data_list = []

        for tweet in tweets:

            single_tweet_data = await client.get_tweet_by_id(tweet_id=tweet.id)

            tweet_data = {
                'id': single_tweet_data.id,
                'text': single_tweet_data.text,
                'view_count': single_tweet_data.view_count,
                'retweet_count': single_tweet_data.retweet_count,
                'quote_count': single_tweet_data.quote_count,
                'reply_count': single_tweet_data.reply_count,
                'favorite_count': single_tweet_data.favorite_count,
                'user_screen_name': single_tweet_data.user.screen_name,
                'lang': single_tweet_data.lang,
                'user_name': single_tweet_data.user.name,
                'created_at': str(single_tweet_data.created_at_datetime),
                'sensitive': single_tweet_data.possibly_sensitive
            }
            tweet_data_list.append(tweet_data)

        formatted_tweet_data = [json.dumps(tweet) for tweet in tweet_data_list]

        # Push the formatted data into Redis
        redis_client.lpush(cache_key, *formatted_tweet_data)#pass the list as separate arguments
    else:
        return data_cache
    
    return tweet_data_list

