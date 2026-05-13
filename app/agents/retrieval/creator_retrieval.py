from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_creator_patterns(product):

    query = f"""
    High-performing creators, influencer content styles,
    engagement patterns, storytelling formats,
    and creator campaign strategies for {product}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response["results"]