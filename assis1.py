import streamlit as st
import pyttsx3
import speech_recognition as sr
from threading import Thread
from datetime import datetime
import time

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize speech recognition
recognizer = sr.Recognizer()

# Speak function
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    """Listen for a voice command and return the recognized text."""
    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            st.success(f"You said: {command}")
            return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat.")
        return None
    except sr.RequestError:
        speak("Microphone or recognition service is not working. Please check.")
        return None

# Locations and Routes
locations = {
    "malviya nagar": "A residential and commercial area in Jaipur.",
    "vaishali nagar": "A posh locality in Jaipur known for its vibrant markets.",
    "tonk road": "A major road connecting various parts of Jaipur.",
    "ajmer road": "A highway leading to Ajmer from Jaipur.",
    "delhi": "The capital city of India.",
    "jaipur": "The Pink City and the capital of Rajasthan.",
    "niwai": "A small town near Jaipur.",
    "banasthali vidyapith": "A renowned women's university near Tonk."
}

routes = {
    ("delhi", "jaipur"): [
        "Start from Delhi.",
        "Take NH48 and continue on the Jaipur-Delhi Highway.",
        "Drive for approximately 260 kilometers.",
        "Follow signs for Jaipur and take the exit towards the city center.",
        "You have arrived in Jaipur."
    ],
    ("niwai", "jaipur"): [
        "Start from Niwai.",
        "Take the NH52 road towards Jaipur.",
        "Continue straight for about 65 kilometers.",
        "Enter Jaipur via Tonk Road.",
        "You have arrived in Jaipur."
    ],
    ("banasthali vidyapith", "delhi"): [
        "Start from Banasthali Vidyapith.",
        "Head towards Tonk and join NH52.",
        "Drive north to Jaipur and merge onto NH48.",
        "Continue on NH48 towards Delhi for approximately 260 kilometers.",
        "You have arrived in Delhi."
    ]
}

# Reminders
reminders = []

def add_reminder(time_input, task):
    """Add a reminder."""
    time_obj = datetime.strptime(time_input, "%H:%M")
    reminder_minutes = time_obj.hour * 60 + time_obj.minute
    reminders.append({"time": reminder_minutes, "task": task})
    speak(f"Reminder added for {task} at {time_input}.")
    return f"Reminder added for {task} at {time_input}."

def check_reminders():
    """Thread function to check reminders."""
    notified_tasks = set()
    while True:
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute
        for reminder in reminders:
            if current_minutes == reminder["time"] and reminder["time"] not in notified_tasks:
                speak(f"Reminder: {reminder['task']}")
                st.write(f"Reminder: {reminder['task']}")
                notified_tasks.add(reminder["time"])
        time.sleep(30)

def navigate(start, destination):
    """Provide navigation instructions."""
    if start not in locations or destination not in locations:
        speak("Sorry, I couldn't find one of the locations you mentioned.")
        return

    route = routes.get((start, destination))
    if not route:
        speak(f"Sorry, I don't have a predefined route from {start} to {destination}.")
        return

    speak(f"Starting navigation from {start.capitalize()} to {destination.capitalize()}.")
    for step in route:
        speak(step)
        st.write(step)
    speak(f"You have arrived at {destination.capitalize()}.")

def main():
    st.title("Voice-Based Navigation and Reminder System")

    # Background thread to check reminders
    reminder_thread = Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

    st.header("Voice Commands")
    st.write("Use voice commands to control the system.")

    # Wait for commands
    while True:
        speak("How can I assist you? Say 'navigate', 'reminder', or 'exit'.")
        command = listen()

        if command is None:
            continue

        if "navigate" in command:
            speak("Please tell me your starting location.")
            start = listen()
            if not start:
                continue
            speak("Please tell me your destination.")
            destination = listen()
            if start and destination:
                navigate(start.lower(), destination.lower())

        elif "reminder" in command:
            speak("Please tell me the time for the reminder in HH:MM format.")
            time_input = listen()
            if not time_input:
                continue
            speak("What task should I remind you about?")
            task = listen()
            if time_input and task:
                try:
                    message = add_reminder(time_input, task)
                    st.success(message)
                except ValueError:
                    speak("Invalid time format. Please try again.")

        elif "exit" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    main()
