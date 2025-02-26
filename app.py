import streamlit as st
from streamlit_webrtc import webrtc_streamer
import webbrowser

def main():
    # Set page configuration
    st.set_page_config(page_title="Discord Style App", page_icon="🔧", layout="wide")

    # Apply Discord-like styling
    st.markdown(
        """
        <style>
            body {
                background-color: #36393f;
                color: #dcddde;
                font-family: 'Arial', sans-serif;
            }
            .stButton button {
                background-color: #5865f2;
                color: white;
                border-radius: 5px;
                border: none;
                padding: 10px 15px;
                font-size: 16px;
            }
            .stButton button:hover {
                background-color: #4752c4;
            }
            .stTextInput > div > input {
                background-color: #2f3136;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Camera", "Open Webpage"])

    if app_mode == "Camera":
        st.header("Camera Stream")
        st.write("Use your camera directly from this app.")
        webrtc_streamer(key="camera")

    elif app_mode == "Open Webpage":
        st.header("Open a Webpage")
        url = st.text_input("Enter the URL of the webpage you want to visit:")
        if st.button("Open URL"):
            if url:
                webbrowser.open(url)
                st.success(f"Opening {url}...")
            else:
                st.error("Please enter a valid URL.")

if __name__ == "__main__":
    main()
