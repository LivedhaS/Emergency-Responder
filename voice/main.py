import speech_recognition as sr
import pyttsx3

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listen for user voice commands and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
            command = recognizer.recognize_google(audio)
            print(f"✅ Raw recognized: {command}")
            return command.lower().strip()
        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand. Please try again.")
            speak("Sorry, I couldn't understand. Please try again.")
            return ""
        except sr.RequestError:
            print("🔌 Network error. Check your internet connection.")
            speak("Network error. Please check your internet connection.")
            return ""

def provide_first_aid(keyword):
    """Provides first-aid instructions based on emergency keyword or burn severity."""
    keyword = keyword.lower().strip()

    # Normalize spoken digits to severity words
    if keyword in ["1", "one"]:
        keyword = "mild"
    elif keyword in ["2", "two"]:
        keyword = "moderate"
    elif keyword in ["3", "three"]:
        keyword = "severe"

    if keyword in ["mild"]:
        instructions = """
        First Aid for Mild Burns:
        1. Cool the burn under running water for at least 10 minutes.
        2. Remove any jewelry or tight items near the burn.
        3. Cover the burn with a sterile, non-stick bandage.
        4. Avoid applying butter or ointments.
        5. Take a pain reliever if needed.
        """
        speak("For mild burns, cool the area under running water, remove jewelry, and cover with a clean bandage.")

    elif keyword in ["moderate"]:
        instructions = """
        First Aid for Moderate Burns:
        1. Follow the steps for mild burns.
        2. If blisters form, do not pop them.
        3. Keep the burned area elevated to reduce swelling.
        4. Watch for signs of infection.
        5. Seek medical advice if pain persists.
        """
        speak("For moderate burns, follow mild burn steps and monitor for infection.")

    elif keyword in ["severe"]:
        instructions = """
        First Aid for Severe Burns:
        1. Call emergency services immediately.
        2. Do not remove burned clothing stuck to the skin.
        3. Cover with a cool, moist cloth.
        4. Keep the person warm and monitor breathing.
        5. Perform CPR if necessary.
        """
        speak("For severe burns, call emergency services and cover the burn with a moist cloth.")

    elif "fracture" in keyword:
        instructions = """
        First Aid for Fracture:
        1. Do not move the injured area.
        2. Immobilize with a splint if trained.
        3. Apply cold packs to reduce swelling.
        4. Elevate if possible and seek medical help.
        """
        speak("For fracture, keep the injured area still and apply cold packs.")

    elif "bleeding" in keyword:
        instructions = """
        First Aid for Bleeding:
        1. Apply firm pressure with a clean cloth.
        2. Raise the bleeding area if possible.
        3. Do not remove embedded objects.
        4. Seek emergency help if bleeding doesn't stop.
        """
        speak("For bleeding, apply pressure and elevate the area.")

    elif "choking" in keyword:
        instructions = """
        First Aid for Choking:
        1. Ask if the person can speak or cough.
        2. If not, perform abdominal thrusts (Heimlich maneuver).
        3. Call emergency services if choking persists.
        """
        speak("For choking, perform abdominal thrusts and call for help.")

    elif "unconscious" in keyword:
        instructions = """
        First Aid for Unconsciousness:
        1. Check for responsiveness.
        2. Call emergency services.
        3. Place in recovery position if breathing.
        4. Start CPR if not breathing.
        """
        speak("If someone is unconscious, check for breathing and call for help.")

    else:
        instructions = "No first aid information available for that command."
    
    print(f"🩹 Instructions for '{keyword}':\n", instructions)
    return instructions
