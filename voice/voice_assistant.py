import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listens for a voice command and converts speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f" You said: {command}")
        return command
    except sr.UnknownValueError:
        print(" Sorry, I couldn't understand.")
        speak("Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print(" API Error.")
        speak("There was an issue connecting to the speech recognition service.")
        return None
