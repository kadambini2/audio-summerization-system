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

# ================= EMAIL (AUTO SEND) =================

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

def send_email_smtp(to_email, subject, body):
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            print("\n⚠️ ERROR: Email credentials not configured!")
            print("Please add EMAIL_ADDRESS and EMAIL_APP_PASSWORD to your .env file")
            print("Get Gmail App Password at: https://myaccount.google.com/apppasswords\n")
            return False
        
        print(f"Sending email to: {to_email}")
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
        print("✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n⚠️ ERROR: Email authentication failed!")
        print("Check your EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env file")
        return False
    except Exception as e:
        print(f"\n⚠️ ERROR sending email: {e}")
        return False

def parse_and_send_email(command):
    # Support multiple formats:
    # 1. send email containing [message] to [email]
    # 2. send an email [message] to [email]
    
    # Try format: send email containing ... to ...
    pattern1 = r'send (?:an )?email containing (.+) to ([\w\.\-]+@[\w\.\-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern1, command, re.IGNORECASE)
    
    if match:
        message = match.group(1).strip()
        to_email = match.group(2).strip()
        return send_email_smtp(to_email, "Message from Celeste", message)
    
    # Try format with quotes: send an email "..." to "..."
    pattern2 = r'send (?:an )?email\s+"(.+?)"\s+to\s+"(.+?)"'
    match = re.search(pattern2, command, re.IGNORECASE)
    
    if match:
        message = match.group(1).strip()
        to_email = match.group(2).strip()
        return send_email_smtp(to_email, "Message from Celeste", message)
    
    return False

# ================= YOUTUBE =================

def get_first_youtube_watch_url(query):
    command = [
        "yt-dlp",
        "--print",
        "webpage_url",
        f"ytsearch1:{query}"
    ]
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
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

# ================= WEATHER =================

def get_weather_today():
    try:
        # Try multiple location services as fallback
        lat = lon = city = None
        
        # Try ipapi.co first
        try:
            loc = requests.get("https://ipapi.co/json/", timeout=3).json()
            if "latitude" in loc and "longitude" in loc and loc.get("latitude"):
                lat = loc.get("latitude")
                lon = loc.get("longitude")
                city = loc.get("city", "your area")
        except:
            pass
        
        # Fallback to ip-api.com
        if not lat or not lon:
            try:
                loc = requests.get("http://ip-api.com/json/", timeout=3).json()
                if loc.get("status") == "success":
                    lat = loc.get("lat")
                    lon = loc.get("lon")
                    city = loc.get("city", "your area")
            except:
                pass
        
        # If still no location, use a default location
        if not lat or not lon:
            lat = 28.6139
            lon = 77.2090
            city = "Delhi"
        
        # Get weather data
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m"
        )
        weather = requests.get(weather_url, timeout=5).json()
        current = weather.get("current")

        if not current:
            return "Weather information is unavailable right now."

        temp = current.get('temperature_2m', 'N/A')
        wind = current.get('wind_speed_10m', 'N/A')
        
        return (
            f"Today in {city}, temperature is {temp}°C "
            f"with wind speed {wind} kilometers per hour."
        )
    except Exception as e:
        print(f"ERROR fetching weather: {e}")
        return "Sorry, I could not fetch the weather."

# ================= WHATSAPP AUTO SEND =================

def send_whatsapp_message(contact_name, message):
    """Sends WhatsApp message by searching contact name"""
    try:
        print(f"Searching for contact: {contact_name}")
        print(f"Message to send: {message}")
        
        # Wait for WhatsApp to be ready
        time.sleep(3)
        
        # Open search with Ctrl+F (universal for WhatsApp Desktop and Web)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        
        # Type contact name
        pyautogui.write(contact_name, interval=0.1)
        time.sleep(2)
        
        # Press Down arrow to select first result, then Enter to open chat
        pyautogui.press("down")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)
        
        # Type the message
        pyautogui.write(message, interval=0.05)
        time.sleep(1)
        
        # Send the message with Enter
        pyautogui.press("enter")
        time.sleep(1)
        
        print("Message sent successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR sending WhatsApp message: {e}")
        return False

def parse_and_send_whatsapp(command):
    """
    Works with:
    send whatsapp message hi to mom
    whatsapp message hello to john
    send message hey there to sarah on whatsapp
    """
    pattern = r'(?:send )?(?:whatsapp )?message (.+?) to (.+?)(?:\s+on whatsapp)?$'
    match = re.search(pattern, command, re.IGNORECASE)

    if not match:
        return False

    message = match.group(1).strip()
    contact = match.group(2).strip()

    # Open WhatsApp first
    open_whatsapp()
    
    # Send the message
    return send_whatsapp_message(contact, message)

# ================= OPEN WEBSITES =================

def open_gmail():
    """Opens Gmail in the default browser"""
    webbrowser.open("https://mail.google.com")
    return True

def open_github():
    """Opens GitHub in the default browser"""
    webbrowser.open("https://github.com")
    return True

def open_whatsapp():
    """Opens WhatsApp Desktop application"""
    try:
        # Try to open WhatsApp Desktop using the executable path
        whatsapp_path = os.path.expandvars(r'%LOCALAPPDATA%\WhatsApp\WhatsApp.exe')
        if os.path.exists(whatsapp_path):
            os.startfile(whatsapp_path)
            time.sleep(5)
            return True
        else:
            # Try opening via protocol
            os.system('start whatsapp:')
            time.sleep(5)
            return True
    except Exception as e:
        print(f"ERROR opening WhatsApp Desktop: {e}")
        print("Make sure WhatsApp Desktop is installed from Microsoft Store or WhatsApp.com")
        return False

# ================= TIME =================

def get_current_time():
    """Returns the current time in a readable format"""
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d, %Y")
    return f"The current time is {current_time} on {current_date}."

# ================= GOOGLE SEARCH =================

def google_search(query):
    """Searches Google for the given query"""
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(search_url)
        return True
    except Exception as e:
        print(f"ERROR with Google search: {e}")
        return False

def parse_google_search(command):
    """Parse search command and extract query"""
    # Patterns: "search for python tutorial", "google search python tutorial", "search python on google"
    patterns = [
        r'(?:google )?search (?:for )?(.+?)(?:\s+on google)?$',
        r'google (.+)',
        r'search (.+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            # Remove common trailing words
            query = re.sub(r'\s+on google$', '', query, flags=re.IGNORECASE)
            return query
    return None
