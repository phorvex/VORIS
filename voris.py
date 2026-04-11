from memory import remember, recall, save_memory, load_memory

def normalize(key):
    stopwords = ["my", "the", "a", "an", "our", "your"]
    key = key.replace("?", "").replace(".", "").replace("!", "")
    words = key.lower().split()
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

load_memory()
print("VORIS online.")

while True:
    user_input = input("You: ")
    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(normalize(key.strip()), value.strip())
        save_memory()
        print(f"VORIS: Got it. I'll remember that {key} is {value}.")
    elif user_input.lower().startswith("what is"):
        key = normalize(user_input.split("what is")[1].strip())
        result = recall(key)
        if result == "I don't know that yet.":
            answer = input(f"VORIS: I don't know {key} yet. What is it? ")
            remember(key, answer)
            save_memory()
            print(f"VORIS: Got it. I'll remember that.")
        else:
            print(f"VORIS: {result}")
    elif user_input.lower() in ["exit", "goodbye", "shutdown"]:
        save_memory()
        print("VORIS: Going offline. Goodbye.")
        break
    else:
        print("VORIS: I don't know how to handle that yet.")