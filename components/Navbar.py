# navbar.py
import streamlit as st
import bcrypt
from components.FA_database import 


user_handler = UserHandling()

def login_form():
    st.subheader("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    user_record = user_handler.get_user(username)
    if st.button("Login"):
        if user_record :
            password_hashed = user_record[0][2]
            if bcrypt.checkpw(password.encode('utf-8'), password_hashed.encode('utf-8')) :
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else :
                st.error("❌ Incorrect password")
        else:
            st.error("❌ Invalid username ")

def register_form():
    st.subheader("📝 Register")

    new_user = st.text_input("Choose a username", key="register_user")
    new_pass = st.text_input("Choose a password", type="password", key="register_pass")

    if st.button("Register"):
        if new_user in user_handler.load_users() :
            st.warning("⚠️ Username already taken.")
        elif len(new_pass) < 8:
            st.error("❌ Password must be at least 8 characters.")
        else:
            has_upper = any(c.isupper() for c in new_pass)
            has_lower = any(c.islower() for c in new_pass)
            has_digit = any(c.isdigit() for c in new_pass)
            has_special = any(c in "!@#$%^&*()*+-" for c in new_pass)

            if has_upper and has_lower and has_digit and has_special:
                user_handler.add_user(new_user, new_pass)
                st.success("✅ Registered successfully. Please log in.")
            else:
                st.error("❌ Password must include uppercase, lowercase, digit, and special character.")