import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import subprocess
import time
from collections import defaultdict

genai.configure(api_key="api_key_here")  # Replace with your API key
model = genai.GenerativeModel('gemini-2.5-pro')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print("Lucy:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, there was a problem with the speech service.")
            return ""

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Error:", e)
        return "I'm having trouble connecting to Gemini right now."

app_paths = {
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "valorant": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\VALORANT.lnk",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "spotify": r"C:\Users\Orrin\AppData\Roaming\Spotify\Spotify.exe",
    "vscode": r"D:\Microsoft VS Code\Code.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "discord": r"C:\Users\Orrin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc",
}

command_map = defaultdict(list)
command_map["firefox"] = ["open firefox", "launch firefox", "start firefox"]
command_map["valorant"] = ["open valorant", "launch valorant", "start valorant", "play valorant"]
command_map["notepad"] = ["open notepad", "launch notepad", "text editor"]
command_map["spotify"] = ["open spotify", "play music", "launch spotify"]
command_map["vscode"] = ["open code", "launch vscode", "open vs code", "start coding"]
command_map["calculator"] = ["open calculator", "launch calculator", "calc"]
command_map["discord"] = ["open discord", "open disc", "launch discord"]

def handle_command(command):
    if "shutdown" in command:
        speak("Shutting down your PC.")
        subprocess.Popen(["shutdown", "/s", "/t", "1"])
        return

    for app, triggers in command_map.items():
        if any(trigger in command for trigger in triggers):
            path = app_paths.get(app)
            if path:
                try:
                    subprocess.Popen([path])
                    speak(f"Opening {app}.")
                except Exception as e:
                    speak(f"Sorry, I couldn't open {app}.")
                    print(f"Error: {e}")
            else:
                speak(f"Path to {app} not set correctly.")
            return

    if command.strip() == "":
        return

    response = ask_gemini(command)
    speak(response)

def passive_listen_for_lucy():
    while True:
        trigger = listen()
        if "lucy" in trigger:
            speak("Yes?")
            return

speak("Lucy is online. Say 'Lucy' when you need me.")
try:
    while True:
        passive_listen_for_lucy()
        command = listen()
        handle_command(command)
        time.sleep(0.5)
except KeyboardInterrupt:
    speak("Goodbye!")
