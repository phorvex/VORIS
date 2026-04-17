import speech_recognition as sr
import threading

mic_enabled = False
wake_word_enabled = False
recognizer = sr.Recognizer()
wake_recognizer = sr.Recognizer()
wake_callback = None

def get_best_mic():
    try:
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            if "usb" in name.lower() or "composite" in name.lower():
                return i
        return None
    except:
        return None

def enable_mic():
    global mic_enabled
    mic_enabled = True
    return "Mic enabled. I'm listening."

def disable_mic():
    global mic_enabled
    mic_enabled = False
    return "Mic disabled."

def is_mic_on():
    return mic_enabled

def listen():
    if not mic_enabled:
        return None
    try:
        mic_index = get_best_mic()
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None

def wake_word_listener(callback):
    global wake_callback
    wake_callback = callback
    mic_index = get_best_mic()
    while wake_word_enabled:
        try:
            with sr.Microphone(device_index=mic_index) as source:
                wake_recognizer.energy_threshold = 300
                wake_recognizer.dynamic_energy_threshold = False
                audio = wake_recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = wake_recognizer.recognize_google(audio).lower()
                if "voris" in text:
                    callback()
        except:
            pass

def enable_wake_word(callback):
    global wake_word_enabled
    wake_word_enabled = True
    t = threading.Thread(target=wake_word_listener, args=(callback,), daemon=True)
    t.start()
    return "Wake word enabled. Say 'Hey VORIS' to activate me."

def disable_wake_word():
    global wake_word_enabled
    wake_word_enabled = False
    return "Wake word disabled."

def is_wake_word_on():
    return wake_word_enabled