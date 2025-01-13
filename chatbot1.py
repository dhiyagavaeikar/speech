import streamlit as st
import speech_recognition as sr
import pyttsx3
import spacy
import threading

# Initialize NLP model (spaCy)
nlp = spacy.load("en_core_web_sm")

# Initialize text-to-speech engine (pyttsx3)
engine = pyttsx3.init()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        st.write("There was an issue with the speech recognition service.")
        return None

# Function for generating a response based on user input
def generate_response(user_input):
    doc = nlp(user_input)
    
    # Simple responses based on user input
    if "hello" in user_input.lower():
        return "Hello! How can I assist you today?"
    elif "name" in user_input.lower():
        return "I am your friendly voice chatbot!"
    elif "goodbye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I didn't understand that."

# Function to speak the response in a separate thread
def speak_response(response):
    def speak():
        engine.say(response)
        engine.runAndWait()
    # Run the speech synthesis in a separate thread
    thread = threading.Thread(target=speak)
    thread.start()

# Streamlit app interface
st.title("Voice Chatbot with Streamlit")
st.write("Press the button below to start talking to the bot.")

if st.button("Start Chat"):
    # Recognize speech and process it
    user_input = recognize_speech()
    
    if user_input:
        # Generate response
        response = generate_response(user_input)
        st.write(f"Bot: {response}")
        
        # Speak the response
        speak_response(response)
