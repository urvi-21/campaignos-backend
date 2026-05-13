from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_social_signals(product, audience):

    query = f"""
    Reddit discussions, TikTok trends,
    audience conversations, creator content styles,
    and emotional engagement patterns for
    {product} targeting {audience}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response["results"]