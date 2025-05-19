import streamlit as st


def settings():
    with st.expander("Model and Prompt Settings", expanded=True):
        st.selectbox(label="Select Model",options=['gpt-4o','gemini-2.0-flash'],key="model")
        st.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1, key="temperature")
        st.slider(label="Top-p", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="top_p")
        st.caption(body="test")

def main():
    settings()
    if "model_settings" not in st.session_state:
        st.session_state.model_settings = {
            "model" : st.session_state.model,
            "temperature" : st.session_state.temperature,
            "top_p" : st.session_state.top_p
        }
    st.write(st.session_state.model_settings)


main()