import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import requests
from io import BytesIO

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

# Helper functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            speak(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that. Please try again.")
            return None
        except sr.RequestError:
            speak("There was an error with the speech recognition service.")
            return None

# Tkinter app setup
root = tk.Tk()
root.title("Accessible Assistant")
root.geometry("1200x800")
root.configure(bg="#f7f7f7")

# Left Frame (Voice Assistant)
left_frame = tk.Frame(root, bg="#f7f7f7", width=300, height=800)
left_frame.pack(side=tk.LEFT, fill=tk.Y)
left_label = tk.Label(left_frame, text="Voice Assistant", font=("Arial", 16), bg="#f7f7f7")
left_label.pack(pady=20)

command_button = tk.Button(left_frame, text="Start Listening", font=("Arial", 12), command=lambda: speak("Listening"))
command_button.pack(pady=10)

# Center Frame (Camera Feed)
center_frame = tk.Frame(root, bg="#000", width=600, height=800)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

camera_label = tk.Label(center_frame)
camera_label.pack(fill=tk.BOTH, expand=True)

# Right Frame (Static Map)
right_frame = tk.Frame(root, bg="#f7f7f7", width=300, height=800)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

right_label = tk.Label(right_frame, text="Navigation Map", font=("Arial", 16), bg="#f7f7f7")
right_label.pack(pady=20)

# Function to fetch and display map using Google Maps Static API
def show_map():
    api_key = "AIzaSyCwStunGtTkMGVDifnJTefx0GN8RdpnFDU"  # Replace with your Google Maps API Key
    center = "26.9124,75.7873"  # Coordinates for Jaipur, India (can be changed to any location)
    zoom = "13"  # Zoom level
    size = "600x400"  # Size of the map image
    map_type = "roadmap"  # Type of map ('roadmap', 'satellite', 'hybrid', 'terrain')

    # Construct the API request URL
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom={zoom}&size={size}&maptype={map_type}&markers={center}&key={api_key}"

    # Send the request to the Google Maps Static API
    response = requests.get(url)
    
    if response.status_code == 200:
        # Convert the response content (image) to an image object
        img_data = BytesIO(response.content)
        img = Image.open(img_data)

        # Resize the image to fit in Tkinter window
        img = img.resize((300, 400))

        # Convert the image to a Tkinter-compatible format
        img_tk = ImageTk.PhotoImage(img)

        # Display the image in the Tkinter window
        map_label = tk.Label(right_frame, image=img_tk)
        map_label.image = img_tk
        map_label.pack(pady=10)
    else:
        print(f"Error fetching map: {response.status_code}")

show_map_button = tk.Button(right_frame, text="Show Map", font=("Arial", 12), command=show_map)
show_map_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
