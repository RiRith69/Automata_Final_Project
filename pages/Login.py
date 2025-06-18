# app.py
import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.Hero import show_hero

import streamlit as st
from components.Navbar import login_form, register_form

show_hero()
# Initialize session state
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# If logged in, show welcome
if st.session_state.logged_in:
    st.success(f"👋 Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home")
        st.rerun()
else:
    # Navigation UI
    nav = st.radio("Choose an option:", ["Login", "Register"])
    if nav == "Login":
        login_form()
    elif nav == "Register":
        register_form()