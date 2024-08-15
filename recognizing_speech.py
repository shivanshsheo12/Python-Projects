import speech_recognition as sr
import pyttsx3
while True:
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    def speak(text):
        engine.say(text)
        engine.runAndWait()
    
    with sr.Microphone() as source:
        speak("Say something...")
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        if(text.lower() == "exit"):
            speak("Thank you !!")
            print("Thank you")
            break
        print(f"You said {text}")
        speak(f"You said {text}")
    except sr.UnknownValueError:
        print("Google speech recognition could not understood the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google speech recognition service; {e}")
