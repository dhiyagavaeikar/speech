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

# Function to initiate the conversation
def chatbot_conversation():
    print("Hello! I'm your AI Assistant. How can I help you today?")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check for exit command
        if re.search(r'\b(exit|quit|bye)\b', user_input, re.IGNORECASE):
            print("Goodbye! It was nice talking to you.")
            break
        
        # Prepare prompt
        prompt = f"You are an expert AI Assistant. Respond to the following: {user_input}"
        
        # Get the response from the AI model
        response = model.generate_content(prompt).text
        print(f"AI Assistant: {response}")

# Start the conversation
chatbot_conversation()
