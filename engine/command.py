import sys
import pyttsx3
import eel
import time
import speech_recognition as sr
import pywhatkit as kit






engine = pyttsx3.init() 
voices = engine.getProperty('voices')         #taking voices
# print(voices)                              
# print(voices[0].id)                              
engine.setProperty('voice', voices[1].id)     #taking voices(0 asnd 1) change it to change the voice
engine.setProperty('rate',174) #To slow down(0 - 100) and fast the voice speed(100 - 200)


@eel.expose
def speak(audio):
    audio = str(audio)
    eel.DisplayMessage(audio)
    engine.say(audio)                              #speak function
    eel.receiverText(audio)
    engine.setProperty('volume' , 1.0)
    engine.runAndWait()

def speakwithout(audio):
    audio = str(audio)
    engine.say(audio)                               #speak function
    eel.receiverText(audio)
    engine.setProperty('volume' , 1.0)
    engine.runAndWait()




def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:                #taking commands from user
        print("listening...")
        eel.DisplayMessage("listening...")
        r.pause_threshold = 0.9
        audio= r.listen(source)
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google (audio, language='en-in') 
        # query= r.recognize_google(audio, language='hi-in') 
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        # speak("say that again please...")
        return ""
    return query.lower()

def takecommandwithout():
    r = sr.Recognizer()
    with sr.Microphone() as source:                #taking commands from user
        print("listening...")
        r.pause_threshold = 0.9
        audio= r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google (audio, language='en-in') 
        # query= r.recognize_google(audio, language='hi-in') 
        print(f"User said: {query}")
        time.sleep(2)
    except Exception as e:
        # speak("say that again please...")
        return ""
    return query.lower()


@eel.expose
def inputBoxCommands(massage):
    query = massage
    eel.senderText(query)
    try:
        if "goodbye" in query or "good bye" in query:
            speak("goodbye sir,have a good day")
            sys.exit()
            # I have to add here jarvis said you want that i closs the computer
        elif "open youtube" in query:
            speak("Sure sir....")
            speak("What do you want to search on youtube?")
            tt = takecommand().lower()
            if tt!="":
                speak("Wait sir i am searching....")
                kit.playonyt(f"{tt}")
                time.sleep(2)
            else:
                speak("I'm sorry, I didn't catch that. Could you please repeat it")
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "close" in query:
            from engine.features import closeCommand
            closeCommand(query)
        elif "youtube" in query:
            from engine.features import playYoutube
            playYoutube(query)
        elif "search" in query:
            from engine.features import search
            search(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):
                if "send message" in query:
                    message = 'message'
                    
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)
            # speak("Sorry, I didn't catch that. Could you please repeat your command?")
        eel.ShowHood()


    except Exception as e:
        print(f"Some error occurred: {e}")

        eel.ShowHood()



@eel.expose
def allCommands():
    try:
       empty_count = 0
       while True:
            query = takecommand()
            eel.senderText(query)

            if query == "":
                empty_count += 1
                if empty_count >= 3:
                    speak("No input detected three times. Exiting...")
                    break
            elif "you can sleep" in query:
               speak("i am going to sleep you can call me anytime.")
               break
            elif "goodbye" in query or "good bye" in query:
                speak("goodbye sir,have a good day")
                eel.hideFrontend() #To Hide The Frontend Terminal This Line Of Code Needed
                sys.exit(0)
            elif "open youtube" in query:
                speak("Sure sir....")
                speak("What do you want to search on youtube?")
                tt = takecommand().lower()
                eel.senderText(tt)
                if tt!="":
                    speak("Wait sir i am searching....")
                    kit.playonyt(f"{tt}")
                    time.sleep(2)
                else:
                    speak("No input detected")
            elif "open" in query:
                from engine.features import openCommand
                openCommand(query)
                empty_count = 0     #To Reset the empty_count variable in up-side
            elif "close" in query:
                from engine.features import closeCommand
                closeCommand(query)
                empty_count = 0     #To Reset the empty_count variable in up-side
            elif "youtube" in query:
                from engine.features import playYoutube
                playYoutube(query)
                empty_count = 0     #To Reset the empty_count variable in up-side
            elif "search" in query:
                from engine.features import search
                search(query)
                empty_count = 0     #To Reset the empty_count variable in up-side
            elif "send message" in query or "phone call" in query or "video call" in query:
                from engine.features import findContact, whatsApp
                message = ""
                contact_no, name = findContact(query)
                if(contact_no != 0):
    
                    if "send message" in query:
                        message = 'message'
                        
                        speak("what message to send")
                        query = takecommand()
                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                        
                    whatsApp(contact_no, query, message, name)
            else:
                
                from engine.features import chatBot
                chatBot(query)
                # speak("Sorry, I didn't catch that. Could you please repeat your command?")
                empty_count = 0     #To Reset the empty_count variable in up-side
    except Exception as e:
        print(f"Some error occurred: {e}")



    eel.ShowHood()
