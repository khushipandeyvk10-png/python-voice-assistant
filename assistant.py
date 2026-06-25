import datetime
import os
import speech_recognition as sr
import pyttsx3
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech feedback."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Captures voice input from the microphone and converts it to text."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening...")
        # Adjust for ambient noise to improve accuracy
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing voice...")
            # Using Google's free web API for speech recognition
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        
        except sr.WaitTimeoutError:
            # Handle case where user didn't speak within the timeout window
            return ""
        except sr.UnknownValueError:
            # Graceful error handling: voice was not understood
            speak("I'm sorry, I didn't quite catch that. Could you please repeat it?")
            return ""
        except sr.RequestError:
            speak("Networking error. Please check your internet connection.")
            return ""

def process_voice_assistant():
    """Main logic handler for beginner tier features."""
    speak("Voice assistant activated. How can I help you today?")
    
    while True:
        command = listen_command()
        
        if not command:
            continue
        
        # 1. Respond to "Hello"
        if "hello" in command or "hi " in command:
            speak("Hello! I am your python assistant. I'm ready for your commands.")
            
        # 2. Tell the current time and date
        elif "time" in command or "date" in command:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            current_date = now.strftime("%B %d, %Y")
            speak(f"Today is {current_date}, and the current time is {current_time}.")
            
        # 3. Perform a web search on a user-specified topic
        elif "search for" in command or "google" in command:
            # Extract the search query from the sentence
            search_query = command.replace("search for", "").replace("google", "").strip()
            if search_query:
                speak(f"Searching the web for {search_query}.")
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
            else:
                speak("What would you like me to search for?")
                
        # 4. Exit / Stop Command
        elif "stop" in command or "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day.")
            break
            
        else:
            speak("I recognized the words, but I don't have a command mapped for that action yet.")

if __name__ == "__main__":
    process_voice_assistant()