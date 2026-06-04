import asyncio
import subprocess
import edge_tts

async def test():
    communicate = edge_tts.Communicate("Hello Phillippi, I am VORIS", "en-US-AriaNeural")
    await communicate.save("test_speech.mp3")
    result = subprocess.run(["mpg123", "-q", "test_speech.mp3"], capture_output=True)
    print("Return code:", result.returncode)
    print("Stderr:", result.stderr)

asyncio.run(test())