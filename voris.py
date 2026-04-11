from memory import remember, recall, save_memory, load_memory
load_memory()
print("VORIS online.")
while True:
    user_input = input("You: ")
    if user_input.lower().startswith("remember"):
        parts = user_input.split("remember")[1].strip()
        key, value = parts.split(" is ")
        remember(key.strip(), value.strip())
        save_memory()
        print(f"VORIS: Got it. I'll remember that {key} is {value}.")
    elif user_input.lower().startswith("what is"):
        key = user_input.split("what is")[1].strip()
        print(f"VORIS: {recall(key)}")
    elif user_input.lower() in ["exit", "goodbye", "shutdown"]:
        save_memory()
        print("VORIS: Going offline. Goodbye.")
        break
    else:
        print("VORIS: I don't know how to handle that yet.")