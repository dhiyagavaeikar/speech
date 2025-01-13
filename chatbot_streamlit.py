import streamlit as st
import google.generativeai as genai
import re
import logging

# Suppress non-critical warnings
logging.getLogger('streamlit').setLevel(logging.CRITICAL)

# Initialize the Google GenAI API with your key
genai.configure(api_key="AIzaSyDFJ_Cz2xvOwz9TaAn62rDn1LkzbARWvYU")

# Set up the generation configuration with max output tokens of 100
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 1,
    "max_output_tokens": 100,  # Limit tokens for concise responses
}

# Create the generative model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config)

# Streamlit UI
st.title("AI Chatbot Assistant")

# Start a session state to store the conversation history
if "history" not in st.session_state:
    st.session_state.history = []
    # Initial AI greeting message
    st.session_state.history.append({"role": "AI Assistant", "content": "Hello, I am your Assistant. How can I help you today?"})

# Display conversation history
for message in st.session_state.history:
    st.markdown(f"**{message['role']}**: {message['content']}")

# User input field
user_input = st.text_input("You:", "")

if user_input:
    # Add user message to the history
    st.session_state.history.append({"role": "You", "content": user_input})

    # Prepare prompt for the AI model
    prompt = f"You are an expert AI Assistant. Respond to the following: {user_input}"

    # Get the response from the AI model
    response = model.generate_content(prompt).text

    # Add AI response to the history
    st.session_state.history.append({"role": "AI Assistant", "content": response})

    # Display the AI response
    st.markdown(f"**AI Assistant**: {response}")

    # Clear the input field after submission
    st.session_state.user_input = ""  # Clear the text input field

# Run the Streamlit app with: streamlit run chatbot.py
