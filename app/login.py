import streamlit as st
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

# Set Streamlit page config
st.set_page_config(page_title="Login Example")

# Parse token from URL
def show():
    token = st.query_params.get("token")

    # Style
    st.markdown("<h1>🔐 Google OAuth2 Login</h1>", unsafe_allow_html=True)

    if token:
        try:
            # Decode the JWT token
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            email = decoded.get("sub")
            st.session_state.email = email
            st.success(f"✅ Logged in as: {email}")
            if st.button("Logout"):
                st.session_state.clear()
                st.query_params.clear()
                st.rerun()
        except jwt.ExpiredSignatureError:
            st.error("❌ Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            st.error("❌ Invalid token. Authentication failed.")
    else:
        st.info("Please log in to continue.")
        st.markdown(
            """
            <a href="http://localhost:8000/auth/google">
                <button style='
                    background-color: #4285F4;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                '>
                    Login with Google
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
