import os
# import quote  # This line should be removed
from urllib.parse import quote  # Add this line instead
# import quote
import sqlite3
import struct
import subprocess
import time
import pyaudio
import pyautogui
import pywhatkit as kit
import webbrowser
import wikipedia
import eel
from playsound import playsound
import sys
from hugchat import hugchat

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.config import ASSISTANT_NAME
from engine.command import speak, speakwithout
from engine.helper import remove_words

con = sqlite3.connect("siri.db")
cursor = con.cursor()


#playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = r"frontend\\assets\\audio\\startSound.mp3"  # Raw string to avoid issues with backslashes

    playsound(music_dir)



def openCommand(query):
    query = query.replace(ASSISTANT_NAME , "")
    query = query.replace("open" , "")
    query = query.replace("siri open","")
    query = query.replace("can","")
    query = query.replace("you","")
    query = query.replace("please","")
    query.lower()


        
    app_name = query.strip()

    if ".com" in query or ".co.in" in query or ".org" in query:
        speak(f"Opening {query} sir, Please wait...")

        try:
          kit.search(query)
        except:
         speak("No speakable output available")


    elif app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        pyautogui.press("super")
                        pyautogui.sleep(0.5)
                        pyautogui.typewrite(query)
                        pyautogui.sleep(1)
                        pyautogui.press("enter")
                    except:
                        speak(f"Sorry sir i am unable to open {query}")
            else:
                speak("Opening "+query)
                try:
                    pyautogui.press("super")
                    pyautogui.sleep(0.5)
                    pyautogui.typewrite(query)
                    pyautogui.sleep(1)
                    pyautogui.press("enter")
                except:
                    speak(f"Sorry sir i am unable to open {query}")
        except:
            speak("Some thing went wrong")



dictapp1 ={"microsoft edge" : "msedge.exe","video" : "video" ,"command prompt":"cmd","notepad":"notepad","word":"winword","excel":"excel","chrome" or "google" or "google chrome":"chrome","vscode" or "vs code":"code","cmd" : "cmd" ,"CMD" : "cmd" ,"powerpoint":"powerpnt"}



def closeCommand(query):
    query = query.replace(ASSISTANT_NAME , "")
    query = query.replace("open" , "")
    query = query.replace("siri open","")
    query = query.replace("can","")
    query = query.replace("you","")
    query = query.replace("please","")
    query.lower()
    speak("closing sir, please wait..")
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        speak("All tabs closed")
    elif "two tab" in query or "2 tab" in query:
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        speak("All tabs closed")
    elif "three tab" in query or "3 tab" in query:
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        speak("All tabs closed")
    elif "four tab" in query or "4 tab" in query:
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        speak("All tabs closed")
    elif "five tab" in query or "5 tab" in query:
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "w")
        time.sleep(0.5)
        speak("All tabs closed")
    else:
        keys = list(dictapp1.keys())
        for app in keys:
            if app in query:
                os.system(f"taskkill /f /im {dictapp1[app]}.exe")



def playYoutube(query):
    query = query.replace("youtube search ", "")
    query = query.replace("youtube" , "")
    query = query.replace("search" , "")
    query = query.replace(ASSISTANT_NAME , "")
    speakwithout(f"Playing {query}'s video on youtube")
    kit.playonyt(query)




def search(query):
        query = query.replace(ASSISTANT_NAME , "")
        query = query.replace("google search", "")
        query = query.replace("search", "")
        query = query.replace("google", "")
        query = query.replace("on google", "")
        speakwithout("This is what i found on google")
        try:
          kit.search(query)
          try:
            result = wikipedia.summary(query,1)
            speak(result)
          except:
              speakwithout(f"No summary found about {query}")
        except:
         speak("No speakable output available")






import struct
import time
import pyaudio
import pvporcupine

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis" , "alexa" , "siri"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print(f"{ASSISTANT_NAME} hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Clean up resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# Finds contact
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    



def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(2)
    subprocess.run(full_command, shell=True)
    time.sleep(2)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    try:
        user_input = query.lower()
        # Ensure the path is cross-platform
        cookie_path = os.path.join("engine", "cookies.json")
        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        # Get the chatbot's response
        response =  chatbot.chat(user_input)


        if isinstance(response, str):
            # Limit the response to 30 words
            response_words = response.split()
            if len(response_words) > 30:
                response = ' '.join(response_words[:30]) + "..."
        else:
            response = str(response)  # Convert to string if it's another type

        print(response)
        speak(response)
        return response
    
    except Exception as e:
        print(f"Some error occurred: {e}")
        return None
