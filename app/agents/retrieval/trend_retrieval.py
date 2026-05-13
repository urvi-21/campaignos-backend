from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_trends(product, audience):

    query = f"""
    Current social media trends, viral content formats,
    audience behavior, and campaign patterns for
    {product} targeting {audience}
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response["results"]