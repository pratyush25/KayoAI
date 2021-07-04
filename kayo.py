import pyttsx3
import os
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    # converts a string to audo
    engine.say(audio)
    engine.runAndWait()


def audioToString():
    # converts audio to string
    # input from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.2   # listening time
        audio = r.listen(source)

    try:
        print("Recognizing, Please Wait...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query, "\n")
    except Exception as ex:
        # print(ex)
        print("Did not get that :(")
        return "None"
    return query


def greeter():
    hours = int(datetime.datetime.now().hour)
    if hours >= 4 and hours <= 12:
        speak('Good Morning!')
    elif hours > 12 and hours <= 17:
        speak('Good Afternoon!')
    elif hours > 17 and hours <= 20:
        speak('Good Evening!')
    else:
        speak('Good Night!')
    speak('Hey, I am Kayo. How may I help you?')


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your_password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


def main():
    greeter()
    while True:
        query = audioToString().lower()
        if query == 'bye':
            speak("Good Bye!")
            break
        # logic for queries
        elif 'wikipedia' in query and 'open' not in query:
            speak("Searching in Wikipedia...")
            query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open' in query:
            words = query.split()
            wb.open(f"https://{words[words.index('open')+1]}.com")
        elif 'the time' in query:
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Time is {nowtime}")
        elif 'date' in query:
            nowdate = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today is {nowdate}")
        elif 'open code' in query:
            cpath = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(cpath)
        elif 'play music' in query:
            muspath = "C:\\Users\\DELL\\AppData\\Roaming\\Spotify\\Spotify.exe"
            os.startfile(muspath)
        elif 'send email' in query:
            try:
                name = query.split()
                name = name[name.index('to')+1]
                speak("What should I say?")
                content = audioToString()
                sendEmail(name, content)
                speak("Email sent!")
            except Exception as e:
                # print(e)
                speak("Some Error occurred. Please try again later.")


if __name__ == '__main__':
    main()
