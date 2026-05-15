from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_trends(product, audience):

    query = f"""
    Current social media trends, viral creator formats,
    engagement behavior, emotional audience reactions,
    high-performing campaign narratives, and platform-native
    storytelling patterns for {product} targeting {audience}
    """

    print("\n===================================")
    print("RETRIEVING TREND INTELLIGENCE")
    print("===================================\n")

    try:

        response = client.search(

            query=query,

            search_depth="advanced",

            max_results=8,

            include_raw_content=True
        )

        results = response.get("results", [])

        print(f"TREND RESULTS: {len(results)}")

        return results

    except Exception as e:

        print("TREND RETRIEVAL FAILED")
        print(str(e))

        return []