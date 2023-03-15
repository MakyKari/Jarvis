import speech_recognition as sr
from playsound import playsound
from datetime import datetime
from subprocess import Popen
from os import system
from psutil import process_iter
import webbrowser
import requests

paths = {
        "voicefolder": "C:\\MyOwnFiles\\Programming\\Projects\\voices\\",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "visualstudio" : "C:\\MyOwnFiles\\Programming\\Visual Studio\\Common7\\IDE\\devenv.exe"
}

def VoiceRecorder():
    InputVoice = sr.Recognizer()
    with sr.Microphone() as source:
        UserPhrase = InputVoice.listen(source, phrase_time_limit=3)
        
    told=InputVoice.recognize_google(UserPhrase, language="ru-RU")
    return told

def sayTime():
    now = datetime.now()
    playsound(paths["voicefolder"]+now.strftime("%H")+"hours.mp3")
    playsound(paths["voicefolder"]+now.strftime("%M")+"minutes.mp3")
    playsound(paths["voicefolder"]+now.strftime("%S")+"seconds.mp3")

def openapp(nameofpath,soundopen):
    Popen([paths[nameofpath]])
    playsound(paths["voicefolder"]+soundopen)

def closeapp(appname,appclosename,soundclose):
    if(appname in (i.name() for i in process_iter())):
        system("taskkill /f /im " + appclosename)
        playsound(paths["voicefolder"]+soundclose)
    else:
        playsound(paths["voicefolder"]+"cannotclose.mp3")

def main():
    try:
        rawphrase = VoiceRecorder()
        phrase = rawphrase.lower()
        print(phrase)

        for greatings in ["приветствую","здравствуйте","здравствуй","привет"]:                            #greatings to user
            if(greatings in phrase.lower()):                                                              #Greatings to user
                playsound(paths["voicefolder"]+'Greatings.mp3')
        
        for bye in ["пока","прощай","до свидания","отключись"]:                                           #bye to user
            if(bye in phrase.lower()):
                playsound(paths["voicefolder"]+"goodbye.mp3")
        
        if "время" in phrase or "час" in phrase:                                                          #Outputs current time
            sayTime()
        
        if ("калькулятор" in phrase) and ("открыть" in phrase or "открой" in phrase):                     #opens calculator
            openapp("calculator","calculator.mp3")
        
        if ("калькулятор" in phrase) and ("закрыть" in phrase or "закрой" in phrase):                     #closes calculator
            closeapp("Calculator.exe","Calculator.exe","closecalc.mp3")
        
        if ("google" in phrase or "браузер" in phrase) and ("открыть" in phrase or "открой" in phrase):   #opens Edge
            webbrowser.open("https://www.google.com/")
        
        if ("google" in phrase or "браузер" in phrase) and ("закрой" in phrase or "закрыть" in phrase):   #closes Edge
            closeapp("msedge.exe","msedge.exe","closeedge.mp3")
        
        if "загугли" in phrase:                                                                           #googles sth
            search = (phrase.replace("пожалуйста","")).split("загугли")
            webbrowser.open("https://www.google.com/search?q="+ search[1])
            playsound(paths["voicefolder"]+"googled.mp3")
        
        if "погода" in phrase or "погоду" in phrase:                                                      #tells weather
            
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': 1526273, 'units': 'metric', 'lang': 'ru', 'APPID': "afffb769afeb11fa6d1f724d78e036a7"})
            data = res.json()
            
            if data['main']['temp'] > 0:
                playsound(paths["voicefolder"]+str(round(data['main']['temp']))+".mp3")
                playsound(paths["voicefolder"]+"celcium degree.mp3")
            elif data['main']['temp'] < 0:
                playsound(paths["voicefolder"]+"minus.mp3")
                playsound(paths["voicefolder"]+str(round(data['main']['temp']))+".mp3")
                playsound(paths["voicefolder"]+"celcium degree.mp3")
            else:
                playsound(paths["voicefolder"]+"0.mp3")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


playsound(paths["voicefolder"]+"waiting.mp3")
while(True):
    main()