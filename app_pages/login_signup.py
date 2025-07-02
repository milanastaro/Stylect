import streamlit as st
from utils_.auth_engine import signup_user, login_user

st.title("👗 Welcome to Stylect")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = st.radio("Select an option", ["Login", "Sign Up"], horizontal=True)

if menu == "Sign Up":
    st.subheader("Create a New Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    st.markdown("#### Security Questions (for password recovery)")
    q1 = st.text_input("What is your grandmother's name?")
    q2 = st.text_input("What elementary school did you attend?")
    q3 = st.text_input("What city were you born in?")

    if st.button("Sign Up"):
        if username and password and email and phone and q1 and q2 and q3:
            success, msg = signup_user(
                username, password, email, phone,
                {"q1": q1.strip().lower(), "q2": q2.strip().lower(), "q3": q3.strip().lower()}
            )
            st.success(msg) if success else st.error(msg)
        else:
            st.error("Please fill out all fields.")

elif menu == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if username and password:
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.experimental_rerun()
            else:
                st.error(msg)
        else:
            st.error("Please enter username and password.")
