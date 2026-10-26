# A pretend web search, shaped like the AgentCore Web Search
# connector: same limits, a domain filter, and results with a
# title, URL, snippet and date. The "web" is a tiny local file.
import json
from pathlib import Path

from strands import tool

INDEX = json.loads((Path(__file__).parent / "index.json").read_text())
EXCLUDE = ["rumours.example"]  # set by the admin, per target


@tool
def web_search(query: str, max_results: int = 10) -> dict:
    """Search the web. Always cite the URLs you use."""
    if len(query) > 200:
        return {"error": "Query must be 200 characters or less"}
    max_results = min(max(max_results, 1), 25)
    words = [w[:5] for w in query.lower().split() if len(w) > 3]
    hits, excluded = [], []
    for page in INDEX:
        text = (page["title"] + " " + page["text"]).lower()
        if not any(w in text for w in words):
            continue
        if any(d in page["url"] for d in EXCLUDE):
            excluded.append(page["url"])  # filtered out
        else:
            hits.append(page)
    return {"results": hits[:max_results], "excluded": excluded}
