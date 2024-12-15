import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import urllib.parse

# Inisialisasi engine text-to-speech
engine = pyttsx3.init()

# Berbicara
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Mendengarkan suara dari mikrofon
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Mengurangi noise sekitar
        audio = recognizer.listen(source)
    return audio

# Mengenali perintah suara
def recognize_command(audio):
    recognizer = sr.Recognizer()
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble connecting to the speech service.")
        return None

# Memproses perintah
def process_command(command):
    if command is None:
        speak("I didn't catch that. Can you repeat?")
        return

    if 'hello' in command:
        speak("Hello! How can I assist you today?")
    
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    
    elif 'open' in command:
        if 'website' in command:
            speak("Which website do you want to open?")
            command = listen()
            website = recognize_command(command)
            if website:
                webbrowser.open(f"http://{website}.com")
                speak(f"Opening {website}.com")
    
    elif 'play music' in command:
        speak("What song do you want to play?")
        command = listen()
        song = recognize_command(command)
        if song:
            # Mencari lagu di YouTube 
            song = urllib.parse.quote_plus(song)  # Encode nama lagu agar bisa digunakan di URL
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            speak(f"Playing {song} on YouTube")
    
    elif 'thanks for helping' in command:  # Menambahkan perintah untuk menutup aplikasi
        speak("okay, Goodbye!")
        sys.exit()  # Menghentikan program
    
    else:
        speak("Sorry, I did not understand that command.")

# Utama
def main():
    speak("Hello, I am your voice assistant. Please give me a command.")
    while True:
        audio = listen()
        command = recognize_command(audio)
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
