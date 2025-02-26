import streamlit as st
from streamlit_option_menu import option_menu
import pyttsx3
import speech_recognition as sr
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Set speaking rate
engine.setProperty("volume", 1.0)  # Set volume

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process voice commands
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

# Streamlit App Configuration
st.set_page_config(
    page_title="Accessible Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "This is an accessible assistant application for the visually impaired."
    }
)

# App logo and customization
uploaded_logo = st.sidebar.file_uploader("Upload your logo (PNG or JPEG)", type=["png", "jpg", "jpeg"])
if uploaded_logo:
    st.sidebar.image(uploaded_logo, caption="Your Logo", use_column_width=True)

# Discord-like Sidebar Styling
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Navigation", "Voice Assistant", "Virtual Eye"],
        icons=["map", "mic", "eye"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "#2C2F33"},
            "icon": {"color": "#7289DA", "font-size": "25px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "color": "#FFFFFF",
                "padding": "10px 15px",
                "border-radius": "5px",
            },
            "nav-link-selected": {"background-color": "#7289DA"},
        },
    )

# Main Content Area Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #23272A;
        color: #FFFFFF;
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #7289DA;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #5865F2;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Content Area
if selected == "Navigation":
    st.title("Navigation System")
    st.write("Use voice commands or buttons to navigate.")

    if st.button("Navigate to Malviya Nagar"):
        speak("Navigating to Malviya Nagar. Take the main road towards Tonk Road.")
    if st.button("Navigate to Vaishali Nagar"):
        speak("Navigating to Vaishali Nagar. Merge onto Ajmer Road and continue.")

elif selected == "Voice Assistant":
    st.title("Voice Assistant")
    st.write("Ask me anything or give me commands.")

    if st.button("Start Listening"):
        command = listen_command()
        if command:
            if "navigate" in command and "malviya nagar" in command:
                speak("Navigating to Malviya Nagar. Please follow the directions.")
            elif "navigate" in command and "vaishali nagar" in command:
                speak("Navigating to Vaishali Nagar. Please follow the directions.")
            else:
                speak("I am sorry, I do not recognize this command.")

elif selected == "Virtual Eye":
    st.title("Virtual Eye System")
    st.write("Helping you see the world around you.")

    if st.button("Describe Environment"):
        speak("Analyzing the environment. This area appears to be a residential location.")

# Footer Section
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #2C2F33;
        color: #FFFFFF;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">Accessible Assistant © 2025</div>
    """,
    unsafe_allow_html=True
)
