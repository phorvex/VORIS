from ddgs import DDGS

def search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if results:
            return results[0]["body"]
        return "I couldn't find anything on that."