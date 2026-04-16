import speech_recognition as sr
import subprocess

mic_enabled = False
recognizer = sr.Recognizer()

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