import speech_recognition as sr
import webbrowser
import pyttsx3
import pywhatkit
import requests

# Groq API
GROQ_API_KEY = "YOUR API KEY"  # Replace with your actual Groq API key
GROQ_URL = "YOUR GORQ URL" # Repalce with your actual Groq URL

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

newsapi = "Your News API" # Repalce with your news API
def speak(text):
    engine.say(text)
    engine.runAndWait()

# AI Response

def ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful virtual assistant named Ultron."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn't process that right now."
    except Exception as e:
        return f"Error connecting to AI: {e}"
    


def processcommand(c):
    
    # browsing

    if "open" in c:
        try:
            # Extract site name from the command
            site = c.split("open")[-1].strip().replace(" ", "")
            url = f"https://{site}.com"
            webbrowser.open(url)
            speak(f"Opening {site}")
        except Exception as e:
            speak("Sorry, I couldn't open the website.")

    # music 

    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            speak("I couldn't play the song. Please try again.")
    
    # news

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=newsapi")
        # Parse JSON response
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            if articles:
                for article in articles:
                    speak(article["title"])
            else:
                speak("No news articles were found.")
        else:
            speak("Sorry, I couldn't fetch the news at this time."  )
    
    # exit
    
    elif "exit" in c.lower() or "stop" in c.lower():
        speak("good bye Sir")
        exit()
    
    # AI Takeover

    else:
        speak("Let me think...")
        reply = ai_response(c)
        speak(reply)
            
            

# main
if __name__ == "__main__":
    speak("Ultron Intialized.....")
    while True:
        print("Recognizing.....")
        # listen for the wake word ultron
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source ,timeout = 2 ,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "ultron"):
                speak("yes Boss..")
            
            # Listen for the command
                with sr.Microphone() as source:
                    print("Ultron Activated ....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processcommand(command)
                    print(command)




        except Exception as e:
            print("Error; {0}".format(e))