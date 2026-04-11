import datetime
import pytz
from memory import remember, recall, save_memory, load_memory
from search import search

def normalize(key):
    stopwords = ["my", "the", "a", "an", "our", "your"]
    key = key.replace("?", "").replace(".", "").replace("!", "")
    words = key.lower().split()
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

def detect_intent(text):
    text = text.lower().replace("?", "").replace(".", "").replace("!", "")
    if any(phrase in text for phrase in ["who am i", "what is my name", "what's my name"]):
        return "identity"
    if any(phrase in text for phrase in ["how old am i", "what is my age", "what's my age"]):
        return "age"
    if any(phrase in text for phrase in ["what time is it", "what's the time", "current time", "what is the time"]):
        return "time"
    if any(phrase in text for phrase in ["what is the date", "what is todays date", "what day is it", "today's date"]):
        return "date"
    if any(phrase in text for phrase in ["what is your name", "who are you", "what are you"]):
        return "voris_identity"
    if any(phrase in text for phrase in ["search for", "look up", "find out about"]):
        return "search"
    return None

load_memory()
print("VORIS online.")

TIMEZONE = pytz.timezone("America/New_York")

while True:
    user_input = input("You: ")
    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(normalize(key.strip()), value.strip())
        save_memory()
        print(f"VORIS: Got it. I'll remember that {key} is {value}.")
    elif detect_intent(user_input) == "identity":
        name = recall("name")
        print(f"VORIS: You are {name}.")
    elif detect_intent(user_input) == "voris_identity":
        print(f"VORIS: I am VORIS. I am yours.")
    elif detect_intent(user_input) == "age":
        age = recall("age")
        print(f"VORIS: You are {age} years old.")
    elif detect_intent(user_input) == "time":
        now = datetime.datetime.now(TIMEZONE).strftime("%I:%M %p")
        print(f"VORIS: It is {now}.")
    elif detect_intent(user_input) == "date":
        today = datetime.datetime.now(TIMEZONE).strftime("%A, %B %d %Y")
        print(f"VORIS: Today is {today}.")
    elif detect_intent(user_input) == "search":
        query = user_input.lower().replace("search for", "").replace("look up", "").replace("find out about", "").strip()
        print("VORIS: Searching...")
        result = search(query)
        print(f"VORIS: {result}")
    elif user_input.lower().startswith("what is"):
        key = normalize(user_input.lower().split("what is")[1].strip())
        result = recall(key)
        if result == "I don't know that yet.":
            print("VORIS: Let me look that up...")
            searched = search(user_input)
            print(f"VORIS: {searched}")
        else:
            print(f"VORIS: {result}")
    elif user_input.lower() in ["exit", "goodbye", "shutdown"]:
        save_memory()
        print("VORIS: Going offline. Goodbye.")
        break
    else:
        print("VORIS: Let me look that up...")
        result = search(user_input)
        print(f"VORIS: {result}")