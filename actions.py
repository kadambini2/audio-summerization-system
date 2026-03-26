import re
import time
import os
import subprocess
import webbrowser
import smtplib
import requests
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# ----------------- EMAIL -----------------
def send_email_smtp(to_email, subject, body):
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            print("⚠️ Email credentials not configured!")
            return False
        
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def parse_and_send_email(command):
    pattern1 = r'send (?:an )?email containing (.+) to ([\w\.\-]+@[\w\.\-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern1, command, re.IGNORECASE)
    if match:
        return send_email_smtp(match.group(2), "Message from Celeste", match.group(1))
    
    pattern2 = r'send (?:an )?email\s+"(.+?)"\s+to\s+"(.+?)"'
    match = re.search(pattern2, command, re.IGNORECASE)
    if match:
        return send_email_smtp(match.group(2), "Message from Celeste", match.group(1))
    
    return False

# ----------------- YOUTUBE -----------------
def get_first_youtube_watch_url(query):
    result = subprocess.run(
        ["yt-dlp", "--print", "webpage_url", f"ytsearch1:{query}"],
        capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def parse_and_play_youtube(command):
    match = re.search(r'play (.+)', command)
    if not match:
        return False
    song = match.group(1).replace("on youtube", "").strip()
    url = get_first_youtube_watch_url(song)
    if not url:
        return False
    webbrowser.open(url)
    return True

# ----------------- WEATHER -----------------
def get_weather_today():
    try:
        lat = lon = city = None
        try:
            loc = requests.get("https://ipapi.co/json/", timeout=3).json()
            lat, lon, city = loc.get("latitude"), loc.get("longitude"), loc.get("city")
        except: pass
        if not lat:
            try:
                loc = requests.get("http://ip-api.com/json/", timeout=3).json()
                if loc.get("status") == "success":
                    lat, lon, city = loc.get("lat"), loc.get("lon"), loc.get("city")
            except: pass
        if not lat: lat, lon, city = 28.6139, 77.2090, "Delhi"
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m",
            timeout=5
        ).json()
        current = weather.get("current")
        if not current: return "Weather info unavailable."
        temp, wind = current.get("temperature_2m", "N/A"), current.get("wind_speed_10m", "N/A")
        return f"Today in {city}, temperature is {temp}°C with wind speed {wind} km/h."
    except Exception as e:
        return "Sorry, could not fetch weather."

# ----------------- WHATSAPP -----------------
def send_whatsapp_message(contact_name, message):
    try:
        time.sleep(3)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(contact_name, interval=0.1)
        time.sleep(2)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.write(message, interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"WhatsApp error: {e}")
        return False

def parse_and_send_whatsapp(command):
    pattern = r'(?:send )?(?:whatsapp )?message (.+?) to (.+?)(?:\s+on whatsapp)?$'
    match = re.search(pattern, command, re.IGNORECASE)
    if not match: return False
    message, contact = match.group(1).strip(), match.group(2).strip()
    open_whatsapp()
    return send_whatsapp_message(contact, message)

# ----------------- OPEN WEBSITES -----------------
def open_gmail(): webbrowser.open("https://mail.google.com"); return True
def open_github(): webbrowser.open("https://github.com"); return True
def open_whatsapp():
    try:
        whatsapp_path = os.path.expandvars(r'%LOCALAPPDATA%\WhatsApp\WhatsApp.exe')
        if os.path.exists(whatsapp_path): os.startfile(whatsapp_path); time.sleep(5); return True
        os.system('start whatsapp:'); time.sleep(5); return True
    except Exception as e: print(f"WhatsApp open error: {e}"); return False

# ----------------- TIME -----------------
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("The current time is %I:%M %p on %A, %B %d, %Y.")

# ----------------- GOOGLE SEARCH -----------------
def google_search(query):
    import urllib.parse
    try:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        return True
    except Exception as e: print(f"Google search error: {e}"); return False

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
