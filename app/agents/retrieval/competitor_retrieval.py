from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_competitors(product):

    query = f"""
    Competitor marketing campaigns,
    creator marketing strategies,
    and brand positioning for {product}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response["results"]