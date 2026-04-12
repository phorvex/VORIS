import datetime
import pytz
import requests
from memory import remember, recall, save_memory, load_memory
from search import search
from personality import startup, greeting, searching, remember_confirm, not_found, shutdown, how_are_you
from learn import extract_facts
from system import get_system_summary

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

def get_weather_tomorrow(location):
    try:
        url = f"https://wttr.in/{location}?format=%t+%C"
        response = requests.get(url, timeout=5)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return f"Tomorrow in {location}: {response.text.strip()}"
        return "I couldn't get tomorrow's forecast right now."
    except:
        return "I couldn't reach the weather service."

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        return f"{city}, {region}, {country}"
    except:
        return "I couldn't determine your current location."

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
    if any(phrase in clean for phrase in ["where am i right now", "where am i currently", "where am i"]):
        return "current_location"
    if any(phrase in clean for phrase in ["where do i live", "what is my location", "whatis my location", "where do i stay"]):
        return "home_location"
    if any(phrase in clean for phrase in ["what time is it", "what's the time", "current time", "what is the time"]):
        return "time"
    if any(phrase in clean for phrase in ["what is the date tomorrow", "tomorrow's date", "what day is tomorrow"]):
        return "date_tomorrow"
    if any(phrase in clean for phrase in ["what is the date", "what is todays date", "what day is it", "today's date"]):
        return "date"
    if any(phrase in clean for phrase in ["what is your name", "who are you", "what are you"]):
        return "voris_identity"
    if any(phrase in clean for phrase in ["weather in", "weather for", "what is the weather", "whats the weather"]):
        return "weather"
    if any(phrase in clean for phrase in ["search for", "look up", "find out about"]):
        return "search"
    if any(phrase in clean for phrase in ["what did i say", "what was my last message", "repeat that"]):
        return "history"
    if any(phrase in clean for phrase in ["system status", "how is the system", "system info", "what system are you on", "check system", "system report"]):
        return "system_status"
    return None

def get_last_intent():
    for entry in reversed(conversation_history):
        if entry["role"] == "voris":
            continue
        content = entry["content"].lower()
        if "weather" in content:
            return "weather"
        if "search" in content:
            return "search"
    return None

def get_last_location():
    for entry in reversed(conversation_history):
        content = entry["content"].lower()
        for phrase in ["weather in", "weather for"]:
            if phrase in content:
                return content.split(phrase)[1].strip().replace("?", "")
    return None

load_memory()
conversation_history = []
name = recall("name")
print(startup(name))

TIMEZONE = pytz.timezone("America/New_York")

def voris_say(message):
    print(f"VORIS: {message}")
    conversation_history.append({"role": "voris", "content": message})

while True:
    user_input = input("You: ")
    conversation_history.append({"role": "user", "content": user_input})
    extracted = extract_facts(user_input, remember, recall, save_memory)

    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(normalize(key.strip()), value.strip())
        save_memory()
        voris_say(remember_confirm(key.strip(), value.strip()))
    elif detect_intent(user_input) == "greeting":
        name = recall("name")
        voris_say(greeting(name))
    elif detect_intent(user_input) == "how_are_you":
        voris_say(how_are_you())
    elif detect_intent(user_input) == "identity":
        name = recall("name")
        voris_say(f"You are {name}.")
    elif detect_intent(user_input) == "voris_identity":
        voris_say("I am VORIS. I am yours.")
    elif detect_intent(user_input) == "age":
        age = recall("age")
        voris_say(f"You are {age} years old.")
    elif detect_intent(user_input) == "current_location":
        voris_say(searching())
        location = get_current_location()
        voris_say(f"Based on your IP, you appear to be in {location}.")
    elif detect_intent(user_input) == "home_location":
        location = recall("location")
        if location == "I don't know that yet.":
            voris_say("I don't know where you live yet.")
        else:
            voris_say(f"You live in {location}.")
    elif detect_intent(user_input) == "time":
        now = datetime.datetime.now(TIMEZONE).strftime("%I:%M %p")
        voris_say(f"It is {now}.")
    elif detect_intent(user_input) == "date":
        today = datetime.datetime.now(TIMEZONE).strftime("%A, %B %d %Y")
        voris_say(f"Today is {today}.")
    elif detect_intent(user_input) == "date_tomorrow":
        tomorrow = datetime.datetime.now(TIMEZONE) + datetime.timedelta(days=1)
        voris_say(f"Tomorrow is {tomorrow.strftime('%A, %B %d %Y')}.")
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
        voris_say(searching())
        result = get_weather(location)
        voris_say(result)
    elif detect_intent(user_input) == "search":
        query = user_input.lower().replace("search for", "").replace("look up", "").replace("find out about", "").strip()
        voris_say(searching())
        result = search(query)
        voris_say(result)
    elif detect_intent(user_input) == "history":
        if len(conversation_history) > 1:
            last = conversation_history[-2]["content"]
            voris_say(f"You said: {last}")
        else:
            voris_say("I don't have anything before this.")
    elif detect_intent(user_input) == "system_status":
        voris_say(get_system_summary())
    elif user_input.lower().startswith("what is"):
        key = normalize(user_input.lower().split("what is")[1].strip())
        result = recall(key)
        if result == "I don't know that yet.":
            voris_say(not_found(key))
            searched = search(user_input)
            voris_say(searched)
        else:
            voris_say(result)
    elif user_input.lower() in ["exit", "goodbye", "shutdown"]:
        save_memory()
        name = recall("name")
        voris_say(shutdown(name))
        break
    else:
        last_intent = get_last_intent()
        if last_intent == "weather" and any(word in user_input.lower() for word in ["tomorrow", "tonight", "weekend", "later"]):
            location = get_last_location() or "Lakeland Florida"
            voris_say(searching())
            result = get_weather_tomorrow(location)
            voris_say(result)
        elif extracted:
            pass
        else:
            voris_say(searching())
            result = search(user_input)
            voris_say(result)