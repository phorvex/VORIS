import edge_tts
import asyncio
import subprocess
import platform
import tempfile
import os

VOICE = "en-US-AriaNeural"
voice_enabled = False

def fix_pronunciation(text):
    replacements = {
        "Phillippi": "Fee-LEE-pee",
        "phillippi": "Fee-LEE-pee",
        "PHILLIPPI": "Fee-LEE-pee",
    }
    for word, phonetic in replacements.items():
        text = text.replace(word, phonetic)
    return text

async def speak_async(text):
    text = fix_pronunciation(text)
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        if platform.system() == "Windows":
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tmp.close()
            await communicate.save(tmp.name)
            subprocess.run(["mpg123", tmp.name])
            os.unlink(tmp.name)
        else:
            await communicate.save("/tmp/voris_speech.mp3")
            subprocess.run(
                ["mpg123", "-q", "/tmp/voris_speech.mp3"],
                capture_output=True
            )
    except Exception as e:
        pass

def speak(text):
    if voice_enabled:
        asyncio.run(speak_async(text))

def enable_voice():
    global voice_enabled
    voice_enabled = True
    return "Voice enabled."

def disable_voice():
    global voice_enabled
    voice_enabled = False
    return "Voice disabled."

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    return "Voice enabled." if voice_enabled else "Voice disabled."