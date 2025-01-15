import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

# Speech to Text function using SpeechRecognition
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please say something:")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.write("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
            return None

# Text to Speech function using gTTS
def text_to_speech(text):
    if text:
        tts = gTTS(text=text, lang='en')
        tts_file = 'output.mp3'
        tts.save(tts_file)
        return tts_file
    return None

# Streamlit App
st.title("Speech to Text and Text to Speech App")

# Speech to Text button
if st.button('Convert Speech to Text'):
    text = speech_to_text()

    # If text conversion is successful, proceed to text to speech
    if text:
        tts_file = text_to_speech(text)
        if tts_file:
            # Play the audio using Streamlit
            audio_file = open(tts_file, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

# Optionally, provide an example text for conversion
st.write("You can also enter text below to convert to speech:")
user_input = st.text_input("Enter Text here:")
if st.button('Convert Text to Speech'):
    if user_input:
        tts_file = text_to_speech(user_input)
        if tts_file:
            audio_file = open(tts_file, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')