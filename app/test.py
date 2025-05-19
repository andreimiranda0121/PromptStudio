import os
import sys
import streamlit as st
import tiktoken

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.constants import SUPPORTED_MODELS
# from src.services.api_requests import execute_prompt
# from src.services.file_processing import process_uploaded_file

# Example prompt template default
DEFAULT_PROMPT_TEMPLATE = "You are a helpful assistant. Answer the user's question:\n\n{query}"

# Max limits
MAX_PROMPT_TEMPLATE_CHARS = 1000
MAX_PROMPT_TEMPLATE_TOKENS = 250
MAX_USER_INPUT_CHARS = 200
MAX_USER_INPUT_TOKENS = 50  # approx for 200 chars, can adjust

# Initialize tokenizer for GPT-4 style models (replace if your model differs)
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(tokenizer.encode(text))

# Initialize session state for chat and settings if not exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_context" not in st.session_state:
    st.session_state.document_context = ""

if "saved_settings" not in st.session_state:
    st.session_state.saved_settings = {
        "model": SUPPORTED_MODELS[0],
        "temperature": 0.7,
        "max_tokens": 512,
        "prompt_template_text": DEFAULT_PROMPT_TEMPLATE,
    }

# --- Sidebar History ---
st.sidebar.title("📜 Prompt History")
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.sidebar.markdown(f"**You:** {chat['user']}\n\n**Bot:** {chat['bot']}")
else:
    st.sidebar.info("No chat history yet.")

# --- Settings Panel ---
with st.expander("⚙️ Model & Prompt Settings", expanded=False):
    temp_model = st.selectbox("Choose Model", SUPPORTED_MODELS, index=SUPPORTED_MODELS.index(st.session_state.saved_settings["model"]))
    temp_temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.saved_settings["temperature"], 0.1)
    temp_max_tokens = st.slider("Max Tokens", 100, 4096, st.session_state.saved_settings["max_tokens"], 100)

    # Prompt template text area only (no selection)
    prompt_template_text = st.text_area(
        "Edit Prompt Template (use {query} where user input is inserted):",
        value=st.session_state.saved_settings["prompt_template_text"],
        height=150,
    )
    
    # Count tokens and chars in prompt template
    prompt_template_chars = len(prompt_template_text)
    prompt_template_tokens = count_tokens(prompt_template_text)
    st.markdown(f"**Prompt Template Length:** {prompt_template_chars} chars / {prompt_template_tokens} tokens")

    # Validation warnings for prompt template
    if prompt_template_chars > MAX_PROMPT_TEMPLATE_CHARS:
        st.warning(f"Prompt template exceeds max {MAX_PROMPT_TEMPLATE_CHARS} characters!")
    if prompt_template_tokens > MAX_PROMPT_TEMPLATE_TOKENS:
        st.warning(f"Prompt template exceeds max {MAX_PROMPT_TEMPLATE_TOKENS} tokens!")

    # Optional RAG File Upload
    uploaded_file = st.file_uploader("📄 Upload document for RAG (optional)", type=["pdf", "txt", "csv"])
    if uploaded_file:
        with st.spinner("Processing document..."):
            # st.session_state.document_context = process_uploaded_file(uploaded_file)
            st.success("Document processed successfully!")

    # Save button
    if st.button("Save"):
        if prompt_template_chars <= MAX_PROMPT_TEMPLATE_CHARS and prompt_template_tokens <= MAX_PROMPT_TEMPLATE_TOKENS:
            st.session_state.saved_settings = {
                "model": temp_model,
                "temperature": temp_temperature,
                "max_tokens": temp_max_tokens,
                "prompt_template_text": prompt_template_text,
            }
            st.success("Settings saved!")
        else:
            st.error("Cannot save: Prompt template exceeds max limits.")

# --- Main Chat Interface ---
st.title("🧪 PromptPlayground Chat Sandbox")

# Show existing chat messages
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("ai"):
        st.markdown(chat["bot"])

# Chat input with live char/token counter
user_input = st.chat_input("Type your query here... (Max 200 characters / 50 tokens)")

if user_input:
    user_input_chars = len(user_input)
    user_input_tokens = count_tokens(user_input)

    if user_input_chars > MAX_USER_INPUT_CHARS:
        st.warning(f"Input exceeds {MAX_USER_INPUT_CHARS} characters. Please shorten your query.")
    elif user_input_tokens > MAX_USER_INPUT_TOKENS:
        st.warning(f"Input exceeds {MAX_USER_INPUT_TOKENS} tokens. Please shorten your query.")
    else:
        # Combine prompt template and user input using saved settings
        full_prompt = st.session_state.saved_settings["prompt_template_text"].replace("{query}", user_input)

        with st.spinner("Generating response..."):
            response = "test response"
            '''
            response = execute_prompt(
                model=st.session_state.saved_settings["model"],
                prompt=full_prompt,
                temperature=st.session_state.saved_settings["temperature"],
                max_tokens=st.session_state.saved_settings["max_tokens"],
                context=st.session_state.document_context
            )
            '''
            # Save chat
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": response
            })
            st.experimental_rerun()
