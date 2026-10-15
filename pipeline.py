import re
from collections.abc import Callable

from agents import critic_chain, writer_chain
from tools import web_scrape, web_search


def run_research_pipeline(
    topic: str,
    progress_callback: Callable[[str], None] | None = None,
) -> dict[str, str]:
    state = {}

    def report_progress(message: str) -> None:
        if progress_callback is not None:
            progress_callback(message)

    # Search directly to avoid a model round-trip just to call the tool.
    report_progress("Searching the web")
    print("\n"+" ="*50)
    print("step 1: Searching the web for relevant information...")
    print("\n"+" ="*50)
    state["search_result"] = web_search.invoke({
        "query": f"recent and reliable information on: {topic}"
    })
    first_url = re.search(
        r"^URL:\s*(https?://\S+)",
        state["search_result"],
        re.MULTILINE,
    )
    if first_url is None:
        raise ValueError(f"Web search returned no usable URLs for topic: {topic}")
    print("\n Search Results:\n", state["search_result"])

    # Scrape the top-ranked result directly instead of asking a model to select it.
    report_progress("Reading the top search result")
    print("\n"+" ="*50)
    print("step 2: Scraping the top search result for deeper analysis...")
    print("\n"+" ="*50)
    state["reader_result"] = web_scrape.invoke({"url": first_url.group(1)})

    print("\n Scraped Content:\n", state["reader_result"])

    #writer chain working
    report_progress("Writing the research report")
    print("\n"+" ="*50)
    print("step 3: Writing a detailed research report...")
    print("\n"+" ="*50)
    research_combined=(
        f"Search Results:\n{state['search_result']}\n\n"
        f"Scraped Content:\n{state['reader_result']}"
    )

    state['report']= writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n Research Report:\n", state["report"])

    #critic chain working
    report_progress("Reviewing the report")
    print("\n"+" ="*50)
    print("step 4: Critiquing the research report...")
    print("\n"+" ="*50)

    state["feedback"]= critic_chain.invoke({
        "report": state['report']})
    print("\n Critique:\n", state["feedback"])

    return state



if __name__ == "__main__":
    topic = "Will JEV replace LLMs in the next 5 years?"
    run_research_pipeline(topic)
