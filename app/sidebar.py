import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("## Welcome")
        st.write(st.session_state.email)

        # Add a large vertical space before logout
        st.markdown("<div style='height: 55vh;'></div>", unsafe_allow_html=True)
        st.write(st.session_state.decoded)
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()
