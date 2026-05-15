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

    audience frustrations,
    emotional triggers,
    skincare pain points,
    buying hesitation,
    product trust discussions,
    creator recommendations,
    and viral product opinions about
    {product} targeting {audience}
    """

    print("\n===================================")
    print("RETRIEVING REDDIT INTELLIGENCE")
    print("===================================\n")

    try:

        response = client.search(

            query=query,

            search_depth="advanced",

            max_results=10,

            include_raw_content=True
        )

        results = response.get("results", [])

        print(f"REDDIT RESULTS: {len(results)}")

        return results

    except Exception as e:

        print("REDDIT RETRIEVAL FAILED")
        print(str(e))

        return []