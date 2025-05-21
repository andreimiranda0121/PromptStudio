import streamlit as st
import login
import dashboard
from sidebar import sidebar
# Do NOT call the functions here
PAGES = {
    "Login": login.show,
    "Dashboard": dashboard.show,
}

def main():
    if "email" in st.session_state:
        page = "Dashboard"
        sidebar()
    else:
        page = "Login"

    PAGES[page]()

if __name__ == "__main__":
    main()
