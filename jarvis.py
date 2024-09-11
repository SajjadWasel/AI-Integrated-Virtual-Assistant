import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import pyautogui
import time

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

if __name__ == "__main__":
    wish_user()
    
    while True:
        query = listen_for_command()

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Current time: {strTime}")
            speak(f"Sir, the time is {strTime}")

# =================================================================
# Searches on Wikipidea Starts
# ==================================================================

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
# Searches on Wikipidea Ends
# ==================================================================


# =================================================================
# Note Taking Starts
# ==================================================================
        elif 'type' in query:
            query = query.replace('type', '').strip()
            speak("Typing now")
            pyautogui.write(query)

# =================================================================
# Note Taking Ends
# ==================================================================

# =================================================================
# App Opening Closing starts
# =================================================================

        elif 'close' in query:
            query = query.replace("close", "")
            speak("Closing sir")
            pyautogui.hotkey('alt', 'f4')
        
        elif 'minimise' in query:
            speak(f"Minimizing sir")
            pyautogui.hotkey('alt', 'space')
            pyautogui.press('n')

        elif 'reopen it' or 'go to vs code' in query:
            speak(f"Opening Minimized tab sir")
            pyautogui.hotkey('alt', 'tab')

        elif 'open' in query:
            query = query.replace("open", "")
            query = query.replace("jarvis", "")
            speak(f"Opening {query} sir")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.press("enter")

# =================================================================
# App Opening Closing ends
# =================================================================


# =================================================================
# Power Point Presentation Starts
# ==================================================================


        elif 'powerpoint' or 'presentation' in query:
            sentence = query

            topic = sentence.split("presentation", 1)[1].strip()
            topic = topic.replace('about', '')
            topic = topic.replace('on', '')
            topic = topic.replace('slide', '')


            pyautogui.press("win")
            time.sleep(1)
            pyautogui.write('google crome')
            time.sleep(1)
            pyautogui.press('enter') 
            time.sleep(2)
            pyautogui.write('https://gamma.app/')
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.press('f11')
            time.sleep(7)

            # =====Create New=====
            pyautogui.click(x=400, y=80)
            time.sleep(3)

            # =====Generate====
            pyautogui.click(x=580, y=500)
            time.sleep(3)

            # ======Write Topic======
            pyautogui.click(x=580, y=407)
            time.sleep(2)
            pyautogui.write('Physics Vector for class lecture')
            time.sleep(3) 
            pyautogui.click(x=770, y=480)
            time.sleep(3)


            # =======Select Slide Number=====
            pyautogui.click(x=850, y=80)
            time.sleep(1.4)
            pyautogui.click(x=850, y=290)
            time.sleep(3)



            pyautogui.click(x=750, y=730)
            time.sleep(4)
            pyautogui.click(x=1200, y=650)
            time.sleep(5)
            pyautogui.click(x=1200, y=130)


            time.sleep(10)
            pyautogui.click(x=1280, y=130)

            time.sleep(18)
            pyautogui.click(x=1080, y=28)

            speak(f"Your job is done sir! I created a presentation on {topic}. Just have a look at it")

    
# =================================================
# Power Point Presentation Ends
# =================================================


        elif 'stop' in query:
            speak("Goodbye sir!")
            break

