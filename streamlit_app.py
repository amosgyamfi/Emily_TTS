from pathlib import Path
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Emily TTS", layout="wide")

# Initialize OpenAI client with API key from environment variables
client = OpenAI()  # OpenAI client will automatically use OPENAI_API_KEY from environment

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

# UI Components
st.title("Emily TTS")

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
    with st.spinner("Generating speech..."):
        audio_file = generate_speech(text_input, voice_input, tone_input)
        st.audio(audio_file, format="audio/mp3")
