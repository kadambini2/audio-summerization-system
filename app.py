import streamlit as st
from actions import (
    parse_and_send_email,
    parse_and_play_youtube,
    get_weather_today,
    get_current_time,
    parse_google_search,
    google_search,
    think
)
from gtts import gTTS
import os

ASSISTANT_NAME = "Celeste"

st.title(f"{ASSISTANT_NAME} - AI Assistant")
st.write("Type a message below and I will respond:")

command = st.text_input("You:")

if command:
    command_lower = command.lower()
    response_text = ""

    # -------- HARD-CODED SHORTCUTS --------
    if "time" in command_lower:
        response_text = get_current_time()
    elif "weather" in command_lower:
        response_text = get_weather_today()
    elif "search" in command_lower or ("google" in command_lower and "open" not in command_lower):
        query = parse_google_search(command)
        if query:
            google_search(query)
            response_text = f"Searching Google for: {query}"
        else:
            response_text = think(command)  # fallback
    elif "send" in command_lower and "email" in command_lower:
        if parse_and_send_email(command):
            response_text = "Email sent successfully."
        else:
            response_text = "Failed to send email. Format: send email containing <message> to <email>"
    elif command_lower.startswith("play"):
        url = parse_and_play_youtube(command)
        if url:
            response_text = f"Playing on YouTube: {url}"
        else:
            response_text = think(command)  # fallback
    else:
        # -------- AI FALLBACK --------
        response_text = think(command)

    # Display response
    st.text_area(f"{ASSISTANT_NAME}:", value=response_text, height=150)

    # Optional: speak response using gTTS
    try:
        tts = gTTS(text=response_text, lang="en")
        tts_file = "response.mp3"
        tts.save(tts_file)
        audio_file = open(tts_file, "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        os.remove(tts_file)
    except Exception as e:
        st.warning(f"TTS Error: {e}")
