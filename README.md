# 🪐 Celeste AI - Your Personal Voice Assistant

Celeste is an intelligent AI assistant powered by Google's Gemini AI that can perform various tasks through voice or text commands. From sending emails and WhatsApp messages to searching Google and engaging in natural conversations, Celeste makes your daily tasks easier!

## ✨ Features

- 🎤 **Voice & Text Input** - Control Celeste using your voice or keyboard
- 🌤️ **Weather Updates** - Get current weather information for your location
- ⏰ **Time & Date** - Ask for current time and date
- 📧 **Email Sending** - Send emails via Gmail SMTP
- 💬 **WhatsApp Automation** - Send WhatsApp messages automatically
- 🎵 **YouTube Player** - Search and play YouTube videos
- 🔍 **Google Search** - Search anything on Google instantly
- 🌐 **Quick Access** - Open Gmail, GitHub, and WhatsApp with voice commands
- 🤖 **Natural Conversations** - Chat naturally with AI powered by Gemini

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Windows OS** (for WhatsApp Desktop automation)
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))
- **Gmail Account** with App Password (for email functionality)
- **Microphone** (for voice input)
- **WhatsApp Desktop** (for WhatsApp automation)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/celeste-ai.git
cd celeste-ai
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Additional Tools

**For YouTube functionality**, install yt-dlp:
```bash
pip install yt-dlp
```

**For voice input**, install PyAudio (may require additional setup):
```bash
pip install pyaudio
```

If PyAudio installation fails on Windows, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:
```bash
pip install PyAudio‑0.2.11‑cp312‑cp312‑win_amd64.whl
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
copy .env.example .env  # On Windows
# or
cp .env.example .env    # On Linux/Mac
```

Edit `.env` and add your credentials:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration (Optional - for email sending)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
```

#### 🔑 How to Get API Keys:

**Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste into `.env`

**Gmail App Password:**
1. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in to your Google account
3. Create an app password for "Mail"
4. Copy the 16-character password (no spaces)
5. Paste into `.env`

### Step 6: Install WhatsApp Desktop (Optional)

For WhatsApp automation, install WhatsApp Desktop:
- Download from [whatsapp.com/download](https://www.whatsapp.com/download)
- Or install from Microsoft Store

## 🎮 Usage

### Starting Celeste

```bash
python main.py
```

You'll be greeted by Celeste and prompted to choose input mode:
- Type `V` for Voice input
- Type `T` for Text input

### 📝 Command Examples

#### General Commands
```
"what time is it"
"tell me the weather"
"who are you"
"exit" or "bye"
```

#### Opening Applications
```
"open gmail"
"open github"
"open whatsapp"
```

#### Google Search
```
"search for python tutorial"
"google artificial intelligence"
"search cats on google"
```

#### YouTube
```
"play despacito"
"play python tutorial on youtube"
```

#### Email (requires configuration)
```
"send email containing hello world to someone@gmail.com"
```

#### WhatsApp (requires WhatsApp Desktop)
```
"send whatsapp message hello to mom"
"whatsapp message how are you to john"
```

#### Natural Conversations
```
"lets talk about cricket"
"tell me about space"
"what do you think about AI"
```

## 📁 Project Structure

```
celeste-ai/
├── main.py                 # Main entry point
├── actions.py              # Task automation functions
├── brain_gemini.py         # AI conversation handler
├── voice_input.py          # Voice recognition
├── text_to_speech.py       # Text-to-speech output
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Customizing Assistant Name

Edit `config.py` to change the assistant's name:

```python
ASSISTANT_NAME = "Celeste"  # Change to your preferred name
```

### Adjusting Voice Settings

Edit `text_to_speech.py` to customize voice properties:
- Voice rate (speed)
- Volume
- Voice type (male/female)

## 🐛 Troubleshooting

### Weather Not Working
- The app uses fallback location services
- If it fails, default location (Delhi) is used
- Check your internet connection

### Voice Input Not Working
- Ensure microphone is connected and enabled
- Install/update PyAudio
- Check microphone permissions in Windows settings

### Email Not Sending
- Verify `.env` has correct EMAIL_ADDRESS and EMAIL_APP_PASSWORD
- Ensure you're using a Gmail App Password, not regular password
- Check if "Less secure app access" is enabled (older accounts)

### WhatsApp Automation Issues
- Ensure WhatsApp Desktop is installed and logged in
- Don't interrupt the automation while it's running
- Contact names must match exactly as saved in WhatsApp

### YouTube Not Playing
- Install yt-dlp: `pip install yt-dlp`
- Check internet connection
- Some videos may be region-restricted

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) - Conversational AI
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Text-to-speech
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice input
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube integration

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review closed issues for solutions

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

Made with ❤️ by [Your Name]
