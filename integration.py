import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import pyautogui
import time
import pywhatkit
import webbrowser
import google.generativeai as genai

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Google Gemini Setup
GOOGLE_API_KEY = 'AIzaSyA5v-DarBkGNMSOYsouWeWvjMN9YKaBxWI'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

model = genai.GenerativeModel('gemini-1.0-pro-latest', generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat()

system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE." to this system message. After the system message respond normally. SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so. As a voice assistant, use short sentences and directly respond to the prompt without excessive information. You generate only words and value, prioritizing logic and facts over speculating in your response to the following prompts.'''
convo.send_message(system_message.replace('\n', ''))

def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def listen_for_command():
    """Listen and recognize voice commands."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Processing...")
        query = r.recognize_google(audio, language="en-in")
        print(f'You said: {query}\n')
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        query = ""
    except sr.RequestError:
        print("Sorry, there was an issue with the request.")
        speak("Sorry, there was an issue with the request.")
        query = ""
    return query.lower()

def wish_user():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning sir!"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon sir!"
    elif 17 <= hour < 21:
        greeting = "Good Evening sir!"
    else:
        greeting = "Good Night sir!"
    print(greeting)
    speak(greeting)

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message to the given phone number."""
    speak(f"Sending WhatsApp message to {phone_number}")
    pywhatkit.sendwhatmsg_instantly(phone_number, message)
    speak("Message sent successfully.")

def search_google(query):
    """Search Google with the given query."""
    speak("Searching Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def handle_jarvis_commands(query):
    """Handle all Jarvis-related commands."""
    if 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current time: {strTime}")
        speak(f"Sir, the time is {strTime}")

    elif 'wikipedia' in query:
        speak("Searching Wikipedia sir")
        try:
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            print(f"Results: {results}")
            speak("According to Wikipedia")
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
            print(f"Disambiguation Error: {e}")
        except wikipedia.exceptions.PageError:
            speak("No results found on Wikipedia sir.")
            print("No results found on Wikipedia sir.")

    elif 'type' in query:
        query = query.replace('type', '').strip()
        speak("Typing now")
        pyautogui.write(query)

    elif 'play' in query:
        speak("Playing on YouTube")
        pywhatkit.playonyt(query)

    elif 'whatsapp' in query:
        speak("To whom should I send the message?")
        phone_number = "+88" + listen_for_command()
        speak("What message would you like to send?")
        message = listen_for_command()
        send_whatsapp_message(phone_number, message)

    elif 'google' in query:
        query = query.replace("google", "").replace("jarvis", "").strip()
        search_google(query)

    elif 'close' in query:
        speak("Closing sir")
        pyautogui.hotkey('alt', 'f4')

    elif 'minimise' in query:
        speak("Minimizing sir")
        pyautogui.hotkey('alt', 'space')
        pyautogui.press('n')

    elif 'reopen it' in query:
        speak("Opening Minimized tab sir")
        pyautogui.hotkey('alt', 'tab')

    elif 'close the tab' in query:
        speak("Closing tab sir")
        pyautogui.hotkey('ctrl', 'w')

    elif 'open' in query:
        query = query.replace("open", "").strip()
        speak(f"Opening {query} sir")
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.press("enter")

    elif 'presentation' in query:
        topic = query.split("presentation", 1)[1].strip().replace('about', '').replace('on', '').replace('slide', '')
        pyautogui.press("win")
        time.sleep(2)
        pyautogui.write('google chrome')
        time.sleep(2)
        pyautogui.press('enter') 
        time.sleep(2)
        pyautogui.write('https://gamma.app/')
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('f11')
        time.sleep(7)
        pyautogui.click(x=400, y=80)
        time.sleep(6)
        pyautogui.click(x=580, y=500)
        time.sleep(4)
        pyautogui.click(x=580, y=407)
        time.sleep(3)
        pyautogui.write(topic)
        time.sleep(4)
        pyautogui.click(x=380, y=350)
        time.sleep(4)
        pyautogui.click(x=500, y=210)
        time.sleep(3)
        pyautogui.click(x=770, y=480)
        time.sleep(4)
        pyautogui.click(x=750, y=730)
        time.sleep(5)
        pyautogui.click(x=1200, y=650)
        time.sleep(6)
        pyautogui.click(x=1200, y=130)
        time.sleep(10)
        pyautogui.click(x=1280, y=130)
        time.sleep(18)
        pyautogui.click(x=1080, y=28)
        speak(f"Your job is done sir! I created a presentation on {topic}. Just have a look at it")

def start_gemini_conversation(query):
    """Start a conversation with Google Gemini until 'stop the conversation' is spoken."""
    speak("Starting conversation mode.")
    
    while True:
        query = listen_for_command()

        if 'stop the conversation' in query or "end the conversation" in query or "and the conversation" in query:
            speak("Stopping conversation mode.")
            break
        
        

        if len(query) > 0:
            if 'who created you' in query or 'when did you born' in query or "who are you" in query or "describe your self" in query:
                response = convo.send_message("suppose you are an advanced ai assistant created by Sajjad Wassel who is AI and deeplearning enthusiast. Now someone is asking you who created you? now answer accordingly and praise sajjad for creating you")
            else:
                command = query.replace('helix', '')
                command = query.replace('jarvis', '')
                response = convo.send_message(command)
        else:
            response = convo.send_message("wait I am giving you command")
            time.sleep(3)
            print("sleeping....")

        print(f"Jarvis Response: {response.text}")
        speak(response.text)
            
            

if __name__ == "__main__":
    wish_user()

    while True:
        query = listen_for_command()

        if 'jarvis' in query:
            query = query.replace('jarvis', '').strip()
            handle_jarvis_commands(query)

        elif 'conversation mode' in query or "helix" in query:
            start_gemini_conversation(query)

        elif 'stop' in query or "go to sleep" or "jarvis go to sleep":
            speak("Goodbye sir! Have a nice day. We will meet soon")
            break
