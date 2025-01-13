import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import google.generativeai as genai
import base64
import time
import re

# Initialize the Google GenAI API with your key
genai.configure(api_key="AIzaSyDFJ_Cz2xvOwz9TaAn62rDn1LkzbARWvYU")

# Set up the generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 1,
    "max_output_tokens": 100,  # Limit tokens for a concise response
}

# Create the generative model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config)

# Initialize text-to-speech engine (for AI speaking)
engine = pyttsx3.init()

# Function to record audio
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your input...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
    return audio_data

# Function to recognize speech from audio
def recognize_speech(audio_data):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, the speech recognition service is unavailable."

# Function to convert text to speech (AI speaking)
def text_to_speech(text):
    tts = gTTS(text)
    return tts

# Function to save audio and generate download link
def generate_audio_download_link(audio, filename="output.mp3"):
    audio.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'
    return href

# Streamlit Interface
def chatbot_conversation():
    # Streamlit header
    st.title("AI Chatbot with Voice Interaction")
    
    # AI speaks greeting
    greeting_text = "Hi! How can I help you today?"
    engine.say(greeting_text)
    engine.runAndWait()
    
    # Display AI greeting text on the UI
    st.write(greeting_text)
    
    # Start listening for user input immediately
    while True:
        st.write("Listening... Please speak into the microphone.")
        
        # Record user audio input
        audio_data = record_audio()

        # Convert speech to text
        user_input = recognize_speech(audio_data)
        st.write(f"You said: {user_input}")

        # Exit if user says "exit"
        if re.search(r'\b(exit|quit|bye)\b', user_input, re.IGNORECASE):
            goodbye_text = "Goodbye! It was nice talking to you."
            st.write(goodbye_text)
            engine.say(goodbye_text)
            engine.runAndWait()
            break

        # Prepare prompt for AI
        prompt = f"You are an expert AI Assistant. Respond to the following: {user_input}"

        # Get the AI's response
        response = model.generate_content(prompt).text
        st.write(f"AI: {response}")

        # Convert AI response to speech
        tts = text_to_speech(response)

        # Save and display the audio download link
        audio_link = generate_audio_download_link(tts)
        st.markdown(audio_link, unsafe_allow_html=True)

        # Optionally, use pyttsx3 for speaking to the user directly
        engine.say(response)
        engine.runAndWait()

# Run Streamlit chatbot
if __name__ == '__main__':
    chatbot_conversation()
