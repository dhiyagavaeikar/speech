import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import re
import logging
import os
# logging.basicConfig(level=logging.DEBUG)

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

# Function to play text-to-speech using gTTS
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")  # Use mpg321 to play the audio
    os.remove("response.mp3")  # Remove the temporary audio file

# Streamlit Interface
def chatbot_conversation():
    # Streamlit header
    st.title("AI Chatbot with Voice Interaction")
    
    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        .chat-box {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .user-message {
            background-color: #d1e7dd;
            color: #0f5132;
        }
        .ai-message {
            background-color: #e2e3e5;
            color: #41464b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # AI speaks greeting
    greeting_text = "Hi! How can I help you today?"
    speak_text(greeting_text)
    
    # Display AI greeting text on the UI
    st.markdown(f'<div class="chat-box ai-message">{greeting_text}</div>', unsafe_allow_html=True)
    
    # Start listening for user input immediately
    while True:
        st.write("Listening... Please speak into the microphone.")
        
        # Record user audio input
        audio_data = record_audio()

        # Convert speech to text
        user_input = recognize_speech(audio_data)
        st.markdown(f'<div class="chat-box user-message">You said: {user_input}</div>', unsafe_allow_html=True)

        # Exit if user says "exit"
        if re.search(r'\b(exit|quit|bye)\b', user_input, re.IGNORECASE):
            goodbye_text = "Goodbye! It was nice talking to you."
            st.markdown(f'<div class="chat-box ai-message">{goodbye_text}</div>', unsafe_allow_html=True)
            speak_text(goodbye_text)
            break

        # Prepare prompt for AI
        prompt = f"You are an expert AI Assistant. Respond to the following: {user_input}"

        # Get the AI's response
        response = model.generate_content(prompt).text
        st.markdown(f'<div class="chat-box ai-message">AI: {response}</div>', unsafe_allow_html=True)

        # Optionally, use gTTS for speaking to the user directly
        speak_text(response)

# Run Streamlit chatbot
if __name__ == '__main__':
    chatbot_conversation()
