import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pyautogui
import time
import pywhatkit
import webbrowser
import google.generativeai as genai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io

# ========== TTS SETUP ==========
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# ========== GEMINI SETUP ==========
GOOGLE_API_KEY = "AIzaSyAaqnmRvOb1faFP18_s9g1-5YWx1aMkNnE"
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat()

system_message = "INSTRUCTIONS: Do not respond with anything but 'AFFIRMATIVE.'..."
convo.send_message(system_message)

# ========== FUNCTIONS ==========
def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    buffer = io.BytesIO()
    wav.write(buffer, fs, audio)
    buffer.seek(0)
    return buffer

def listen_for_command():
    recognizer = sr.Recognizer()
    audio_buffer = record_audio()
    with sr.AudioFile(audio_buffer) as source:
        audio_data = recognizer.record(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio_data, language="en-in")
        print(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Could not request results; check your connection.")
        return ""
    return query.lower()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning sir!")
        speak("Good Morning sir!")
    elif 12 <= hour < 17:
        print("Good Afternoon sir!")
        speak("Good Afternoon sir!")
    elif 17 <= hour < 21:
        print("Good Evening sir!")
        speak("Good Evening sir!")
    else:
        print("Good Night sir!")
        speak("Good Night sir!")

def send_whatsapp_message(phone_number, message):
    speak(f"Sending WhatsApp message to {phone_number}")
    pywhatkit.sendwhatmsg_instantly(phone_number, message)
    speak("Message sent successfully.")

def search_google(query):
    speak("Searching Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def handle_jarvis_commands(query):
    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif "wikipedia" in query:
        speak("Searching Wikipedia")
        try:
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except:
            speak("No relevant Wikipedia results found.")

    elif "type" in query:
        speak("Typing now")
        pyautogui.write(query.replace("type", "").strip())

    elif "enter" in query:
        pyautogui.press("enter")
        speak("Pressed enter")

    elif "play" in query:
        speak("Playing on YouTube")
        pywhatkit.playonyt(query)

    elif "whatsapp" in query:
        speak("To whom should I send the message?")
        phone_number = "+88" + listen_for_command()
        speak("What is the message?")
        message = listen_for_command()
        send_whatsapp_message(phone_number, message)

    elif "google" in query:
        search_google(query.replace("google", "").strip())

    elif "close" in query:
        speak("Closing window")
        pyautogui.hotkey("alt", "f4")

    elif "minimise" in query:
        speak("Minimizing window")
        pyautogui.hotkey("alt", "space")
        pyautogui.press("n")

    elif "open" in query:
        app = query.replace("open", "").strip()
        speak(f"Opening {app}")
        pyautogui.press("win")
        pyautogui.write(app)
        time.sleep(2)
        pyautogui.press("enter")

def start_gemini_conversation():
    speak("Conversation mode on.")
    while True:
        query = listen_for_command()
        if "stop the conversation" in query:
            speak("Conversation mode off.")
            break
        elif any(x in query for x in ["who created you", "who are you"]):
            response = convo.send_message("Who created you?")
        else:
            response = convo.send_message(query)
        speak(response.text)

# ========== MAIN ==========
if __name__ == "__main__":
    wish_user()
    while True:
        query = listen_for_command()
        if "jarvis" in query:
            handle_jarvis_commands(query.replace("jarvis", ""))
        elif "conversation mode" in query or "helix" in query:
            start_gemini_conversation()
        elif "stop" in query or "sleep" in query:
            speak("Goodbye sir. Signing off.")
            break
