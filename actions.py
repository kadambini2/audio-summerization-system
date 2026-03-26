import re
import os
import requests
import subprocess
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
import openai

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ----------------- EMAIL -----------------
def send_email_smtp(to_email, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return False
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

def parse_and_send_email(command):
    pattern = r'send (?:an )?email containing (.+) to ([\w\.\-]+@[\w\.\-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return send_email_smtp(match.group(2), "Message from AI Assistant", match.group(1))
    return False

# ----------------- YOUTUBE -----------------
def get_first_youtube_watch_url(query):
    result = subprocess.run(
        ["yt-dlp", "--print", "webpage_url", f"ytsearch1:{query}"],
        capture_output=True, text=True, shell=True
    )
    if result.returncode != 0: return None
    return result.stdout.strip()

def parse_and_play_youtube(command):
    match = re.search(r'play (.+)', command)
    if not match: return None
    song = match.group(1).replace("on youtube", "").strip()
    url = get_first_youtube_watch_url(song)
    return url

# ----------------- WEATHER -----------------
def get_weather_today():
    try:
        loc = requests.get("https://ipapi.co/json/", timeout=3).json()
        lat, lon, city = loc.get("latitude"), loc.get("longitude"), loc.get("city")
        if not lat: lat, lon, city = 28.6139, 77.2090, "Delhi"
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true",
            timeout=5
        ).json()
        current = weather.get("current_weather", {})
        temp, wind = current.get("temperature", "N/A"), current.get("windspeed", "N/A")
        return f"Today in {city}, temperature is {temp}°C with wind speed {wind} km/h."
    except:
        return "Sorry, could not fetch weather."

# ----------------- TIME -----------------
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("The current time is %I:%M %p on %A, %B %d, %Y.")

# ----------------- GOOGLE SEARCH -----------------
def google_search(query):
    import urllib.parse
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(search_url)
    return search_url

def parse_google_search(command):
    patterns = [
        r'(?:google )?search (?:for )?(.+?)(?:\s+on google)?$',
        r'google (.+)',
        r'search (.+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            query = re.sub(r'\s+on google$', '', match.group(1).strip(), flags=re.IGNORECASE)
            return query
    return None

# ----------------- AI FALLBACK -----------------
def think(command):
    if not OPENAI_API_KEY:
        return "AI fallback unavailable. Please set your OpenAI API key."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": command}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Sorry, I cannot process that right now."
