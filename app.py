from tweety import TwitterAsync
from tweety import types
import asyncio

twitter_client = TwitterAsync("session")
async def start_twitter_client():
    await twitter_client.start("gcrespe", "199146658732")

async def main():
    await start_twitter_client()
    all_tweets: list[types.Tweet] = await twitter_client.get_tweets("elonmusk")
    for tweet in all_tweets:
        
        print("Tweet ", tweet.id, " -----------------------------")
        tweet_json = {
            "id": tweet.id,
            "author": tweet.author.username,
            "text": tweet.text,
            "likes": tweet.likes,
            "replies": tweet.reply_counts,
            "retweeted": tweet.retweeted_tweet != None
        }
        print(tweet_json)

        analytics = await twitter_client.get_tweet_analytics(tweet_id=tweet.id)
        
        print(analytics)
        print("")
    trends = await twitter_client.get_trends() #TODO verificar se tem como mudar as trends para outro lugar do mundo
    print(trends)        

    trends = await twitter_client.get_trends() 
    print(trends)   


asyncio.run(main())