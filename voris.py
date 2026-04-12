import datetime
import pytz
import requests
from memory import remember, recall, save_memory, load_memory
from search import search
from personality import startup, greeting, searching, remember_confirm, not_found, shutdown, how_are_you

def normalize(key):
    stopwords = ["my", "the", "a", "an", "our", "your"]
    key = key.replace("?", "").replace(".", "").replace("!", "")
    words = key.lower().split()
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

def get_weather(location):
    try:
        url = f"https://wttr.in/{location}?format=3"
        response = requests.get(url, timeout=5)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return response.text.strip()
        return "I couldn't get the weather right now."
    except:
        return "I couldn't reach the weather service."

def detect_intent(text):
    clean = text.lower().replace("?", "").replace(".", "").replace("!", "").strip()
    if any(clean == phrase or clean.startswith(phrase + " ") for phrase in ["hello", "hi", "hey", "sup", "what's up", "wassup"]):
        return "greeting"
    if any(phrase in clean for phrase in ["how are you", "you good", "you okay", "how do you feel"]):
        return "how_are_you"
    if any(phrase in clean for phrase in ["who am i", "what is my name", "what's my name"]):
        return "identity"
    if any(phrase in clean for phrase in ["how old am i", "what is my age", "what's my age"]):
        return "age"
    if any(phrase in clean for phrase in ["what time is it", "what's the time", "current time", "what is the time"]):
        return "time"
    if any(phrase in clean for phrase in ["what is the date", "what is todays date", "what day is it", "today's date"]):
        return "date"
    if any(phrase in clean for phrase in ["what is your name", "who are you", "what are you"]):
        return "voris_identity"
    if any(phrase in clean for phrase in ["weather in", "weather for", "what is the weather", "whats the weather"]):
        return "weather"
    if any(phrase in clean for phrase in ["search for", "look up", "find out about"]):
        return "search"
    return None

load_memory()
name = recall("name")
print(startup(name))

TIMEZONE = pytz.timezone("America/New_York")

while True:
    user_input = input("You: ")
    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(normalize(key.strip()), value.strip())
        save_memory()
        print(f"VORIS: {remember_confirm(key.strip(), value.strip())}")
    elif detect_intent(user_input) == "greeting":
        name = recall("name")
        print(f"VORIS: {greeting(name)}")
    elif detect_intent(user_input) == "how_are_you":
        print(f"VORIS: {how_are_you()}")
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
    elif detect_intent(user_input) == "weather":
        text = user_input.lower()
        location = None
        for phrase in ["weather in", "weather for"]:
            if phrase in text:
                location = text.split(phrase)[1].strip().replace("?", "")
                break
        if not location:
            location = recall("location")
            if location == "I don't know that yet.":
                location = "Lakeland Florida"
        print(f"VORIS: {searching()}")
        result = get_weather(location)
        print(f"VORIS: {result}")
    elif detect_intent(user_input) == "search":
        query = user_input.lower().replace("search for", "").replace("look up", "").replace("find out about", "").strip()
        print(f"VORIS: {searching()}")
        result = search(query)
        print(f"VORIS: {result}")
    elif user_input.lower().startswith("what is"):
        key = normalize(user_input.lower().split("what is")[1].strip())
        result = recall(key)
        if result == "I don't know that yet.":
            print(f"VORIS: {not_found(key)}")
            searched = search(user_input)
            print(f"VORIS: {searched}")
        else:
            print(f"VORIS: {result}")
    elif user_input.lower() in ["exit", "goodbye", "shutdown"]:
        save_memory()
        name = recall("name")
        print(f"VORIS: {shutdown(name)}")
        break
    else:
        print(f"VORIS: {searching()}")
        result = search(user_input)
        print(f"VORIS: {result}")