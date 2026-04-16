import datetime
import pytz
import requests
import re
from dateutil import parser as dateparser
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from memory import remember, recall, save_memory, load_memory, learn, recall_knowledge, recall_knowledge_exact, load_knowledge, get_all_memory, get_all_knowledge
from search import search
from personality import startup, greeting, searching, remember_confirm, not_found, shutdown, how_are_you
from learn import extract_facts
from system import get_system_summary, get_running_processes, get_network_info, get_disk_partitions, get_battery, get_uptime, get_installed_packages, get_environment_vars
from tasks import run_command, create_file, list_directory, read_file, delete_file
from voice import speak, enable_voice, disable_voice, toggle_voice
from autolearn import auto_learn
from listen import enable_mic, disable_mic, is_mic_on, listen
from convert import convert

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

def get_time_in_location(location):
    try:
        geolocator = Nominatim(user_agent="voris")
        loc = geolocator.geocode(location, timeout=10)
        if not loc:
            return None
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        if not tz_name:
            return None
        tz = pytz.timezone(tz_name)
        local_time = datetime.datetime.now(tz).strftime("%I:%M %p")
        return f"It is {local_time} in {location}."
    except:
        return None

def calculate(expression):
    try:
        import math as mathlib
        import re
        clean_expr = expression.lower()
        for word in ["what is", "calculate", "how much is", "whats", "what's"]:
            clean_expr = clean_expr.replace(word, "")
        clean_expr = clean_expr.replace("square root of", "mathlib.sqrt(").replace("sqrt of", "mathlib.sqrt(")
        clean_expr = clean_expr.replace("squared", "**2").replace("cubed", "**3")
        clean_expr = clean_expr.replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
        if "mathlib.sqrt(" in clean_expr and not clean_expr.strip().endswith(")"):
            clean_expr = clean_expr.strip() + ")"
        clean_expr = re.sub(r'\bthe\b|\ba\b|\ban\b|\bof\b', '', clean_expr)
        clean_expr = ' '.join(clean_expr.split()).strip()
        result = eval(clean_expr, {"mathlib": mathlib, "__builtins__": {}})
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(round(result, 4))
    except:
        return None

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
    if any(phrase in clean for phrase in ["learn about", "learn more about", "study", "research", "go learn", "teach yourself"]):
        return "autolearn"
    if any(phrase in clean for phrase in ["what day is my birthday", "what day of the week is my birthday", "what day does my birthday fall", "what day was my birthday"]):
        return "birthday_day"
    if any(phrase in clean for phrase in ["when is my birthday", "what is my birthday", "whats my birthday", "when was i born", "what is my birth date"]):
        return "birthday"
    if any(phrase in clean for phrase in ["where am i right now", "where am i currently", "where am i"]):
        return "current_location"
    if any(phrase in clean for phrase in ["where do i live", "what is my location", "whatis my location", "where do i stay"]):
        return "home_location"
    if any(phrase in clean for phrase in ["what time is it in", "time in", "current time in"]):
        return "time_in_location"
    if any(phrase in clean for phrase in ["what time is it", "what's the time", "current time", "what is the time"]):
        return "time"
    if any(phrase in clean for phrase in ["what is the date tomorrow", "tomorrow's date", "what day is tomorrow"]):
        return "date_tomorrow"
    if any(phrase in clean for phrase in ["what is the date", "what is todays date", "what day is it", "today's date"]):
        return "date"
    if any(phrase in clean for phrase in ["what is your name", "who are you", "what are you", "what is your goal", "what is your purpose"]):
        return "voris_identity"
    if any(phrase in clean for phrase in ["weather here", "weather outside", "weather right now", "whats the weather"]):
        return "weather_here"
    if any(phrase in clean for phrase in ["weather in", "weather for", "what is the weather"]):
        return "weather"
    if any(phrase in clean for phrase in ["search for", "look up", "find out about"]):
        return "search"
    if any(phrase in clean for phrase in ["what did i say", "what was my last message", "repeat that"]):
        return "history"
    if any(phrase in clean for phrase in ["what do you know", "show knowledge", "what have you learned"]):
        return "show_knowledge"
    if any(phrase in clean for phrase in ["system status", "system stats", "how is the system", "system info", "what system are you on", "check system", "system report"]):
        return "system_status"
    if any(phrase in clean for phrase in ["what is running", "running processes", "show processes", "active processes"]):
        return "processes"
    if any(phrase in clean for phrase in ["network info", "network status", "what network", "show network", "ip address"]):
        return "network"
    if any(phrase in clean for phrase in ["show partitions", "disk partitions", "storage info", "what drives", "show drives", "disk info"]):
        return "partitions"
    if any(phrase in clean for phrase in ["battery", "battery status", "how much battery"]):
        return "battery"
    if any(phrase in clean for phrase in ["uptime", "how long has", "system uptime"]):
        return "uptime"
    if any(phrase in clean for phrase in ["installed packages", "what is installed", "show packages"]):
        return "packages"
    if any(phrase in clean for phrase in ["environment", "env vars", "show environment"]):
        return "environment"
    if any(phrase in clean for phrase in ["enable mic", "turn on mic", "mic on", "start listening"]):
        return "mic_on"
    if any(phrase in clean for phrase in ["disable mic", "turn off mic", "mic off", "stop listening"]):
        return "mic_off"
    if any(phrase in clean for phrase in ["enable voice", "turn on voice", "voice on"]):
        return "voice_on"
    if any(phrase in clean for phrase in ["disable voice", "turn off voice", "voice off"]):
        return "voice_off"
    if any(phrase in clean for phrase in ["toggle voice", "switch voice"]):
        return "voice_toggle"
    if any(phrase in clean for phrase in ["run ", "execute ", "cat ", "ls", "pwd", "whoami"]):
        return "run_command"
    if any(phrase in clean for phrase in ["list files", "list directory", "show files", "show filesystems", "what files", "what's in"]):
        return "list_dir"
    if any(phrase in clean for phrase in ["create file", "make file", "new file"]):
        return "create_file"
    if any(phrase in clean for phrase in ["read file", "show file", "open file"]):
        return "read_file"
    if any(phrase in clean for phrase in ["delete file", "remove file"]):
        return "delete_file"
    if any(phrase in clean for phrase in ["that is incorrect", "that's wrong", "that's incorrect", "you're wrong", "wrong answer", "that is wrong"]):
        return "correction"
    if any(phrase in clean for phrase in ["tell me about", "tell me more about", "tell me more"]):
        return "tell_me"
    if any(phrase in clean for phrase in ["convert", "to kilometers", "to miles", "to celsius", "to fahrenheit", "to pounds", "to kilograms", "to liters", "to gallons", "to meters", "to feet"]) and any(c.isdigit() for c in clean):
        return "convert"
    if any(c.isdigit() for c in clean) and any(op in clean for op in ["+", "-", "*", "/", "times", "divided by", "plus", "minus", "square root", "squared", "cubed", "sqrt"]):
        return "math"
    return None

def is_shutdown(text):
    clean = text.lower().strip()
    triggers = ["exit", "goodbye", "shutdown", "shut down", "turn off", "bye", "exit please", "please exit", "close", "quit"]
    return any(clean == t or clean.startswith(t) for t in triggers)

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

def get_last_search_query():
    for entry in reversed(conversation_history):
        if entry["role"] == "voris":
            continue
        content = entry["content"].lower()
        for phrase in ["search for", "look up", "find out about"]:
            if phrase in content:
                return content.split(phrase)[1].strip()
        if len(content) > 10 and content != user_input.lower():
            return content
    return None

def get_last_topic():
    for entry in reversed(conversation_history):
        if entry["role"] == "voris":
            continue
        content = entry["content"].lower()
        for phrase in ["learn about", "tell me about", "what is", "search for", "look up"]:
            if phrase in content:
                return content.split(phrase)[1].strip().replace("?", "").replace(".", "")
    return None

def is_followup(text):
    clean = text.lower().strip()
    followup_phrases = [
        "what about", "do i need", "what is the price", "how much",
        "what does it cost", "is it compatible", "will it fit",
        "what else", "and the", "what about the",
        "how do i", "where do i", "can i", "should i"
    ]
    return any(phrase in clean for phrase in followup_phrases)

load_memory()
load_knowledge()
conversation_history = []
name = recall("name")

def voris_say(message):
    print(f"VORIS: {message}")
    conversation_history.append({"role": "voris", "content": message})
    speak(message)

startup_message = startup(name)
print(startup_message)
speak(startup_message)

TIMEZONE = pytz.timezone("America/New_York")

while True:
    if is_mic_on():
        spoken = listen()
        if spoken:
            user_input = spoken
        else:
            user_input = input("You: ")
    else:
        user_input = input("You: ")
    conversation_history.append({"role": "user", "content": user_input})
    extracted = extract_facts(user_input, remember, recall, save_memory)
    if extracted:
        voris_say("Noted.")

    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(normalize(key.strip()), value.strip())
        save_memory()
        voris_say(remember_confirm(key.strip(), value.strip()))
    elif is_shutdown(user_input):
        save_memory()
        name = recall("name")
        voris_say(shutdown(name))
        break
    elif detect_intent(user_input) == "mic_on":
        result = enable_mic()
        print(f"VORIS: {result}")
        speak(result)
    elif detect_intent(user_input) == "mic_off":
        result = disable_mic()
        print(f"VORIS: {result}")
        speak(result)
    elif detect_intent(user_input) == "voice_on":
        result = enable_voice()
        print(f"VORIS: {result}")
    elif detect_intent(user_input) == "voice_off":
        result = disable_voice()
        print(f"VORIS: {result}")
    elif detect_intent(user_input) == "voice_toggle":
        result = toggle_voice()
        print(f"VORIS: {result}")
    elif detect_intent(user_input) == "greeting":
        name = recall("name")
        voris_say(greeting(name))
    elif detect_intent(user_input) == "how_are_you":
        voris_say(how_are_you())
    elif detect_intent(user_input) == "identity":
        name = recall("name")
        voris_say(f"You are {name}.")
    elif detect_intent(user_input) == "voris_identity":
        voris_say("I am VORIS. I exist to serve you, learn from you, and grow with you.")
    elif detect_intent(user_input) == "age":
        age = recall("age")
        voris_say(f"You are {age} years old.")
    elif detect_intent(user_input) == "birthday":
        birthday = recall("birthday")
        if birthday == "I don't know that yet.":
            voris_say("I don't know your birthday yet.")
        else:
            voris_say(f"Your birthday is {birthday}.")
    elif detect_intent(user_input) == "birthday_day":
        birthday = recall("birthday")
        if birthday == "I don't know that yet.":
            voris_say("I don't know your birthday yet.")
        else:
            try:
                year_match = re.search(r'\b(19|20)\d{2}\b', user_input)
                year = int(year_match.group()) if year_match else datetime.datetime.now().year
                bday = dateparser.parse(f"{birthday} {year}")
                day_name = bday.strftime("%A")
                if year == datetime.datetime.now().year:
                    voris_say(f"Your birthday falls on a {day_name} this year.")
                else:
                    voris_say(f"Your birthday fell on a {day_name} in {year}.")
            except:
                voris_say(searching())
                result = search(f"what day is {birthday} {datetime.datetime.now().year}")
                voris_say(result)
    elif detect_intent(user_input) == "autolearn":
        topic = user_input.lower()
        for phrase in ["learn more about", "learn about", "study", "research", "go learn", "teach yourself about", "teach yourself"]:
            if phrase in topic:
                topic = topic.split(phrase)[1].strip()
                break
        voris_say(f"Learning about {topic} now. Give me a moment.")
        summary = auto_learn(topic, update_callback=lambda msg: print(f"VORIS: {msg}"))
        voris_say(summary)
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
    elif detect_intent(user_input) == "time_in_location":
        loc_text = user_input.lower()
        for phrase in ["what time is it in", "time in", "current time in"]:
            if phrase in loc_text:
                loc_text = loc_text.split(phrase)[1].strip().replace("?", "")
                break
        result = get_time_in_location(loc_text)
        if result:
            voris_say(result)
        else:
            voris_say(f"I couldn't get the time for {loc_text}.")
    elif detect_intent(user_input) == "time":
        now = datetime.datetime.now(TIMEZONE).strftime("%I:%M %p")
        voris_say(f"It is {now}.")
    elif detect_intent(user_input) == "date":
        today = datetime.datetime.now(TIMEZONE).strftime("%A, %B %d %Y")
        voris_say(f"Today is {today}.")
    elif detect_intent(user_input) == "date_tomorrow":
        tomorrow = datetime.datetime.now(TIMEZONE) + datetime.timedelta(days=1)
        voris_say(f"Tomorrow is {tomorrow.strftime('%A, %B %d %Y')}.")
    elif detect_intent(user_input) == "weather_here":
        location = recall("location")
        if location == "I don't know that yet.":
            voris_say(searching())
            location = get_current_location()
        voris_say(searching())
        result = get_weather(location)
        voris_say(result)
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
        elif detect_intent(user_input) == "convert":
        result = convert(user_input)
        if result:
            voris_say(result)
        else:
            voris_say(searching())
            searched = search(user_input)
            learn(user_input, searched, source="search")
            voris_say(searched)
    elif detect_intent(user_input) == "math":
        result = calculate(user_input)
        if result:
            voris_say(result)
        else:
            voris_say(searching())
            searched = search(user_input)
            learn(user_input, searched, source="search")
            voris_say(searched)
    elif detect_intent(user_input) == "correction":
        last_voris = None
        for entry in reversed(conversation_history):
            if entry["role"] == "voris":
                last_voris = entry["content"]
                break
        voris_say("I'll note that. What's the correct answer?")
        correction = input("You: ")
        conversation_history.append({"role": "user", "content": correction})
        last_query = get_last_search_query()
        if last_query:
            learn(last_query, correction, source="user_correction")
        voris_say("Got it. I've updated what I know.")
    elif detect_intent(user_input) == "tell_me":
        topic = user_input.lower()
        for phrase in ["tell me more about", "tell me about", "tell me more"]:
            if phrase in topic:
                topic = topic.split(phrase)[1].strip().replace("?", "")
                break
        if not topic or topic == user_input.lower():
            topic = get_last_topic() or ""
        if topic:
            cached = recall_knowledge_exact(topic)
            if not cached:
                cached = recall_knowledge(topic)
            if cached:
                voris_say(cached)
            else:
                voris_say(searching())
                result = search(topic)
                learn(topic, result, source="search")
                voris_say(result)
        else:
            voris_say("What would you like to know more about?")
    elif detect_intent(user_input) == "search":
        query = user_input.lower().replace("search for", "").replace("look up", "").replace("find out about", "").strip()
        cached = recall_knowledge(query)
        if cached:
            voris_say(cached)
        else:
            voris_say(searching())
            result = search(query)
            learn(query, result, source="search")
            voris_say(result)
    elif detect_intent(user_input) == "show_knowledge":
        knowledge_data = get_all_knowledge()
        if knowledge_data:
            count = len(knowledge_data)
            topics = ", ".join(list(knowledge_data.keys())[:5])
            voris_say(f"I have learned {count} things so far. Recent topics include: {topics}.")
        else:
            voris_say("I haven't learned anything from searches yet.")
    elif detect_intent(user_input) == "history":
        if len(conversation_history) > 1:
            last = conversation_history[-2]["content"]
            voris_say(f"You said: {last}")
        else:
            voris_say("I don't have anything before this.")
    elif detect_intent(user_input) == "system_status":
        voris_say(get_system_summary())
    elif detect_intent(user_input) == "processes":
        voris_say("Here are the top running processes:")
        voris_say(get_running_processes())
    elif detect_intent(user_input) == "network":
        voris_say("Network information:")
        voris_say(get_network_info())
    elif detect_intent(user_input) == "partitions":
        voris_say("Disk partitions:")
        voris_say(get_disk_partitions())
    elif detect_intent(user_input) == "battery":
        voris_say(get_battery())
    elif detect_intent(user_input) == "uptime":
        voris_say(get_uptime())
    elif detect_intent(user_input) == "packages":
        voris_say(get_installed_packages())
    elif detect_intent(user_input) == "environment":
        voris_say(get_environment_vars())
    elif detect_intent(user_input) == "run_command":
        command = user_input.strip()
        for phrase in ["run ", "execute "]:
            if user_input.lower().startswith(phrase):
                command = user_input[len(phrase):].strip()
                break
        voris_say(f"Running: {command}")
        result = run_command(command)
        voris_say(result)
    elif detect_intent(user_input) == "list_dir":
        path = "."
        for phrase in ["what's in", "list files in", "list directory", "show files in", "show filesystems"]:
            if phrase in user_input.lower():
                path = user_input.lower().split(phrase)[1].strip() or "."
                break
        voris_say(list_directory(path))
    elif detect_intent(user_input) == "create_file":
        parts = user_input.lower().replace("create file", "").replace("make file", "").replace("new file", "").strip()
        voris_say(create_file(parts))
    elif detect_intent(user_input) == "read_file":
        path = user_input.lower().replace("read file", "").replace("show file", "").replace("open file", "").strip()
        voris_say(read_file(path))
    elif detect_intent(user_input) == "delete_file":
        path = user_input.lower().replace("delete file", "").replace("remove file", "").strip()
        voris_say(delete_file(path))
    elif user_input.lower().startswith("what is"):
        has_math = any(op in user_input.lower() for op in ["square root", "squared", "cubed", "sqrt", "+", "-", "*", "/", "times", "divided by", "plus", "minus"])
        if has_math:
            math_result = calculate(user_input)
            if math_result:
                voris_say(math_result)
            else:
                voris_say(searching())
                searched = search(user_input)
                learn(user_input, searched, source="search")
                voris_say(searched)
        else:
            key = normalize(user_input.lower().split("what is")[1].strip())
            cached = recall_knowledge_exact(key)
            if not cached:
                cached = recall_knowledge(key)
            if cached:
                voris_say(cached)
            else:
                result = recall(key)
                if result == "I don't know that yet.":
                    voris_say(not_found(key))
                    searched = search(user_input)
                    learn(key, searched, source="search")
                    voris_say(searched)
                else:
                    voris_say(result)
    else:
        last_intent = get_last_intent()
        if last_intent == "weather" and any(word in user_input.lower() for word in ["tomorrow", "tonight", "weekend", "later"]):
            location = get_last_location() or "Lakeland Florida"
            voris_say(searching())
            result = get_weather_tomorrow(location)
            voris_say(result)
        elif is_followup(user_input):
            last_query = get_last_search_query()
            if last_query:
                filler = ["do i need to", "how much would", "what about", "will it", "can i", "should i", "is it", "what is the", "tell me more about", "and the"]
                clean_followup = user_input.lower()
                for f in filler:
                    clean_followup = clean_followup.replace(f, "").strip()
                combined = f"{clean_followup} {last_query}"
                cached = recall_knowledge(combined)
                if cached:
                    voris_say(cached)
                else:
                    voris_say(searching())
                    result = search(combined)
                    learn(combined, result, source="search")
                    voris_say(result)
            else:
                voris_say(searching())
                result = search(user_input)
                learn(user_input, result, source="search")
                voris_say(result)
        elif extracted:
            pass
        else:
            cached = recall_knowledge(user_input)
            if cached:
                voris_say(cached)
            else:
                voris_say(searching())
                result = search(user_input)
                learn(user_input, result, source="search")
                voris_say(result)