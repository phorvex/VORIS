def extract_facts(text, remember_func, recall_func, save_func):
    text_lower = text.lower()
    
    patterns = [
        (["i live in", "i'm from", "i am from", "i stay in"], "location"),
        (["i am ", "i'm "], "identity_hint"),
        (["i like ", "i love ", "i enjoy "], "preference"),
        (["i work on", "i'm working on", "i am working on"], "current_project"),
        (["my name is"], "name"),
    ]
    
    for triggers, key in patterns:
        for trigger in triggers:
            if trigger in text_lower:
                value = text_lower.split(trigger)[1].strip()
                value = value.split(".")[0].split(",")[0].strip()
                if value and len(value) < 100:
                    remember_func(key, value)
                    save_func()
                    return key
    return None