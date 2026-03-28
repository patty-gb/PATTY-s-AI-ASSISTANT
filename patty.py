import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os

# Initialize text-to-speech engine with error handling
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Female voice (use [0] for male)
    engine.setProperty('rate', 180)
except Exception as e:
    print(f"Error initializing speech engine: {e}")
    print("Try: pip uninstall pyttsx3 && pip install pyttsx3==2.71")
    exit()

def speak(audio):
    """Convert text to speech"""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def wishMe():
    """Greet user based on time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Boss")
    else:
        speak("Good Evening Boss")
    
    speak("I am Patty. How may I help you?")

def takeCommand():
    """Listen and recognize voice commands"""
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 4000  # Increased for better detection
            r.adjust_for_ambient_noise(source, duration=1)
            
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    
    except sr.WaitTimeoutError:
        print("Listening timeout...")
        return "none"
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "none"
    except sr.RequestError:
        speak("Network error. Check internet connection")
        return "none"
    except Exception as e:
        print(f"Error: {e}")
        return "none"

def open_application(app_name, paths, web_fallback):
    """Generic function to open applications"""
    speak(f"Opening {app_name}")
    
    for path in paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            try:
                os.startfile(expanded_path)
                return
            except Exception as e:
                print(f"Error: {e}")
    
    # Fallback to web version
    speak(f"{app_name} not found. Opening web version")
    webbrowser.open(web_fallback)

# Main program
if __name__ == "__main__":
    print("=== JARVIS AI ASSISTANT ===")
    print("Starting...")
    
    wishMe()
    
    while True:
        try:
            query = takeCommand().lower()
            
            if query == "none":
                continue
            
            # Open Google
            if 'google' in query:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
            
            # Open YouTube
            elif 'youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            
            # Open Chrome
            elif 'chrome' in query:
                chrome_paths = [
                    "C:/Program Files/Google/Chrome/Application/chrome.exe",
                    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
                ]
                open_application("Chrome", chrome_paths, "https://www.google.com")
            
            # Open Spotify
            elif 'spotify' in query or 'music' in query:
                spotify_paths = [
                    "~\\AppData\\Roaming\\Spotify\\Spotify.exe"
                ]
                open_application("Spotify", spotify_paths, "https://open.spotify.com")
            
            # Open VS Code
            elif 'code' in query or 'vs code' in query:
                vscode_paths = [
                    "~\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                    "C:/Program Files/Microsoft VS Code/Code.exe"
                ]
                open_application("VS Code", vscode_paths, "https://vscode.dev")
            
            # Open Perplexity
            elif 'perplexity' in query:
                speak("Opening Perplexity")
                webbrowser.open("https://www.perplexity.ai")
            
            # Wikipedia - simplified
            elif 'wikipedia' in query:
                speak("Searching")
                query = query.replace("wikipedia", "")
                webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
            
            # Tell time
            elif 'time' in query:
                time_str = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {time_str}")
                print(f"Time: {time_str}")
            
            # Tell date
            elif 'date' in query:
                date_str = datetime.datetime.now().strftime("%B %d, %Y")
                speak(f"Today is {date_str}")
                print(f"Date: {date_str}")
            
            # Greetings
            elif 'hello' in query or 'hi' in query:
                speak("Hello! How can I help you?")
            
            # Exit
            elif 'exit' in query or 'quit' in query or 'bye' in query or 'stop' in query:
                speak("Goodbye! Have a great day!")
                break
            
            # Unknown command
            else:
                speak("I didn't understand. Please try again.")
        
        except KeyboardInterrupt:
            speak("Shutting down")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue