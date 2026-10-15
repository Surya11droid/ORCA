from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()


tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY"),
)

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a given topic. Returns titles, urls, and snippets of the top search results.
    """
    results = tavily_client.search(query=query, num_results=5).get("results", [])
    out = []
    for r in results:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
    
    return "\n".join(out)

@tool
def web_scrape(url: str) -> str:
    """
    scrape and return clean text content from a given URL for deeper analysis.
    
    """
    try:
        resp= requests.get(url, timeout= 8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, "html.parser")
        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer"]):

            tag.decompose()
        return soup.get_text(separator="\n", strip=True)[:1000]  # Return first 1000 characters of text content
    except Exception as e:
        return f"Error scraping the URL: {e}"



