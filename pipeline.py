from agents import writer_chaim, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # step 1 - web search
    print("\n" + "=" * 50)
    print("step 1 - search agent is working")
    print("=" * 50)

    # LangChain tool-calling agents are failing due to model compatibility with the HF endpoint.
    # Fallback: directly call the web_search tool.
    from tools import web_search, scrape_url

    search_result_text = web_search.invoke(
        f"Find recent, reliable and detailed information about: {topic}"
    )
    state["search_results"] = search_result_text

    print("\n search result ", state["search_results"])

    # step 2 - scrape first URL
    print("\n" + "=" * 50)
    print("step 2 - scraping top resources ...")
    print("=" * 50)

    first_url = None
    for line in state["search_results"].splitlines():
        if line.strip().startswith("URL:"):
            first_url = line.split("URL:", 1)[1].strip()
            break

    if not first_url:
        raise RuntimeError("Could not find a URL in search results")

    state["scraped_content"] = scrape_url.invoke(first_url)

    print("\nscraped content: \n", state["scraped_content"])

    # step 3 - writer chain
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    # Writer uses HF model; if the HF connection fails, return a basic report from scraped data.
    try:
        state["report"] = writer_chaim.invoke(
            {"topic": topic, "research": research_combined}
        )
    except Exception as e:
        state["report"] = (
            f"Topic: {topic}\n\n"
            f"(Writer model failed: {e})\n\n"
            f"--- Search Results ---\n{state['search_results']}\n\n"
            f"--- Scraped Content ---\n{state['scraped_content']}"
        )

    print("\n Final Report\n", state["report"])

    # step 4 - critic report
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    try:
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
    except Exception as e:
        state["feedback"] = (
            f"Critic model failed: {e}\n\n"
            f"--- Report ---\n{state['report']}"
        )

    print("\n critic report \n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)

