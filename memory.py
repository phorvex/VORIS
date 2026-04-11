import json
import os

memory = {}

def remember(key, value):
    memory[key] = value

def recall(key):
    return memory.get(key, "I don't know that yet.")

def save_memory():
    with open("memory.json", "w") as f:
        json.dump(memory, f)

def load_memory():
    global memory
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)