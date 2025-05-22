import streamlit as st
import requests
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.api_request import *


def initialize_session_state():
    # Define all required session state variables with default values
    defaults = {
        "chat_history": [],
        "show_settings": False,
        "settings_saved": False,
        "model": "gpt-4o",
        "temperature": 0.3,
        "top_p": 0.7,
        "use_context": "No",
        "uploaded_file": None,
        "prompt_template": "You're an intelligent assistant that can answer users questions",
        "model_settings": {}
    }
    
    # Set any missing state variables to their defaults
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


initialize_session_state()

def save_settings():
    st.session_state.model_settings = {
        "model": st.session_state.model,
        "temperature": st.session_state.temperature,
        "top_p": st.session_state.top_p,
        "prompt_template": st.session_state.prompt_template,
        "use_context": st.session_state.use_context,
    }

    st.session_state.show_settings = False
    st.session_state.settings_saved = True

    files = None
    if st.session_state.uploaded_file:
        files = {
            "file": (
                st.session_state.uploaded_file.name,
                st.session_state.uploaded_file.getvalue(),
                st.session_state.uploaded_file.type
            )
        }

    response = requests.post(
        url="http://localhost:8000/prompt/saved_settings/",
        data={"model_settings": json.dumps(st.session_state.model_settings)},
        files=files
    )
    st.write(response)



def settings():
    with st.container():
        st.selectbox("Select Model", options=['gpt-4o', 'gemini-2.0-flash'], key="model")
        st.slider("Temperature", 0.0, 1.0, 0.3, 0.1, key="temperature")
        st.slider("Top-p", 0.0, 1.0, 0.7, 0.1, key="top_p")
        st.text_area(
            "Input your prompt template",
            max_chars=500,
            key="prompt_template",
            value=st.session_state.prompt_template,
            height=200,
            help="Use {input} for user input and {context} for context (if any)."
        )

        # Use context toggle
        st.radio("Use context from uploaded file?", ["No", "Yes"], key="use_context", horizontal=True)

        if st.session_state.use_context == "Yes":
            uploaded_file = st.file_uploader("Upload PDF for context", type=["pdf"])
            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file

            if st.session_state.uploaded_file:
                st.info(f"📄 File '{st.session_state.uploaded_file.name}' saved for this session.")
            else:
                st.info("📄 No file uploaded for this session.")

        st.button("Save Settings", on_click=save_settings)

def toggle_settings():
    st.session_state.show_settings = not st.session_state.show_settings
    if st.session_state.show_settings and st.session_state.model_settings:
        for key, value in st.session_state.model_settings.items():
            st.session_state[key] = value

def show():
    # Re-initialize session state to ensure it exists
    initialize_session_state()
    
    col1, col2 = st.columns([9, 1])
    with col1:
        st.title("PromptStudio")
    with col2:
        # Use on_change for the toggle to update state directly
        st.toggle("⚙️", 
                value=st.session_state.show_settings, 
                key="toggle_settings", 
                on_change=toggle_settings,
                help="Toggle model settings")

    if st.session_state.settings_saved:
        st.success("✅ Settings saved.")
        st.session_state.settings_saved = False

    if st.session_state.show_settings:
        settings()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    query = st.chat_input("Enter your query", max_chars=100)
    if query:
       
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        response = "hello"
        with st.chat_message("ai"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "ai", "content": response})

