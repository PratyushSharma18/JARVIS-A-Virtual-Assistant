import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("NEWS_API_KEY:", os.getenv("NEWS_API_KEY"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()



def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    #Initialize pygame mixer
    pygame.mixer.init()

    #Load the mp3 file
    pygame.mixer.music.load('temp.mp3')

    #Play the mp3 file
    pygame.mixer.music.play()

    #Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
    api_key = OPENAI_API_KEY
    )


    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant anmed jarvis skilled in general tasks like Alexa and Google Cloud. Give short and brief responses please."},
        {
            "role": "user",
            "content": command
        }
    ]
 )

    return completion.choices[0].message.content



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=apple&from=2025-03-06&to=2025-03-06&sortBy=popularity&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            #Parse the JSON response
            data = r.json()
            #Extract the articles
            articles = data.get('articles',[]) 
            #Read the headlines
            for article in articles:
                speak(article['title'])   


    else:
         #Let openAI handle the request
         output = aiProcess(c)
         speak(output)
         pass            

if __name__ == "__main__":
    speak("Initializing Jarvis....")    
    while True:
        #Listen for the wake word "Jarvis"
        #Obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Yes")
                # Listening for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))                 