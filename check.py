import speech_recognition as sr  # Speech to text
import webbrowser  # Access to browser
import pyttsx3  # Text to speech
import musicLibrary  # Own module
import requests  # Making HTTP requests to interact with web services and APIs
import openai  # Access to OpenAI
import http.client
import json

# Instances
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API Keys
newsapi = "2179dd9011db48dfb541ef13e37ec68c"
openai.api_key = "sk-proj-ZYljsuBgEDpbUaDlc7VGT3BlbkFJH4QJcndEMWTihS54oWJc"
weather_api_key = "0ba94035ecmsh89ad87e33c44248p12812cjsn52cb305ea4f8"

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

# Fetch weather information
def get_weather(city_name):
    conn = http.client.HTTPSConnection("weatherbit-v1-mashape.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': weather_api_key,
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
    }

    # Format the request URL with the city name
    url = f"/current?city={city_name}&units=imperial&lang=en"
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    weather_data = json.loads(data.decode("utf-8"))

    # Extract weather details
    if 'data' in weather_data and len(weather_data['data']) > 0:
        weather_info = weather_data['data'][0]
        temp = weather_info['temp']
        description = weather_info['weather']['description']
        return f"The current temperature in {city_name} is {temp}°F with {description}."
    else:
        return f"Sorry, I couldn't get the weather information for {city_name}."

# Process commands
def processCommand(c):
    c = c.lower()

    # Access to sites like google, facebook, linkedin, youtube
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    # Play particular songs present in musicLibrary file
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)

        if link:
            webbrowser.open(link)
        else:
            speak("Sorry!! unable to find the song")

    # Fetch news headlines and speaks
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        news_data = r.json()
        titles = [article['title'] for article in news_data['articles']]
        for title in titles:
            speak(title)

    # Fetches weather information
    elif "weather" in c:
        try:
            # Extract city name from command (e.g., "weather in London")
            parts = c.split("weather in ")
            if len(parts) > 1:
                city_name = parts[1].strip()
                weather_report = get_weather(city_name)
                speak(weather_report)
            else:
                speak("Please specify the city for the weather update.")
        except Exception as e:
            speak(f"An error occurred: {e}")

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
                audio = r.listen(source)

            command = r.recognize_google(audio)
            if command.lower() == "jarvis":
                speak("yes")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    speak("Jarvis Activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
