import streamlit as st
import jwt
import os
import time
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.jwt_handler import decode_jwt
# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

# Set Streamlit page config
st.set_page_config(page_title="Login Example")

# Parse token from URL
def show():
    token = st.query_params.get("token")

    # Style
    st.markdown("<h1>🔐 PromptStudio Login</h1>", unsafe_allow_html=True)

    if token:
        try:
            # Decode the JWT token
            decoded = decode_jwt(token)
            email = decoded.get("sub")
            name = decoded.get("name")
            st.session_state.decoded = decoded
            if "email" not in st.session_state:
                st.session_state.email = email
                st.session_state.name = name
                st.session_state.token = token
                st.success(f"✅ Logged in as: {email}")
                st.rerun()  # <-- This triggers rerun to load the dashboard

            else:
                st.success(f"✅ Logged in as: {email}")
                if st.button("Logout"):
                    st.session_state.clear()
                    st.query_params.clear()
                    st.rerun()

        except jwt.ExpiredSignatureError:
            st.error("❌ Token expired. Please log in again.")
            if st.button("Try again"):
                st.session_state.clear()
                st.query_params.clear()
                st.rerun()
        except jwt.InvalidTokenError:
            st.error("❌ Invalid token. Authentication failed.")
            if st.button("Try again"):
                st.session_state.clear()
                st.query_params.clear()
                st.rerun()

    else:
        st.info("Please log in to continue.")
        st.markdown(
            """
            <a href="http://localhost:8000/auth/google" target="_self">
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
