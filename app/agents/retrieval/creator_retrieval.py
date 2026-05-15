from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def retrieve_creator_patterns(product):

    query = f"""
    high-performing creators,
    influencer storytelling styles,
    creator audience trust patterns,
    engagement structures,
    creator marketing formats,
    skincare creator campaigns,
    and viral creator strategies for {product}
    """

    print("\n===================================")
    print("RETRIEVING CREATOR INTELLIGENCE")
    print("===================================\n")

    try:

        response = client.search(

            query=query,

            search_depth="advanced",

            max_results=8,

            include_raw_content=True
        )

        results = response.get("results", [])

        print(f"CREATOR RESULTS: {len(results)}")

        return results

    except Exception as e:

        print("CREATOR RETRIEVAL FAILED")
        print(str(e))

        return []