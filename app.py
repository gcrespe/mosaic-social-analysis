import time
import asyncio
from twikit.client.client import Client
from .data import trending_topics
from .data import fetch_tweet_data

twikit_client = Client(language='en-US')

async def main():
    data = []
    start_time = time.time()
    for topic in trending_topics:
        print(topic)
        topic_data = await fetch_tweet_data(topic, 'Latest', twikit_client)
        data.append(topic_data)
    print(data)
    print("--- %s seconds ---" % (time.time() - start_time))
    twikit_client.logout()

asyncio.run(main())