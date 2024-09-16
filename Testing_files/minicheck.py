from newsdataapi import NewsDataApiClient
import pyautogui
import time



def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


api = NewsDataApiClient(apikey="pub_50175f551643637ca0f8739f7190a9ea16a0")


response = api.news_api(country = "bd")


first_article_title = response['results'][0]['title']
second_article_title = response['results'][1]['title']
third_article_title = response['results'][2]['title']
fourth_article_title = response['results'][3]['title']
fifth_article_title = response['results'][4]['title']


print(f"1: {first_article_title}")
print(f"2: {second_article_title}")
print(f"3: {third_article_title}")
print(f"4: {fourth_article_title}")
print(f"5: {fifth_article_title}")



pyautogui.press('win')
time.sleep(1)
pyautogui.write('notepad')
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)
pyautogui.write(f"Here is the summary of todays news of the country: {first_article_title}")

# pyautogui.write(f"1: {first_article_title}")
# pyautogui.write(f"2: {second_article_title}")
# pyautogui.write(f"3: {third_article_title}")
# pyautogui.write(f"4: {fourth_article_title}")
# pyautogui.write(f"5: {fifth_article_title}")







