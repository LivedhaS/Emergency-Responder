import streamlit as st
from voice.main import provide_first_aid, listen_for_command, speak

st.set_page_config(page_title="Voice-Based First Aid Assistant", page_icon="🩺")
st.title("🎤 Voice-Based First Aid Assistant")

st.write("""
Say an emergency like:  
- **"burn"** or **"first aid"** to classify burn severity (**mild**, **moderate**, or **severe**)  
- Or directly say emergencies like **"fracture"**, **"bleeding"**, **"choking"**, **"unconscious"**
""")

st.subheader("🔊 Click to start voice interaction")

if st.button("Start Listening"):
    speak("How can I assist you?")
    command = listen_for_command()

    if command:
        st.success(f"✅ You said: {command}")

        # Emergency mode
        if "emergency" in command:
            speak("Activating emergency mode.")
            st.error("🚨 Emergency Alert Activated!")

        # Burn-specific flow
        elif "first aid" in command or "burn" in command:
            speak("Please specify the burn severity: mild, moderate, or severe.")
            st.info("🎤 Listening for burn severity level...")
            severity = listen_for_command()

            if severity:
                st.success(f"✅ You said: {severity}")
                instructions = provide_first_aid(severity)
                st.text_area("🩹 First Aid Instructions", value=instructions.strip(), height=200)
            else:
                speak("No severity level detected. Please try again.")
                st.warning("⚠️ No severity detected.")

        # Other emergencies
        else:
            instructions = provide_first_aid(command)
            if "No first aid information" in instructions:
                speak("Sorry, I didn't understand. Please try again.")
                st.warning("❌ Unknown command.")
            else:
                st.text_area("🩹 First Aid Instructions", value=instructions.strip(), height=200)

    else:
        st.warning("⚠️ No command detected.")
