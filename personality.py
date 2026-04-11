import random

def startup(name):
    return f"VORIS online. What's on your mind, {name}?"

def greeting(name):
    responses = [
        f"Hello, {name}.",
        f"Good to see you, {name}.",
        f"I'm here, {name}. What do you need?",
        f"Hey, {name}.",
    ]
    return random.choice(responses)

def searching():
    responses = [
        "On it.",
        "Let me find that.",
        "Searching now.",
        "Give me a moment.",
    ]
    return random.choice(responses)

def remember_confirm(key, value):
    return f"Noted. {key} is {value}."

def not_found(key):
    return f"I don't have anything on {key} yet. Let me look."

def shutdown(name):
    return f"Going offline. I'll be here when you need me, {name}."