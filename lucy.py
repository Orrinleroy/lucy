import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import wikipedia

# --- Initialize Text-to-Speech Engine ---
engine = pyttsx3.init()

def speak(text):
    """This function takes text as input and speaks it."""
    print(f"Lucy: {text}") # <-- CHANGED
    engine.say(text)
    engine.runAndWait()

# --- Initialize Speech Recognition ---
def listen_for_command():
    """Listens for a command from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None

# --- Main Execution Loop ---
if __name__ == '__main__':
    speak("Lucy initialized. How can I help you today?") # <-- CHANGED

    while True:
        # Listen for the wake word "lucy"
        initial_command = listen_for_command()
        
        if initial_command and "lucy" in initial_command: # <-- CHANGED
            speak("Yes? I'm listening.") # <-- CHANGED

            # Listen for the actual command after the wake word
            command = listen_for_command()

            if command:
                # --- Define Your Commands Here ---
                
                if "hello" in command:
                    speak("Hello! It's a pleasure to help.") # <-- CHANGED

                elif "what time is it" in command or "tell me the time" in command:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"The current time is {now}.")

                elif "open google" in command:
                    speak("Opening Google.") # <-- CHANGED
                    webbrowser.open("https://www.google.com")

                elif "search for" in command:
                    search_query = command.replace("search for", "").strip()
                    if search_query:
                        speak(f"Searching for {search_query} on Google.")
                        webbrowser.open(f"https://www.google.com/search?q={search_query}")
                    else:
                        speak("What would you like me to search for?")

                elif "tell me about" in command or "who is" in command:
                # Remove the trigger phrase to get the search topic
                    topic = command.replace("tell me about", "").replace("who is", "").strip()
                
                    if topic:
                        speak(f"Looking up {topic} on Wikipedia.")
                        try:
                            # Get a 2-sentence summary from Wikipedia
                            summary = wikipedia.summary(topic, sentences=2)
                            speak(summary)
                        except wikipedia.exceptions.DisambiguationError as e:
                            speak(f"That could mean several things. Please be more specific. For example, which of these: {e.options[:3]}")
                        except wikipedia.exceptions.PageError:
                            speak(f"Sorry, I could not find a Wikipedia page for {topic}.")
                    else:
                        speak("What topic would you like to know about?")

                elif "weather" in command:
                    api_key = "e9702ac7183b43ff711ca1411eea06e6" 
                    base_url = "http://api.openweathermap.org/data/2.5/weather?"

                    speak("What city are you interested in?")
                    city_name = listen_for_command()

                    if city_name:
                        complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
                        response = requests.get(complete_url)
                        weather_data = response.json()

                        if weather_data["cod"] != "404":
                            main_data = weather_data["main"]
                            current_temperature = main_data["temp"]
                            current_humidity = main_data["humidity"]
                            weather_description = weather_data["weather"][0]["description"]

                            speak(f"The temperature in {city_name} is {current_temperature} degrees Celsius, "
                                f"with {weather_description} and a humidity of {current_humidity} percent.")
                        
                        else:
                            speak("Sorry, I couldn't find that city.")

                    else:
                        speak("I didn't catch the city name.")
                
                elif "goodbye" in command or "exit" in command or "shut down" in command:
                    speak("Goodbye! Shutting down.") # <-- CHANGED
                    break

                else:
                    speak("I'm not sure how to do that yet. Please teach me.")