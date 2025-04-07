from pathlib import Path
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Emily TTS", layout="wide")

# UI Components
st.title("Emily TTS")

# API Key input in sidebar
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Initialize OpenAI client with API key from user input
client = None
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

def generate_speech(text, voice, tone):
    # Create file in current working directory
    output_path = Path("speech.mp3").absolute()
    
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        instructions=tone,
    ) as response:
        response.stream_to_file(output_path)
    
    return str(output_path)

# Text input
text_input = st.text_area(
    "Text to convert to speech",
    value="In virtual care every detail matters. Especially how you connect, drop calls, video lags or delay messages aren't just frustrating, they can be dangerous. We're here to help. Stream powers real-time communication for virtual care. Stream is the only platform that allows you to connect with your patients in real-time",
    height=150
)

# Two columns for voice and tone
col1, col2 = st.columns(2)

with col1:
    voice_input = st.selectbox(
        "Voice",
        options=["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"],
        index=9  # "shimmer" is at index 9
    )

with col2:
    tone_input = st.text_input(
        "Tone instructions",
        value="Speak in a cheerful and positive tone."
    )

# Generate button
if st.button("Generate Speech"):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        with st.spinner("Generating speech..."):
            try:
                audio_file = generate_speech(text_input, voice_input, tone_input)
                st.audio(audio_file, format="audio/mp3")
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")
                st.info("Make sure your API key has access to the TTS features.")
