import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import pyautogui
import time
import pywhatkit
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

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




if __name__ == "__main__":
    wish_user()

    while True:
        query = listen_for_command()

        # The assistant will only respond if 'jarvis' is in the query
        if 'jarvis' in query:
            query = query.replace('jarvis', '').strip()  # Remove 'Jarvis' from the command

            if 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"Current time: {strTime}")
                speak(f"Sir, the time is {strTime}")

# =================================================================
# Wikipedia Search
# =================================================================

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

# =================================================================
# Note Taking
# =================================================================

            elif 'type' in query:
                query = query.replace('type', '').strip()
                speak("Typing now")
                pyautogui.write(query)

# =================================================================
# Youtube
# =================================================================
            elif 'play' in query: 
                speak("Playing on YouTube")
                pywhatkit.playonyt(query)




# =================================================================
# Whatsapp
# =================================================================

            elif 'whatsapp' in query:  
                speak("To whom should I send the message?")
                phone_number = "+88" + listen_for_command()
                speak("What message would you like to send?")
                message = listen_for_command()
                send_whatsapp_message(phone_number, message)



# =================================================================
# Google Search
# =================================================================
            elif 'google' in query:
                query = query.replace("google", "").replace("jarvis", "").strip()
                search_google(query)
            

# =================================================================
# App Management
# =================================================================

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

            elif 'open' in query:
                query = query.replace("open", "").strip()
                speak(f"Opening {query} sir")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.press("enter")

# =================================================================
# PowerPoint Presentation Creation
# =================================================================

            elif 'presentation' in query:
                topic = query.split("presentation", 1)[1].strip().replace('about', '').replace('on', '').replace('slide', '')

                pyautogui.press("win")
                time.sleep(2)
                pyautogui.write('google crome')
                time.sleep(2)
                pyautogui.press('enter') 
                time.sleep(2)
                pyautogui.write('https://gamma.app/')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('f11')
                time.sleep(7)

                # =====Create New=====
                pyautogui.click(x=400, y=80)
                time.sleep(6)

                # =====Generate====
                pyautogui.click(x=580, y=500)
                time.sleep(4)

                # ======Write Topic======
                pyautogui.click(x=580, y=407)
                time.sleep(3)
                pyautogui.write(topic)
                time.sleep(4) 

                # =======Select Slide Number=====

                pyautogui.click(x=380, y=350)
                time.sleep(4)
                pyautogui.click(x=500, y=210)
                time.sleep(3)

                pyautogui.click(x=770, y=480)
                time.sleep(4)


                # ====Generate after previewing slide number
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

# =================================================================
# Exit command
# =================================================================

            elif 'stop' in query:
                speak("Goodbye sir! Have a nice day.")
                break