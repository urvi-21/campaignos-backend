from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_social_signals(product, audience):

    query = f"""
    TikTok trends,
    Instagram engagement patterns,
    creator storytelling structures,
    viral skincare hooks,
    emotional engagement psychology,
    audience reactions,
    and creator campaign performance for
    {product} targeting {audience}
    """

    print("\n===================================")
    print("RETRIEVING SOCIAL INTELLIGENCE")
    print("===================================\n")

    try:

        response = client.search(

            query=query,

            search_depth="advanced",

            max_results=8,

            include_raw_content=True
        )

        results = response.get("results", [])

        print(f"SOCIAL RESULTS: {len(results)}")

        return results

    except Exception as e:

        print("SOCIAL RETRIEVAL FAILED")
        print(str(e))

        return []