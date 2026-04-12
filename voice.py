import edge_tts
import asyncio
import subprocess
import os

VOICE = "en-US-AriaNeural"

async def speak_async(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("/tmp/voris_speech.mp3")
    subprocess.run(
        ["mpg123", "-q", "/tmp/voris_speech.mp3"],
        capture_output=True
    )

def speak(text):
    asyncio.run(speak_async(text))