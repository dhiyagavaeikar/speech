import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import google.generativeai as genai
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
        .mic-icon {
            font-size: 50px;
            color: #0d6efd;
            cursor: pointer;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # AI speaks greeting
    greeting_text = "Hi! How can I help you today?"
    engine.say(greeting_text)
    engine.runAndWait()
    st.markdown(f'<div class="chat-box ai-message">{greeting_text}</div>', unsafe_allow_html=True)

    # Mic icon for recording
    if st.button("🎤 Click to Speak"):
        audio_data = record_audio()
        
        # Convert speech to text
        user_input = recognize_speech(audio_data)
        st.markdown(f'<div class="chat-box user-message">You said: {user_input}</div>', unsafe_allow_html=True)

        # Exit if user says "exit"
        if re.search(r'\b(exit|quit|bye)\b', user_input, re.IGNORECASE):
            goodbye_text = "Goodbye! It was nice talking to you."
            st.markdown(f'<div class="chat-box ai-message">{goodbye_text}</div>', unsafe_allow_html=True)
            engine.say(goodbye_text)
            engine.runAndWait()
            return

        # Prepare prompt for AI
        prompt = f"You are an expert AI Assistant. Respond to the following: {user_input}"

        try:
            # Get the AI's response
            response = model.generate_content(prompt).text
            st.markdown(f'<div class="chat-box ai-message">AI: {response}</div>', unsafe_allow_html=True)
            engine.say(response)
            engine.runAndWait()
        except ValueError:
            # Handle cases where the response is invalid
            error_message = "Sorry, I couldn't provide an answer for that request. Please try rephrasing."
            st.markdown(f'<div class="chat-box ai-message">{error_message}</div>', unsafe_allow_html=True)
            engine.say(error_message)
            engine.runAndWait()

# Run Streamlit chatbot
if __name__ == '__main__':
    chatbot_conversation()
