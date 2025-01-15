import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import time

# Streamlit app title and description
st.title("Live AI Chatbot Calling Demo")
st.write("The AI will ask questions, and you can respond using your microphone. The conversation will be displayed in real-time, and audio will play.")

# Function to convert text to speech (TTS)
def text_to_speech(text, output_file="output.mp3"):
    tts = gTTS(text)
    tts.save(output_file)
    return output_file

# Function to convert speech to text (STT)
def speech_to_text_from_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError:
        return "Error with the speech recognition service."
    except Exception as e:
        return f"Error: {str(e)}"

# List of AI questions
ai_questions = [
    "Hello! How are you doing today?",
    
]

# Function to display conversation in real-time
def display_conversation(ai_text, user_text=None):
    # AI's text on the left
    st.markdown(f"<div style='text-align: left; color: blue;'>AI: {ai_text}</div>", unsafe_allow_html=True)
    if user_text:
        # User's text on the right
        st.markdown(f"<div style='text-align: right; color: green;'>You: {user_text}</div>", unsafe_allow_html=True)

# Start conversation loop
for question in ai_questions:
    # Display AI's question and convert to speech
    display_conversation(question)
    ai_audio = text_to_speech(question)
    st.audio(ai_audio, format="audio/mp3")

    # Capture audio input from the user for response
    audio_uploaded_file = st.audio_input(f"Respond to: {question}", key=f"audio_input_{question}")

    if audio_uploaded_file:
        # Save the uploaded audio temporarily
        audio_file_path = "temp_audio.wav"
        with open(audio_file_path, "wb") as f:
            f.write(audio_uploaded_file.getvalue())  # Use .getvalue() to retrieve bytes

        # Process the user's audio input
        st.info("Processing your response...")
        user_text = speech_to_text_from_audio(audio_file_path)

        # Cleanup the temporary file
        os.remove(audio_file_path)

        # Display both AI and User's text in real-time
        if user_text:
            display_conversation(question, user_text)

            # Convert the recognized user response to speech and play it back
            response_audio = text_to_speech(user_text)
            st.audio(response_audio, format="audio/mp3")
            time.sleep(1)  # Simulate a pause before the next question