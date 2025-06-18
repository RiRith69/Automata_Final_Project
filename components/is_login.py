import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

def is_logged_in():
    """Check if user is logged in. If not, block access and return False."""
    if not st.session_state.get("logged_in", False):
        st.warning("🔒 Please log in to access this page.")
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            if st.button("🔐 Login", use_container_width=True) :
                st.switch_page("pages/Login.py")
        st.stop()