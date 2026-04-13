import re
from search import search
from memory import learn, recall_knowledge

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "was", "are", "were",
    "it", "its", "this", "that", "these", "those", "as", "be", "been",
    "has", "have", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "not", "no", "nor",
    "so", "yet", "both", "either", "neither", "also", "than", "then",
    "when", "where", "which", "who", "whom", "what", "how", "why",
    "known", "after", "later", "first", "second", "third", "during",
    "through", "into", "about", "up", "out", "over", "under", "again"
}

def estimate_complexity(topic, initial_result):
    word_count = len(initial_result.split())
    unique_words = len(set(initial_result.lower().split()))
    if word_count > 200 or unique_words > 100:
        return "complex"
    elif word_count > 100 or unique_words > 50:
        return "medium"
    return "simple"

def extract_keywords(text, limit=5):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    freq = {}
    for word in filtered:
        freq[word] = freq.get(word, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:limit]]

def generate_followup_queries(topic, result, complexity):
    keywords = extract_keywords(result)
    queries = []
    if complexity == "simple":
        queries = [
            f"{topic} examples",
            f"{topic} uses",
        ]
    elif complexity == "medium":
        queries = [
            f"{topic} examples",
            f"{topic} history",
            f"how does {topic} work",
        ]
    else:
        queries = [
            f"{topic} examples",
            f"{topic} history",
            f"how does {topic} work",
            f"{topic} applications",
            f"{topic} advantages and disadvantages",
        ]
    for keyword in keywords[:2]:
        if keyword not in topic.lower():
            queries.append(f"{topic} {keyword}")
    return queries[:8]

def auto_learn(topic, update_callback=None):
    results_learned = 0
    if update_callback:
        update_callback(f"Starting to learn about {topic}...")

    cached = recall_knowledge(topic)
    if cached:
        initial_result = cached
        if update_callback:
            update_callback(f"I already have some knowledge about {topic}. Expanding...")
    else:
        initial_result = search(topic)
        if not initial_result:
            return f"I couldn't find anything about {topic}."
        learn(topic, initial_result, source="autolearn")
        results_learned += 1
        if update_callback:
            update_callback(f"Learned the basics of {topic}.")

    complexity = estimate_complexity(topic, initial_result)
    if update_callback:
        update_callback(f"This looks like a {complexity} topic. Going deeper...")

    followup_queries = generate_followup_queries(topic, initial_result, complexity)

    for query in followup_queries:
        cached = recall_knowledge(query)
        if cached:
            continue
        result = search(query)
        if result and len(result) > 50:
            learn(query, result, source="autolearn")
            results_learned += 1
            if update_callback:
                update_callback(f"Learned about: {query}")

    summary = f"Done. I learned {results_learned} new things about {topic}."
    if complexity == "complex":
        summary += f" It's a complex topic — I went deep on it."
    elif complexity == "medium":
        summary += f" I have a solid understanding now."
    else:
        summary += f" Simple topic — I know the essentials."

    return summary