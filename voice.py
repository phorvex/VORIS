import edge_tts
import asyncio
import subprocess

VOICE = "en-US-AriaNeural"
voice_enabled = False

async def speak_async(text):
    try:
        communicate = edge_tts.Communicate(text, VOICE)
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