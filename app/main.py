import streamlit as st
import login
import dashboard

# Do NOT call the functions here
PAGES = {
    "Login": login.show,
    "Dashboard": dashboard.show,
}

# Control logic based on session state
if "email" in st.session_state:
    page = "Dashboard"
else:
    page = "Login"

# Call the appropriate page's function
PAGES[page]()
