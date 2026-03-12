import pyttsx3

engine = pyttsx3.init()

def set_female_voice():
    voices = engine.getProperty("voices")

    for voice in voices:
        voice_name = voice.name.lower()
        voice_id = voice.id.lower()

        # Try to match female voice keywords
        if (
            "female" in voice_name
            or "zira" in voice_name        # Windows female voice
            or "samantha" in voice_name   # macOS female voice
            or "woman" in voice_name
        ):
            engine.setProperty("voice", voice.id)
            return

    # Fallback: use second voice if exists
    if len(voices) > 1:
        engine.setProperty("voice", voices[1])

# Set female voice once
set_female_voice()

engine.setProperty("rate", 165)   # speaking speed (lower = calmer)
engine.setProperty("volume", 1.0) # max volume

def speak(text):
    print("🪐 Celeste:", text)
    engine.say(text)
    engine.runAndWait()
