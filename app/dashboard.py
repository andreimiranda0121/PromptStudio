import streamlit as st
import requests
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.api_request import *
from sidebar import fetch_prompt_history
from src.services.api_request import chat_request
import uuid

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
        "prompt_id": "",
        "model_settings": {}
    }
    
    # Set any missing state variables to their defaults
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

def save_settings():
    prompt_id = str(uuid.uuid4())
    st.session_state.model_settings = {
        "model": st.session_state.model,
        "temperature": st.session_state.temperature,
        "top_p": st.session_state.top_p,
        "prompt_template": st.session_state.prompt_template,
        "use_context": st.session_state.use_context,
        "prompt_id" :  prompt_id
    }

    st.session_state.show_settings = False
    st.session_state.settings_saved = True
    st.session_state.chat_history = []
    

    try:
        response = requests.post(
            url="http://localhost:8000/prompt/saved_settings/",
            data={
                "email": st.session_state.email,
                "model_settings": json.dumps(st.session_state.model_settings)
            }
        )
        
        if response.status_code == 200:
            # Clear the sidebar cache to force reload of history
            fetch_prompt_history.clear()
            
        else:
            st.error(f"Failed to save settings. Status: {response.status_code}")
            
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")

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
        st.success("✅ Settings saved and history updated!")
        st.session_state.settings_saved = False

    if st.session_state.load_settings:
        st.success("✅ Load Previous Settings Successfully!")
        st.session_state.show_settings = False
        st.session_state.load_settings = False

    if st.session_state.delete_prompt:
        st.success("✅ Delete Prompt Successfully")
        st.session_state.chat_history = []
        st.session_state.delete_prompt = False
    if st.session_state.show_settings:
        settings()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Enter your query", max_chars=100)
    files = None
    if st.session_state.uploaded_file:
        files = {
            "file": (
                st.session_state.uploaded_file.name,
                st.session_state.uploaded_file.getvalue(),
                st.session_state.uploaded_file.type
            )
        }
    if query:
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        if not st.session_state.model_settings:
            st.error("⚠️ Please save your settings before sending a query.")
            return
        response = chat_request(
            st.session_state.email,
            st.session_state.prompt_id,
            st.session_state.model_settings['model'],
            st.session_state.model_settings['temperature'],
            st.session_state.model_settings['top_p'],
            st.session_state.model_settings['prompt_template'],
            st.session_state.model_settings['use_context'],
            query,
            files
        )
        with st.chat_message("ai"):
            st.markdown(response)
            with st.expander(label="Settings"):
                st.write(st.session_state.model_settings['prompt_template'])
        st.session_state.chat_history.append({"role": "ai", "content": response})