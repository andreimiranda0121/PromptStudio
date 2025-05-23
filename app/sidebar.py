import streamlit as st

def sidebar():
    if "load_settings" not in st.session_state:
        st.session_state.load_settings = False
    with st.sidebar:
        st.markdown("## Welcome")
        st.write(st.session_state.email)
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()
        st.title('Prompt History')
        for i in range(5):
            with st.expander(label=f"Prompt {i+1}"):
                st.write("Model Settings:")
                st.write("Model Name: gpt-4o")
                st.write("Temperature: 0.3")
                if st.button(label="Load settings", key=f"load{i+1}"):
                    st.session_state.load_settings = True
                    st.rerun
                
        # Add a large vertical space before logout
        st.markdown("<div style='height: 55vh;'></div>", unsafe_allow_html=True)
        st.write(st.session_state.decoded)
      