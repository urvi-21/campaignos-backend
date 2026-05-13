from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_reddit_signals(product, audience):

    query = f"""
    site:reddit.com
    discussions, opinions, frustrations,
    buying behavior, emotional triggers,
    audience conversations, and trend discussions about
    {product} for {audience}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=8
    )

    return response["results"]