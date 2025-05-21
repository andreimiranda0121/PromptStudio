import streamlit as st

def sidebar():
    with st.sidebar:
        # Your top/sidebar content (e.g., navigation, user info, etc.)
        st.markdown("## Welcome")
        st.write(st.session_state.email)
        # Add your actual nav buttons here if needed

        # Add a large vertical space before logout
        st.markdown("<div style='height: 55vh;'></div>", unsafe_allow_html=True)
        
        # Logout button at the bottom
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()
