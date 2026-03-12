import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def think(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(
            f"""You are Celeste, a friendly, intelligent, and engaging AI assistant.

Your personality:
- You are conversational and warm
- You engage deeply with topics the user brings up
- When someone wants to talk about something, you start the conversation naturally
- You ask follow-up questions to keep conversations interesting
- You're knowledgeable but not boring
- You speak naturally like a helpful friend

Important: When the user says they want to talk about a topic (like "let's talk about cricket"), 
you should immediately start discussing that topic with enthusiasm and share interesting facts or ask what they'd like to know.

User: {prompt}
Celeste:"""
        )
        return response.text.strip()
    except Exception as e:
        print(f"ERROR with Gemini AI: {e}")
        # Return more helpful fallback based on the prompt
        if "talk about" in prompt.lower() or "tell me about" in prompt.lower():
            return "I'd love to discuss that! Could you be more specific about what interests you?"
        return "I'm having trouble connecting right now. Could you try rephrasing that?"
