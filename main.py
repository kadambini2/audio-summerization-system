from voice_input import listen
from text_to_speech import speak
from brain_gemini import think
from actions import (
    parse_and_send_email,
    parse_and_play_youtube,
    get_weather_today,
    parse_and_send_whatsapp,
    open_gmail,
    open_whatsapp,
    open_github,
    get_current_time,
    google_search,
    parse_google_search
)
from config import ASSISTANT_NAME

speak(f"Hello. I am {ASSISTANT_NAME}. How can I help you today?")

while True:
    mode = input("V = Voice | T = Text: ").lower()
    command = listen() if mode == "v" else input("⌨️ You: ").lower()

    if not command:
        continue

    if "exit" in command or "bye" in command:
        speak("Goodbye. Have a nice day.")
        break

    # -------- IDENTITY --------
    if "your name" in command or "who are you" in command:
        speak(f"My name is {ASSISTANT_NAME}. I am your personal AI assistant.")
        continue

    # -------- TIME --------
    if "time" in command or "what time is it" in command:
        speak(get_current_time())
        continue

    # -------- WEATHER --------
    if "weather" in command:
        speak(get_weather_today())
        continue

    # -------- OPEN GITHUB --------
    if "open" in command and "github" in command:
        open_github()
        speak("Opening GitHub.")
        continue

    # -------- GOOGLE SEARCH --------
    if "search" in command or ("google" in command and "open" not in command):
        query = parse_google_search(command)
        if query:
            google_search(query)
            speak(f"Searching Google for {query}.")
        else:
            speak("What would you like me to search for?")
        continue

    # -------- OPEN GMAIL --------
    if "open" in command and "gmail" in command:
        open_gmail()
        speak("Opening Gmail.")
        continue

    # -------- EMAIL --------
    if "send" in command and "email" in command:
        if parse_and_send_email(command):
            speak("Email sent successfully.")
        else:
            speak("Please say: send email containing your message to email address")
        continue

    # -------- WHATSAPP --------
    # OPEN WHATSAPP
    if "open whatsapp" in command:
        speak("Opening WhatsApp.")
        open_whatsapp()
        continue

    # SEND WHATSAPP MESSAGE
    if "whatsapp" in command and "to" in command:
        if parse_and_send_whatsapp(command):
            speak("WhatsApp message sent.")
        else:
            speak("Please say: send whatsapp message hi to mom")
        continue

    # -------- YOUTUBE --------
    if command.startswith("play"):
        if parse_and_play_youtube(command):
            speak("Playing on YouTube.")
        else:
            speak("I could not find the song.")
        continue

    # -------- CONVERSATIONAL AI (like Gemini) --------
    # Let Gemini handle all other queries naturally
    reply = think(command)
    speak(reply)
