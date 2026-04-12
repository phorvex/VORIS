def extract_facts(text, remember_func, recall_func, save_func):
    text_lower = text.lower()
    
    patterns = [
        (["my birthday is", "my birth date is", "i was born on", "i was born in"], "birthday"),
        (["my name is"], "name"),
        (["my goal is", "my goals are"], "goal"),
        (["my favorite color is", "my favourite color is"], "favorite_color"),
        (["my favorite food is", "my favourite food is"], "favorite_food"),
        (["my favorite music is", "my favorite genre is"], "music"),
        (["my phone is", "my device is"], "device"),
        (["my job is", "i work as"], "job"),
        (["my hobby is"], "hobby"),
        (["i live in", "i'm from", "i am from", "i stay in"], "location"),
        (["i work on", "i'm working on", "i am working on"], "current_project"),
        (["i listen to"], "music"),
        (["i like ", "i love ", "i enjoy "], "preference"),
        (["i am ", "i'm "], "identity_hint"),
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