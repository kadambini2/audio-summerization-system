import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def think(prompt: str) -> str:
    """
    Sends the prompt to Google Gemini AI and returns the generated response.
    Includes fallback responses in case of errors.
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(
            f"""You are Celeste, a friendly, intelligent, and engaging AI assistant.

Your personality:
- Conversational and warm
- Engages deeply with topics
- Starts natural conversations when prompted
- Asks follow-up questions to keep discussions interesting
- Knowledgeable but approachable
- Speaks naturally like a helpful friend

User: {prompt}
Celeste:"""
        )
        return response.text.strip()

    except Exception as e:
        print(f"⚠️ ERROR with Gemini AI: {e}")
        # Fallback responses
        if "talk about" in prompt.lower() or "tell me about" in prompt.lower():
            return "I'd love to discuss that! Could you tell me more specifically what interests you?"
        return "I'm having trouble connecting right now. Could you try rephrasing that?"
