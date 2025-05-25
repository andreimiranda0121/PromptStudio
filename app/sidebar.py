import streamlit as st
import requests

@st.cache_data(show_spinner=False)
def fetch_prompt_history(email):
    """Cached function to fetch prompt history - only runs once per session"""
    try:
        response = requests.get(
            "http://localhost:8000/prompt/prompt_history",
            params={"email": email}
        )
        if response.status_code == 200:
            return response.json().get("history", [])
        else:
            return []
    except Exception as e:
        print(f"Error loading history: {e}")
        return []
def delete_prompt(email, prompt_id):
    try:
        response = requests.delete(
            url= "http://localhost:8000/prompt/delete_prompt/",
            params={
                "email": email,
                "prompt_id": prompt_id
            }
        )
        if response.status_code == 200:
            print("Delete success")
        else:
            print(response.status_code)
    except Exception as e:
        print(f"Error deleting prompt: {e}")

def sidebar():
    if "load_settings" not in st.session_state:
        st.session_state.load_settings = False

    with st.sidebar:
        st.markdown(f"## Welcome, {st.session_state.name}")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()

        st.title('Prompt History')

        # Load history only once per session (cached)
        history = fetch_prompt_history(st.session_state.email)
        
        if history:
            # Show latest 5 (most recent first)
            for i, entry in enumerate(reversed(history[::-1])):
                with st.expander(label=f"Prompt {i + 1} - {entry.get('timestamp', 'Unknown')[:19]}"):
                    st.write("Model Settings:")
                    st.write(f"Model Name: {entry.get('model', 'N/A')}")
                    st.write(f"Temperature: {entry.get('temperature', 'N/A')}")
                    st.write(f"Top-p: {entry.get('top_p', 'N/A')}")
                    st.write(f"Prompt Template: {entry.get('prompt_template', 'N/A')}")
                    st.write(f"Use Contexxt: {entry.get('use_context', 'N/A')}")
                    st.write(f"Timestamp: {entry.get('timestamp', 'N/A')}")
                    col1 , col2 = st.columns(2)
                    with col1:
                        if st.button(label="Load", key=f"load{i + 1}"):
                            st.session_state.load_settings = True
                            st.session_state.model_settings = {
                                "model": entry.get('model', 'N/A'),
                                "temperature": entry.get('temperature', 'N/A'),
                                "top_p": entry.get('top_p', 'N/A'),
                                "prompt_template": entry.get('prompt_template', 'N/A'),
                                "use_context": entry.get('use_context', 'N/A'),
                            }
                            st.session_state.chat_history = []
                            st.rerun()
                    with col2:
                        if st.button(label="Delete", key=f"delete{i+1}"):
                            st.write(entry.get('prompt_id', 'N/A'))
                            delete_prompt(st.session_state.email, entry.get('prompt_id', 'N/A'))
                            fetch_prompt_history.clear()  # Correct way to invalidate cache
                            st.rerun()

        else:
            st.info("No prompt history found.")

        # Add a large vertical space before logout
        #st.markdown("<div style='height: 55vh;'></div>", unsafe_allow_html=True)
        #st.write(st.session_state.get("decoded", {}))