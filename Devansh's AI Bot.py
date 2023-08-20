import win32com.client
import os
import speech_recognition as sr
import webbrowser
import openai
import datetime
import requests
import json
def speak (text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)
def login_to_instagram(username, password):
    session = requests.Session()

    # Send GET request to Instagram's login page to get the CSRF token
    response = session.get('https://www.instagram.com/accounts/login/')
    csrf_token = response.cookies.get('csrftoken', '')

    #Prepare the login data (including the CSRF token)
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }

    try:
        # Send POST request to perform the login
        response = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, headers={
            'X-CSRFToken': csrf_token,
            'Referer': 'https://www.instagram.com/accounts/login/',
            'X-Requested-With': 'XMLHttpRequest'
        })

        # Check the response to see if login was successful
        if response.json().get('authenticated'):
            print('Login successful!')
            speak('Login successful!')
            # Continue with your actions after login
            # For example, you can make requests to view your profile, post photos, etc.
        else:
            print('Login failed.')
            speak('Login failed.')
    except json.decoder.JSONDecodeError:
        print('An error occurred while logging in.')
        speak('An error occurred while logging in.')
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said:{query}")
            return query
        except Exception as e:
            return "Some Error Occurred , Sorry From Jarvis"
if __name__ == '__main__':
    print('Pycharm')
    speak("Hello I Am Devansh's A.I Bot, How can i help you Sir!")
    while True:
        print("Listening....")
        query = takeCommand() #Just Say Open Youtube , Open Wikipedia ,etc to open any website
        sites = [["youtube", "https://www.youtube.com"] , ["wikipedia"," https://wikipedia.com"],["google","https://www.google.com"],["chatGPT","https://www.openai.com"],["instagram", "https://www.instagram.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath= "Enter the path of your music file here." #Music file path
            os.startfile(musicPath)
        if "the time" in query:
            strfTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is{strfTime}")
        if "webcam".lower() in query.lower():
            os.startfile("Enter the path of your webcam .exe file here") #Your webcam .exe file path
        if "login my instagram" in query.lower():
            speak("Sure, I am logging in to your Instagram account. Please wait...")
            username =input("Enter Your Username")
            password =input("Enter Your Password")
            login_to_instagram(username, password)
        if "stop".lower() in query.lower(): # To Stop Simply Say Stop
            break



