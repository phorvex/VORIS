import speech_recognition as sr
import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

mic_enabled = False
recognizer = sr.Recognizer()

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
        with sr.Microphone() as source:
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None