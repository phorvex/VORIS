import datetime
import pytz
import requests
import re
import platform
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
from listen import enable_mic, disable_mic, is_mic_on, listen, enable_wake_word, disable_wake_word, is_wake_word_on
from convert import convert
from code_brain import ask_code_brain, is_code_question, is_ollama_available, save_code, run_code, serve_html
from notes import add_note, get_notes, clear_notes, delete_note, add_reminder, check_reminders, get_reminders
from news import get_news, get_news_brief, list_sources
from twilio_comm import send_sms, alert, critical_alert, call_admin, start_server, set_handler
from logger import log_system, log_conversation, log_error, log_learning, log_self, log_security, log_twilio, get_recent_errors, get_recent_alerts, get_todays_summary, read_log, schedule_nightly
from web_ui import start_web_ui, set_web_handler
from vision import enroll_user, verify_face, detect_objects_from_camera, is_camera_available, list_users, delete_user, start_monitoring

if platform.system() == "Linux":
    from face import set_state, start_face, stop_face, get_input_from_face, STATE_IDLE, STATE_SPEAKING, STATE_THINKING, STATE_LISTENING
else:
    def set_state(state, text=""): pass
    def start_face(): pass
    def stop_face(): pass
    def get_input_from_face(): return input("You: ")
    STATE_IDLE = STATE_SPEAKING = STATE_THINKING = STATE_LISTENING = "idle"

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
    if any(phrase in clean for phrase in ["text me", "send me a text", "send sms", "send alert", "sms me", "shoot me a text"]):
        return "send_sms"
    if any(phrase in clean for phrase in ["call me", "call my phone", "phone me"]):
        return "call_me"
    if any(phrase in clean for phrase in ["write code", "write a function", "write a script", "write a program", "write a python", "write a bash", "write a javascript", "write a java", "debug this", "fix this code", "explain this code", "code for", "help me code", "how do i code", "implement", "create a function", "build a", "write me a", "generate a", "generate code", "make a script", "make a program"]):
        return "code"
    if any(phrase in clean for phrase in ["save the code", "save it", "save that", "save to", "save the file"]):
        return "save_code"
    if any(phrase in clean for phrase in ["run the code", "run it", "execute the code", "run that", "run the file"]):
        return "run_code"
    if any(phrase in clean for phrase in ["serve it", "host it", "serve the html", "host the site", "start the server"]):
        return "serve_html"
    if any(phrase in clean for phrase in ["take a note", "add a note", "note that", "remember to", "write down"]):
        return "add_note"
    if any(phrase in clean for phrase in ["read my notes", "show my notes", "what are my notes", "my notes"]):
        return "get_notes"
    if any(phrase in clean for phrase in ["clear my notes", "delete all notes", "wipe my notes"]):
        return "clear_notes"
    if any(phrase in clean for phrase in ["remind me", "set a reminder", "set reminder"]):
        return "add_reminder"
    if any(phrase in clean for phrase in ["my reminders", "show reminders", "what are my reminders"]):
        return "get_reminders"
    if any(phrase in clean for phrase in ["what's the news", "whats the news", "news today", "top news", "latest news", "give me the news", "news briefing", "morning briefing"]):
        return "news_brief"
    if any(phrase in clean for phrase in ["news about", "news on", "show me news", "get me news"]):
        return "news_topic"
    if any(phrase in clean for phrase in ["news sources", "what news sources", "available news"]):
        return "news_sources"
    if any(phrase in clean for phrase in ["enable wake word", "wake word on", "hey voris mode", "passive listen"]):
        return "wake_on"
    if any(phrase in clean for phrase in ["disable wake word", "wake word off", "stop passive"]):
        return "wake_off"
    if any(phrase in clean for phrase in ["show errors", "recent errors", "what went wrong", "any errors"]):
        return "show_errors"
    if any(phrase in clean for phrase in ["show alerts", "any alerts", "critical alerts"]):
        return "show_alerts"
    if any(phrase in clean for phrase in ["todays log", "show the log", "read the log", "log summary"]):
        return "show_log"
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
    if any(phrase in clean for phrase in ["system status", "system stats", "how is the system", "system info", "what system are you on", "check system", "system report", "system specs", "my specs", "pc specs", "hardware info", "storage specs", "what is my storage", "disk space"]):
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
    if any(phrase in clean for phrase in ["enroll user", "add user", "register user"]):
        return "enroll_user"
    if any(phrase in clean for phrase in ["verify face", "scan my face"]):
        return "verify_face"
    if any(phrase in clean for phrase in ["list users", "show users", "who is enrolled"]):
        return "list_users"
    if any(phrase in clean for phrase in ["remove user", "delete user", "unenroll"]):
        return "remove_user"
    if any(phrase in clean for phrase in ["what do you see", "look around", "scan the room", "whats in front"]):
        return "detect_objects"
    if any(phrase in clean for phrase in ["start monitoring", "watch the room", "enable camera"]):
        return "start_monitoring"
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
        if len(content) > 10:
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

def is_admin_command(text):
    blocked = ["sudo", "rm -rf", "mkfs", "dd if", "chmod 777", "chown root", "passwd", "userdel", "usermod"]
    clean = text.lower()
    return any(b in clean for b in blocked)

def process_input(user_input, from_web=False):
    global name
    response = None
    extracted = extract_facts(user_input, remember, recall, save_memory)
    intent = detect_intent(user_input)

    if user_input.lower().startswith("remember"):
        try:
            parts = user_input.split("remember")[1].strip()
            key, value = parts.split(" is ")
            remember(normalize(key.strip()), value.strip())
            save_memory()
            response = remember_confirm(key.strip(), value.strip())
        except:
            response = "I couldn't store that. Try: remember X is Y."
    elif intent == "send_sms":
        text = user_input.lower()
        msg = "VORIS checking in."
        for phrase in ["send me a text", "text me", "send sms", "send alert", "sms me", "shoot me a text"]:
            if phrase in text:
                remainder = text.split(phrase)[1].strip()
                if remainder:
                    msg = remainder
                break
        result = send_sms(msg)
        log_twilio("SENT", "admin", msg, "success" if result else "failed")
        response = "Message sent." if result else "Couldn't send the message."
    elif intent == "call_me":
        call_admin("This is VORIS. You asked me to call you.")
        log_twilio("CALL", "admin", "user requested call", "initiated")
        response = "Calling you now."
    elif intent == "show_errors":
        response = get_recent_errors()
    elif intent == "show_alerts":
        response = get_recent_alerts()
    elif intent == "show_log":
        response = get_todays_summary()
    elif intent == "greeting":
        name = recall("name")
        response = greeting(name)
    elif intent == "how_are_you":
        response = how_are_you()
    elif intent == "identity":
        name = recall("name")
        response = f"You are {name}."
    elif intent == "voris_identity":
        response = "I am VORIS — Voice Operated Responsive Intelligent System. I exist to serve you, learn from you, and grow with you."
    elif intent == "age":
        response = f"You are {recall('age')} years old."
    elif intent == "birthday":
        birthday = recall("birthday")
        response = "I don't know your birthday yet." if birthday == "I don't know that yet." else f"Your birthday is {birthday}."
    elif intent == "birthday_day":
        birthday = recall("birthday")
        if birthday == "I don't know that yet.":
            response = "I don't know your birthday yet."
        else:
            try:
                year_match = re.search(r'\b(19|20)\d{2}\b', user_input)
                year = int(year_match.group()) if year_match else datetime.datetime.now().year
                bday = dateparser.parse(f"{birthday} {year}")
                day_name = bday.strftime("%A")
                response = f"Your birthday falls on a {day_name} this year." if year == datetime.datetime.now().year else f"Your birthday fell on a {day_name} in {year}."
            except:
                response = search(f"what day is {birthday} {datetime.datetime.now().year}")
    elif intent == "autolearn":
        topic = user_input.lower()
        for phrase in ["learn more about", "learn about", "study", "research", "go learn", "teach yourself about", "teach yourself"]:
            if phrase in topic:
                topic = topic.split(phrase)[1].strip()
                break
        summary = auto_learn(topic, update_callback=lambda msg: print(f"VORIS: {msg}"))
        response = summary
    elif intent == "current_location":
        location = get_current_location()
        response = f"Based on your IP, you appear to be in {location}."
    elif intent == "home_location":
        location = recall("location")
        response = "I don't know where you live yet." if location == "I don't know that yet." else f"You live in {location}."
    elif intent == "time_in_location":
        loc_text = user_input.lower()
        for phrase in ["what time is it in", "time in", "current time in"]:
            if phrase in loc_text:
                loc_text = loc_text.split(phrase)[1].strip().replace("?", "")
                break
        result = get_time_in_location(loc_text)
        response = result if result else f"I couldn't get the time for {loc_text}."
    elif intent == "time":
        response = f"It is {datetime.datetime.now(TIMEZONE).strftime('%I:%M %p')}."
    elif intent == "date":
        response = f"Today is {datetime.datetime.now(TIMEZONE).strftime('%A, %B %d %Y')}."
    elif intent == "date_tomorrow":
        tomorrow = datetime.datetime.now(TIMEZONE) + datetime.timedelta(days=1)
        response = f"Tomorrow is {tomorrow.strftime('%A, %B %d %Y')}."
    elif intent == "weather_here":
        location = recall("location")
        if location == "I don't know that yet.":
            location = get_current_location()
        response = get_weather(location)
    elif intent == "weather":
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
        response = get_weather(location)
    elif intent == "save_code":
        filepath = None
        for phrase in ["save to ", "save it to ", "save that to "]:
            if phrase in user_input.lower():
                filepath = user_input.lower().split(phrase)[1].strip()
                break
        response = save_code(filepath)
    elif intent == "run_code":
        response = run_code()
    elif intent == "serve_html":
        response = serve_html()
    elif intent == "code":
        if is_ollama_available():
            set_state(STATE_THINKING)
            result = ask_code_brain(user_input)
            response = result if result else "My coding brain ran into an issue. Try again."
        else:
            response = "My coding brain is offline on this machine."
    elif intent == "add_note":
        text = user_input.lower()
        for phrase in ["take a note", "add a note", "note that", "remember to", "write down"]:
            if phrase in text:
                text = text.split(phrase)[1].strip()
                break
        response = add_note(text)
    elif intent == "get_notes":
        response = get_notes()
    elif intent == "clear_notes":
        response = clear_notes()
    elif intent == "add_reminder":
        text = user_input.lower()
        mins_match = re.search(r'(\d+)\s*(minute|min|hour|hr)', text)
        if mins_match:
            amount = int(mins_match.group(1))
            unit = mins_match.group(2)
            minutes = amount * 60 if "hour" in unit or "hr" in unit else amount
            reminder_text = text
            for phrase in ["remind me to", "remind me in", "remind me"]:
                if phrase in text:
                    reminder_text = text.split(phrase)[1].strip()
                    reminder_text = re.sub(r'in \d+ (minute|min|hour|hr)s?', '', reminder_text).strip()
                    reminder_text = re.sub(r'\d+ (minute|min|hour|hr)s?', '', reminder_text).strip()
                    reminder_text = re.sub(r'^to\s+', '', reminder_text).strip()
                    break
            response = add_reminder(reminder_text, minutes)
        else:
            response = "How many minutes should I remind you in?"
    elif intent == "get_reminders":
        response = get_reminders()
    elif intent == "news_brief":
        response = get_news_brief()
    elif intent == "news_topic":
        topic = user_input.lower()
        for phrase in ["news about", "news on", "show me news about", "get me news on", "show me news", "get me news"]:
            if phrase in topic:
                topic = topic.split(phrase)[1].strip()
                break
        response = get_news(category=topic)
    elif intent == "news_sources":
        response = list_sources()
    elif intent == "convert":
        result = convert(user_input)
        response = result if result else search(user_input)
    elif intent == "math":
        result = calculate(user_input)
        response = result if result else search(user_input)
    elif intent == "correction":
        response = "I'll note that. What's the correct answer?"
    elif intent == "tell_me":
        topic = user_input.lower()
        for phrase in ["tell me more about", "tell me about", "tell me more"]:
            if phrase in topic:
                topic = topic.split(phrase)[1].strip().replace("?", "")
                break
        if topic:
            cached = recall_knowledge_exact(topic) or recall_knowledge(topic)
            response = cached if cached else search(topic)
        else:
            response = "What would you like to know more about?"
    elif intent == "search":
        query = user_input.lower().replace("search for", "").replace("look up", "").replace("find out about", "").strip()
        cached = recall_knowledge(query)
        response = cached if cached else search(query)
    elif intent == "show_knowledge":
        knowledge_data = get_all_knowledge()
        if knowledge_data:
            count = len(knowledge_data)
            topics = ", ".join(list(knowledge_data.keys())[:5])
            response = f"I have learned {count} things so far. Recent topics include: {topics}."
        else:
            response = "I haven't learned anything from searches yet."
    elif intent == "history":
        if len(conversation_history) > 1:
            last = conversation_history[-2]["content"]
            response = f"You said: {last}"
        else:
            response = "I don't have anything before this."
    elif intent == "system_status":
        response = get_system_summary()
    elif intent == "processes":
        response = get_running_processes()
    elif intent == "network":
        response = get_network_info()
    elif intent == "partitions":
        response = get_disk_partitions()
    elif intent == "battery":
        response = get_battery()
    elif intent == "uptime":
        response = get_uptime()
    elif intent == "packages":
        response = get_installed_packages()
    elif intent == "environment":
        response = get_environment_vars()
    elif intent == "run_command":
        if from_web and is_admin_command(user_input):
            response = "I can't run admin commands remotely."
        else:
            command = user_input.strip()
            for phrase in ["run ", "execute "]:
                if user_input.lower().startswith(phrase):
                    command = user_input[len(phrase):].strip()
                    break
            response = run_command(command)
    elif intent == "list_dir":
        path = "."
        for phrase in ["what's in", "list files in", "list directory", "show files in", "show filesystems"]:
            if phrase in user_input.lower():
                path = user_input.lower().split(phrase)[1].strip() or "."
                break
        response = list_directory(path)
    elif intent == "create_file":
        parts = user_input.lower().replace("create file", "").replace("make file", "").replace("new file", "").strip()
        response = create_file(parts)
    elif intent == "read_file":
        path = user_input.lower().replace("read file", "").replace("show file", "").replace("open file", "").strip()
        response = read_file(path)
    elif intent == "delete_file":
        if from_web:
            response = "File deletion is not allowed from the web interface."
        else:
            path = user_input.lower().replace("delete file", "").replace("remove file", "").strip()
            response = delete_file(path)
    elif intent == "enroll_user":
        parts = user_input.lower()
        name = None
        level = 3
        for phrase in ["enroll user", "add user", "register user"]:
            if phrase in parts:
                remainder = parts.split(phrase)[1].strip()
                words = remainder.split()
                if words:
                    name = words[0].capitalize()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                break
        if name:
            if not is_camera_available():
                response = "No camera available for enrollment."
            else:
                _, result = enroll_user(name, level)
                response = result
        else:
            response = "Who should I enroll? Say: enroll user Name level 3"
    elif intent == "verify_face":
        if not is_camera_available():
            response = "No camera available."
        else:
            name, level, msg = verify_face()
            response = msg
    elif intent == "list_users":
        users = list_users()
        response = "Enrolled users: " + ", ".join(users)
    elif intent == "remove_user":
        parts = user_input.lower()
        uname = "Unknown"
        for phrase in ["remove user", "delete user", "unenroll"]:
            if phrase in parts:
                uname = parts.split(phrase)[1].strip().capitalize()
                break
        response = delete_user(uname)
    elif intent == "detect_objects":
        if not is_camera_available():
            response = "No camera available."
        else:
            response = detect_objects_from_camera()
    elif intent == "start_monitoring":
        def on_detection(event, path):
            print(f"VORIS: Unknown face detected — {path}")
        start_monitoring(callback=on_detection)
        response = "Camera monitoring started. I'll alert you if I see an unknown face."
    elif user_input.lower().startswith("what is"):
        has_math = any(op in user_input.lower() for op in ["square root", "squared", "cubed", "sqrt", "+", "-", "*", "/", "times", "divided by", "plus", "minus"])
        if has_math:
            math_result = calculate(user_input)
            response = math_result if math_result else search(user_input)
        else:
            key = normalize(user_input.lower().split("what is")[1].strip())
            cached = recall_knowledge_exact(key) or recall_knowledge(key)
            if cached:
                response = cached
            else:
                mem = recall(key)
                response = mem if mem != "I don't know that yet." else search(user_input)
    else:
        last_intent = get_last_intent()
        if last_intent == "weather" and any(word in user_input.lower() for word in ["tomorrow", "tonight", "weekend", "later"]):
            location = get_last_location() or "Lakeland Florida"
            response = get_weather_tomorrow(location)
        elif is_followup(user_input):
            last_query = get_last_search_query()
            if last_query:
                filler = ["do i need to", "how much would", "what about", "will it", "can i", "should i", "is it", "what is the", "tell me more about", "and the"]
                clean_followup = user_input.lower()
                for f in filler:
                    clean_followup = clean_followup.replace(f, "").strip()
                combined = f"{clean_followup} {last_query}"
                cached = recall_knowledge(combined)
                response = cached if cached else search(combined)
            else:
                response = search(user_input)
        elif extracted:
            response = "Noted."
        else:
            cached = recall_knowledge(user_input)
            response = cached if cached else search(user_input)

    if response:
        try:
            log_conversation("phillippi", user_input, intent or "unknown", response, 0.0)
            learn(user_input, response, source="voris")
        except:
            pass

    return response or "I'm not sure about that."

load_memory()
load_knowledge()
conversation_history = []
name = recall("name")

def voris_say(message):
    set_state(STATE_SPEAKING, message[:50])
    print(f"VORIS: {message}")
    conversation_history.append({"role": "voris", "content": message})
    speak(message)
    set_state(STATE_IDLE)

start_face()
schedule_nightly()
log_system("VORIS started on " + platform.node(), "INFO")

def handle_remote_input(text):
    if is_shutdown(text.lower().strip()):
        return "Shutting down is not allowed remotely."
    conversation_history.append({"role": "user", "content": text})
    response = process_input(text, from_web=True)
    conversation_history.append({"role": "voris", "content": response})
    return response

set_handler(handle_remote_input)
start_server(handle_remote_input, port=5000)
set_web_handler(handle_remote_input)
start_web_ui(handle_remote_input, port=9117)

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
            user_input = get_input_from_face()
    else:
        user_input = get_input_from_face()

    conversation_history.append({"role": "user", "content": user_input})

    due_reminders = check_reminders()
    for reminder in due_reminders:
        voris_say(f"Reminder: {reminder}")

    if detect_intent(user_input) == "mic_on":
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
    elif detect_intent(user_input) == "wake_on":
        def wake_triggered():
            global mic_enabled
            mic_enabled = True
            print("VORIS: I heard you. What do you need?")
            speak("I heard you. What do you need?")
        result = enable_wake_word(wake_triggered)
        voris_say(result)
    elif detect_intent(user_input) == "wake_off":
        result = disable_wake_word()
        voris_say(result)
    elif is_shutdown(user_input):
        save_memory()
        name = recall("name")
        voris_say(shutdown(name))
        stop_face()
        try:
            import curses
            curses.endwin()
        except:
            pass
        log_system("VORIS shutdown.", "INFO")
        break
    else:
        response = process_input(user_input, from_web=False)
        voris_say(response)
        conversation_history.append({"role": "voris", "content": response})