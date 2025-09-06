import os
from agents import Agent, ModelSettings
from clarifier_agent import get_gemini_model
from serpapi import GoogleSearch



def fetch_serp_results(query: str) -> str:
    """Fetch Google search snippets using SerpAPI."""
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),  # Make sure this is set in your .env
        "hl": "en",
        "num": 5   # get top 5 results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    if "organic_results" in results:
        for res in results["organic_results"][:5]:
            if "snippet" in res:
                snippets.append(res["snippet"])

    return "\n".join(snippets) if snippets else "No results found."

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    model=get_gemini_model(),
    model_settings=ModelSettings(tool_choice="required"),
)

# search_agent.py