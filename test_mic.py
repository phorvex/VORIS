import speech_recognition as sr

r = sr.Recognizer()
print("Say something...")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source, timeout=5)
    text = r.recognize_google(audio)
    print("Heard:", text)