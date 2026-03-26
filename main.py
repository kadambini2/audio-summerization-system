import streamlit as st
from actions import (
    parse_and_send_email,
    parse_and_play_youtube,
    get_weather_today,
    get_current_time,
    parse_google_search,
    google_search
)
from gtts import gTTS
import os

ASSISTANT_NAME = "Celeste"

# ----------------- STREAMLIT LAYOUT -----------------
st.title(f"{ASSISTANT_NAME} - AI Assistant")
st.write("Type a command below and see the assistant respond.")

# User input
command = st.text_input("Enter your command here:")

if command:
    response_text = ""

    # -------- EXIT --------
    if any(x in command.lower() for x in ["exit", "bye", "quit"]):
        response_text = "Goodbye. Have a nice day."

    # -------- IDENTITY --------
    elif "your name" in command.lower() or "who are you" in command.lower():
        response_text = f"My name is {ASSISTANT_NAME}. I am your AI assistant."

    # -------- TIME --------
    elif "time" in command.lower():
        response_text = get_current_time()

    # -------- WEATHER --------
    elif "weather" in command.lower():
        response_text = get_weather_today()

    # -------- GOOGLE SEARCH --------
    elif "search" in command.lower() or ("google" in command.lower() and "open" not in command.lower()):
        query = parse_google_search(command)
        if query:
            google_search(query)
            response_text = f"Searching Google for: {query}"
        else:
            response_text = "I could not understand your search query."

    # -------- EMAIL --------
    elif "send" in command.lower() and "email" in command.lower():
        if parse_and_send_email(command):
            response_text = "Email sent successfully."
        else:
            response_text = "Failed to send email. Format: send email containing <message> to <email>"

    # -------- YOUTUBE --------
    elif command.lower().startswith("play"):
        url = parse_and_play_youtube(command)
        if url:
            response_text = f"Playing on YouTube: {url}"
        else:
            response_text = "Could not find the content on YouTube."

    else:
        response_text = f"I am not sure how to handle that. You said: {command}"

    # Display response
    st.text_area("Assistant:", value=response_text, height=150)

    # Optional: Speak response using gTTS
    try:
        tts = gTTS(text=response_text, lang="en")
        tts_file = "response.mp3"
        tts.save(tts_file)
        audio_file = open(tts_file, "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        os.remove(tts_file)
    except Exception as e:
        st.warning(f"TTS Error: {e}")
