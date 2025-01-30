import mysql.connector  # Import MySQL connector
import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import json
import re

# Initialize the Google GenAI API
genai.configure(api_key="AIzaSyDFJ_Cz2xvOwz9TaAn62rDn1LkzbARWvYU")

# Configure generation settings
generation_config = {
    "temperature": 0.6,
    "top_p": 0.9,
    "top_k": 1,
    "max_output_tokens": 300,
}

# Create generative model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition
recognizer = sr.Recognizer()

# Connect to MySQL Database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dhiya123",
        database="sim_support"
    )

# Function to save SIM provider to MySQL
def save_sim_provider(sim_provider):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sim (sim_provider) VALUES (%s)", (sim_provider,))
    conn.commit()
    conn.close()

# Function to record audio
def record_audio():
    with sr.Microphone() as source:
        print("Listening for your input...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
    return audio_data

# Function to recognize speech
def recognize_speech(audio_data):
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, the speech recognition service is unavailable."

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle chatbot conversation
def sim_support_chatbot():
    conversation_context = """
    You are a SIM card support assistant. Your name is Elle. Follow this flow while interacting with the user:
    1. Ask for the user's name.
    2. Ask for the user's SIM provider and always provide a list of details:
       - 1. Airtel
       - 2. Jio
       - 3. Vodafone Idea
    3. Ask for the mobile number.
    4. Ask about the issue they are facing and always provide a list of possible issues example:
       - 1. Network
       - 2. Billing
       - 3. Activation
    5. Based on the issue, ask follow-up questions to gather more details and provide a solution using options wherever possible.
    6. If the issue cannot be resolved, suggest escalating it to customer support.

    Be professional, friendly, and empathetic during the conversation. Always acknowledge the user's inputs before asking the next question.
    """
   
    conversation_history = []
    user_details = {"sim_provider": None}
    
    # Display chatbot title
    st.title("SIM Card Support Chatbot - Elle")
    
    # Initial chatbot message
    bot_message = "Hello! My name is Elle. I am a SIM card support assistant. Could you please tell me your name?"
    st.markdown(f'<div style="background-color: #d1e7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: 80%; margin-left: 0;">SIM Support Bot: {bot_message}</div>', unsafe_allow_html=True)
    text_to_speech(bot_message)
    conversation_history.append({"role": "bot", "message": bot_message})

    while True:
        # Record user input
        st.write("Listening... Please speak into the microphone.")
        audio_data = record_audio()
        user_input = recognize_speech(audio_data)
        st.markdown(f'<div style="background-color: #f8d7da; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: 80%; margin-left: auto;">You said: {user_input}</div>', unsafe_allow_html=True)

        # Exit condition
        if re.search(r'\b(exit|quit|bye)\b', user_input, re.IGNORECASE):
            goodbye_text = "Goodbye! It was nice talking to you."
            st.markdown(f'<div style="background-color: #d1e7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: 80%; margin-left: 0;">SIM Support Bot: {goodbye_text}</div>', unsafe_allow_html=True)
            text_to_speech(goodbye_text)
            break

        # Add user input to conversation history
        conversation_history.append({"role": "user", "message": user_input})

        # Extract SIM provider dynamically
        sim_providers = ["Airtel", "Jio", "Vodafone Idea"]
        for provider in sim_providers:
            if provider.lower() in user_input.lower():
                if user_details["sim_provider"] is None:  # Only save if not already saved
                    user_details["sim_provider"] = provider
                    save_sim_provider(provider)  # Save to MySQL
                    st.write(f"SIM provider '{provider}' saved successfully!")

        # Generate AI response
        prompt = conversation_context
        for turn in conversation_history:
            role = "User" if turn["role"] == "user" else "SIM Support Bot"
            prompt += f"\n{role}: {turn['message']}"

        prompt += "\nSIM Support Bot:"

        try:
            response = model.generate_content(prompt).text.strip()
        except ValueError:
            response = "I'm sorry, I encountered an issue generating a response. Let me try again."

        # Display bot response
        st.markdown(f'<div style="background-color: #d1e7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: 80%; margin-left: 0;">SIM Support Bot: {response}</div>', unsafe_allow_html=True)
        text_to_speech(response)

        # Add bot response to conversation history
        conversation_history.append({"role": "bot", "message": response})

# Run chatbot in Streamlit
if __name__ == '__main__':
    sim_support_chatbot()
