import time
from datetime import datetime
import pyttsx3
import weather

def assistant():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    def speak(message):
        """
        Speaks the given message using text-to-speech.
        :param message: String message to be spoken.
        """
        engine.say(message)
        engine.runAndWait()

    # List of reminders with task description and time in minutes
    reminders = []

    def time_to_minutes(period, time_input):
        """
        Converts a spoken time with a period (am/pm or a/p) to minutes from midnight.
        :param period: String indicating "a" (am) or "p" (pm).
        :param time_input: String indicating the time in "H:MM" format.
        :return: Integer time in minutes from midnight.
        """
        try:
            # Split time into hours and minutes
            time_obj = datetime.strptime(time_input, "%I:%M")
            hour = time_obj.hour
            minutes = time_obj.minute

            # Adjust for AM/PM
            if period.lower() == "p" and hour != 12:
                hour += 12
            elif period.lower() == "a" and hour == 12:
                hour = 0

            # Calculate total minutes from midnight
            total_minutes = hour * 60 + minutes
            return total_minutes
        except ValueError:
            raise ValueError("Invalid time format. Please say the time clearly, like 2:30.")

    def add_reminder():
        """
        Allows the user to add a new reminder using voice input.
        """
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening for the time of the reminder (e.g., 2:30 a/p)...")
                    speak("Please say the time for the reminder, like 2:30 followed by a for AM or p for PM.")
                    audio = recognizer.listen(source)
                    time_with_period = recognizer.recognize_google(audio).lower()

                    print(f"You said: {time_with_period}")

                    # Extract time and period
                    if " " in time_with_period:
                        time_input, period = time_with_period.split()
                        period = period[0]  # Get only 'a' or 'p'
                    else:
                        raise ValueError("Please specify am or pm with the time.")

                    # Convert time to minutes from midnight
                    time_in_minutes = time_to_minutes(period, time_input)

                    print("Listening for the task description...")
                    speak("Now say the task description.")
                    audio = recognizer.listen(source)
                    task_input = recognizer.recognize_google(audio).upper()

                    print(f"You said: {task_input}")

                    # Add the reminder
                    reminders.append({"time": time_in_minutes, "task": task_input})
                    print(f"Reminder added: {task_input} at {time_in_minutes} minutes from midnight")
                    speak(f"Reminder added for {task_input} at {time_input} {period.upper()}")

                    more = input("Do you want to add another reminder? (yes/no): ").strip().lower()
                    if more != "yes":
                        break
            except sr.UnknownValueError:
                print("Sorry, I did not understand. Please try again.")
                speak("Sorry, I did not understand. Please try again.")
            except ValueError as e:
                print(e)
                speak(str(e))

    def check_reminders():
        """
        Continuously checks the current time and triggers reminders.
        """
        print("Daily Task Reminder system is running...")
        notified_tasks = set()  # To avoid multiple notifications for the same task

        while True:
            # Get the current time in minutes from midnight
            now = datetime.now()
            current_minutes = now.hour * 60 + now.minute

            for reminder in reminders:
                if current_minutes == reminder["time"] and reminder["time"] not in notified_tasks:
                    # Notify the user
                    message = "Reminder: {reminder['task']}"
                    print(message)
                    speak(message)

                    # Add the task to the notified set
                    notified_tasks.add(reminder["time"])

            time.sleep(30)  # Check every 30 seconds

    # Interactive menu for setting reminders
    print("Welcome to your Personal Assistant Reminder System!")
    add_reminder()

    # Run the reminder system
    check_reminders()

    speak("I will also tell you the weather outside")
    weather.main()

    
