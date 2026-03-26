from gtts import gTTS
import os
import uuid

def speak(text):
    """
    Convert text to speech and play it if possible.
    Prints text as fallback.
    Returns the path to the generated mp3 file.
    """
    try:
        print("🪐 Celeste:", text)

        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        # Attempt to play audio locally
        os.system(f"mpg321 {filename} || start {filename} || afplay {filename}")

        return filename

    except Exception as e:
        print("TTS Error:", e)
        return None
