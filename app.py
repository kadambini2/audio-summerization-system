import streamlit as st
from PIL import Image
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

# ----------------- LOGO AND DESCRIPTION -----------------
col1, col2 = st.columns([1, 3])  # left: logo, right: text

with col1:
    logo = Image.open("logo.jpg")
    st.image(logo, width=150)

with col2:
    st.markdown(f"""
    # 🪐 {ASSISTANT_NAME} AI - Your Personal Voice Assistant

    Celeste is an intelligent AI assistant powered by Google's Gemini AI that can perform various tasks through voice or text commands. From sending emails and WhatsApp messages to searching Google and engaging in natural conversations, Celeste makes your daily tasks easier!
    """)

st.markdown("---")  # separator

# ----------------- USER INPUT -----------------
command = st.text_input("You:")

if command:
    command_lower = command.lower()
    response_text = ""

    # -------- SHORTCUTS --------
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
            response_text = think(command)
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
            response_text = think(command)
    else:
        # -------- AI FALLBACK --------
        response_text = think(command)

    # ----------------- DISPLAY RESPONSE -----------------
    st.text_area(f"{ASSISTANT_NAME}:", value=response_text, height=150)

    # ----------------- OPTIONAL TTS -----------------
    try:
        tts = gTTS(text=response_text, lang="en")
        tts_file = "response.mp3"
        tts.save(tts_file)
        audio_file = open(tts_file, "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        os.remove(tts_file)
    except Exception as e:
        st.warning(f"TTS Error: {e}")
