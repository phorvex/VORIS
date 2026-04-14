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
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull, 2)
        os.close(devnull)
        with sr.Microphone() as source:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None