import json
import os
import datetime

MEMORY_FILE = "memory.json"
KNOWLEDGE_FILE = "knowledge.json"

memory = {}
knowledge = {}

def remember(key, value, source="user", confidence=1.0):
    memory[key] = {
        "value": value,
        "source": source,
        "confidence": confidence,
        "learned_at": datetime.datetime.now().isoformat()
    }

def recall(key):
    if key in memory:
        entry = memory[key]
        if isinstance(entry, dict) and "value" in entry:
            return entry["value"]
        return entry
    return "I don't know that yet."

def learn(topic, content, source="search"):
    knowledge[topic] = {
        "content": content,
        "source": source,
        "learned_at": datetime.datetime.now().isoformat()
    }
    save_knowledge()

def recall_knowledge(topic):
    topic_lower = topic.lower()
    # exact match first
    if topic_lower in knowledge:
        return knowledge[topic_lower]["content"]
    # check if topic is contained in any stored key
    for key in knowledge:
        if topic_lower in key.lower():
            return knowledge[key]["content"]
    # check if any stored key is contained in topic
    for key in knowledge:
        if key.lower() in topic_lower:
            return knowledge[key]["content"]
    # check for significant word overlap
    topic_words = set(topic_lower.split())
    for key in knowledge:
        key_words = set(key.lower().split())
        overlap = topic_words & key_words
        significant = {w for w in overlap if len(w) > 3}
        if len(significant) >= 2:
            return knowledge[key]["content"]
    return None

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def save_knowledge():
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(knowledge, f, indent=2)

def load_memory():
    global memory
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            raw = json.load(f)
            for key, value in raw.items():
                if isinstance(value, dict) and "value" in value:
                    memory[key] = value
                else:
                    memory[key] = {
                        "value": value,
                        "source": "user",
                        "confidence": 1.0,
                        "learned_at": "unknown"
                    }

def load_knowledge():
    global knowledge
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r") as f:
            knowledge = json.load(f)

def get_all_memory():
    result = {}
    for key, entry in memory.items():
        if isinstance(entry, dict) and "value" in entry:
            result[key] = entry["value"]
        else:
            result[key] = entry
    return result

def get_all_knowledge():
    return {topic: data["content"] for topic, data in knowledge.items()}