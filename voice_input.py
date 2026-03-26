import speech_recognition as sr

def listen():
    """
    Listen to microphone input and return lowercase text.
    Fallbacks to empty string if recognition fails.
    """
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎙️ Celeste is listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        try:
            text = r.recognize_google(audio)
            print("You:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Could not request results; {e}")
            return ""
    except Exception as e:
        print(f"⚠️ Microphone error: {e}")
        return ""
