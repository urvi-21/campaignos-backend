from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = ApifyClient(
    os.getenv("APIFY_API_TOKEN")
)


def retrieve_instagram_signals(query):

    run_input = {
        "search": query,
        "resultsLimit": 5
    }

    run = client.actor(
        "apify/instagram-hashtag-scraper"
    ).call(run_input=run_input)

    results = []

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():

        results.append({
            "caption": item.get("caption"),
            "hashtags": item.get("hashtags"),
            "likesCount": item.get("likesCount"),
            "commentsCount": item.get("commentsCount"),
            "displayUrl": item.get("displayUrl")
        })

    return results