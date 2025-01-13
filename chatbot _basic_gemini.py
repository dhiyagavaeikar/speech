
import google.generativeai as genai
import re

# Initialize the Google GenAI API with your key
genai.configure(api_key="AIzaSyDFJ_Cz2xvOwz9TaAn62rDn1LkzbARWvYU")

# Set up the generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 1,
    "max_output_tokens": 512,  # Limit tokens since we don't need long responses
}


# Create the generative model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config)

prompt2 = (
    f"""You are an expert AI ASSistant whose task is to establish conversation
    """
)

feedback = model.generate_content(prompt2).text
print("feedback: ",feedback)