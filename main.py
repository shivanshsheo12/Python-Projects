import speech_recognition as sr # Speech to text
import webbrowser # Access to browser
import pyttsx3 # Text to speech
import musicLibrary # Own module
import requests # Making HTTP requests to interact with web services and APIs.
import openai # Access to OpenAi

# Instances
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API Keys
newsapi = "2179dd9011db48dfb541ef13e37ec68c"
openai.api_key = "sk-proj-ZYljsuBgEDpbUaDlc7VGT3BlbkFJH4QJcndEMWTihS54oWJc"

# Speak function -> input text -> output voice 
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Conversational responses
def get_conversational_response(prompt):
    r = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return r.choices[0].text.strip()

# Process Three commands
# -> open websites like google,facebook,linkedin,youtube
# -> plays music
# -> speaks the latest news
# -> else: transfers the speech to text-davinci-003 model and gives the process

def processCommand(c):
    c = c.lower()

    # Access to sites like google,facebook,linkedin,youtube
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    # plays particular songs present in musicLibrary file
    elif c.lower().startswith("play"):

        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]

        if link:
            webbrowser.open(link)
        else:
            speak("Sorry!! unable to find the song")

    # Fetches news headlines and speaks
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        news_data = r.json()
        titles = [article['title'] for article in news_data['articles']]
        for title in titles:
            speak(title)

    # Access to ChatGPT
    else:
        response = get_conversational_response(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone

        r = sr.Recognizer()
        print("recognizing...")

        try:

            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,phrase_time_limit=1)

            command = r.recognize_google(audio)
            if(command.lower() == "jarvis"):
                speak("yes")

                # Listen for command
                with sr.Microphone() as source:
                    
                    print("Jarvis Active...")
                    speak("Jarvis Activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error: {0}".format(e))