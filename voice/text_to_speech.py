import pyttsx3

engine = pyttsx3.init()

def speak_response(response):
    engine.say(response)
    engine.runAndWait()
