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


def safe_speak(text):
    try:
        speak(text)
    except Exception as e:
        print("TTS Error:", e)
        print(text)


safe_speak(f"Hello. I am {ASSISTANT_NAME}. How can I help you today?")

while True:
    try:
        mode = input("V = Voice | T = Text: ").lower().strip()

        # -------- INPUT --------
        if mode == "v":
            command = listen()
            if not command:
                print("⚠️ Voice failed, switching to text.")
                command = input("⌨️ You: ").lower()
        else:
            command = input("⌨️ You: ").lower()

        if not command:
            continue

        # -------- EXIT --------
        if any(x in command for x in ["exit", "bye", "quit"]):
            safe_speak("Goodbye. Have a nice day.")
            break

        # -------- IDENTITY --------
        elif "your name" in command or "who are you" in command:
            safe_speak(f"My name is {ASSISTANT_NAME}. I am your AI assistant.")

        # -------- TIME --------
        elif "time" in command:
            safe_speak(get_current_time())

        # -------- WEATHER --------
        elif "weather" in command:
            safe_speak(get_weather_today())

        # -------- OPEN GITHUB --------
        elif "open github" in command:
            open_github()
            safe_speak("Opening GitHub.")

        # -------- GOOGLE SEARCH --------
        elif "search" in command or ("google" in command and "open" not in command):
            query = parse_google_search(command)
            if query:
                google_search(query)
                safe_speak(f"Searching Google for {query}.")
            else:
                safe_speak("What would you like me to search for?")

        # -------- OPEN GMAIL --------
        elif "open gmail" in command:
            open_gmail()
            safe_speak("Opening Gmail.")

        # -------- EMAIL --------
        elif "send" in command and "email" in command:
            if parse_and_send_email(command):
                safe_speak("Email sent successfully.")
            else:
                safe_speak("Please say: send email containing your message to email address")

        # -------- WHATSAPP --------
        elif "open whatsapp" in command:
            open_whatsapp()
            safe_speak("Opening WhatsApp.")

        elif "whatsapp" in command and "to" in command:
            if parse_and_send_whatsapp(command):
                safe_speak("WhatsApp message sent.")
            else:
                safe_speak("Please say: send whatsapp message hi to mom")

        # -------- YOUTUBE --------
        elif command.startswith("play"):
            if parse_and_play_youtube(command):
                safe_speak("Playing on YouTube.")
            else:
                safe_speak("I could not find the content.")

        # -------- AI (Gemini fallback) --------
        else:
            reply = think(command)
            safe_speak(reply)

    except Exception as e:
        print("❌ Error:", e)
        safe_speak("Something went wrong. Please try again.")
