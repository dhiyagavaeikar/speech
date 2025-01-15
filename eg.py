import streamlit as st

def speech_to_text():
    """
    A function to handle audio input in Streamlit and display the audio.
    """
    st.title("Speech-to-Text Demo")
    st.write("Record a voice message below:")

    # Create an audio input widget
    audio_value = st.audio_input("Record a voice message")

    if audio_value is not None:
        st.write("Audio received!")
        st.audio(audio_value, format='audio/wav')
    else:
        st.write("No audio data received. Please record a message.")

# Call the function to run in Streamlit
if __name__ == "__main__":
    speech_to_text()
