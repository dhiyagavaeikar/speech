import streamlit as st
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    # Use the microphone as the source of audio input
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        # Adjust for ambient noise and record the speech
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Use Google's speech recognition API
            st.info("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech service."

# Streamlit UI
def main():
    st.title("Speech-to-Text with Streamlit")
    st.write("Click the button below and start speaking to convert speech into text.")

    if st.button("Start Listening"):
        result = recognize_speech()
        st.success(f"You said: {result}")

if __name__ == "__main__":
    main()
