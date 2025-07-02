import streamlit as st
import os
import json

USER_DB = "data/users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return []
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)

def login_signup():
    st.title("👤 Login / Sign Up")

    tabs = st.tabs(["🔐 Login", "🆕 Sign Up", "🔁 Forgot Username", "🔑 Forgot Password"])
    users = load_users()

    # =========================== SIGN UP ============================
    with tabs[1]:
        st.header("🆕 Create Account")

        new_user = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        new_pass = st.text_input("Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")

        st.markdown("### 🔒 Security Questions (for recovery)")
        grandma = st.text_input("What is your grandmother’s first name?")
        elementary = st.text_input("What elementary school did you attend?")
        favorite_color = st.text_input("What is your favorite color?")

        if st.button("Create Account"):
            if new_pass != confirm_pass:
                st.error("❌ Passwords do not match.")
                return
            if any(u["username"] == new_user for u in users):
                st.error("❌ Username already exists.")
                return

            user_data = {
                "username": new_user,
                "password": new_pass,
                "email": email,
                "phone": phone,
                "is_admin": False,
                "security_questions": {
                    "grandma": grandma.strip().lower(),
                    "elementary": elementary.strip().lower(),
                    "color": favorite_color.strip().lower()
                },
                "profile": {
                    "bio": "",
                    "profile_pic": "",
                    "badges": [],
                    "rating": 0,
                    "followers": [],
                    "following": [],
                    "groups": []
                }
            }
            users.append(user_data)
            save_users(users)

            st.session_state.user_info = user_data
            st.session_state.is_new_user = True
            st.success("🎉 Account created!")
            st.experimental_rerun()

    # =========================== LOGIN =============================
    with tabs[0]:
        st.header("🔐 Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            match = next((u for u in users if u["username"] == username and u["password"] == password), None)
            if match:
                st.session_state.user_info = match
                st.session_state.is_new_user = False
                st.success(f"✅ Welcome back, {username}!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password.")

    # ======================== FORGOT USERNAME ======================
    with tabs[2]:
        st.header("🔁 Forgot Username")
        email_input = st.text_input("Enter your email")

        if st.button("Find My Username"):
            match = next((u for u in users if u["email"] == email_input), None)
            if match:
                st.success(f"✅ Your username is: **{match['username']}**")
            else:
                st.error("❌ No account found with that email.")

    # ======================== FORGOT PASSWORD ======================
    with tabs[3]:
        st.header("🔑 Forgot Password")
        username_input = st.text_input("Enter your username")
        user = next((u for u in users if u["username"] == username_input), None)

        if user:
            st.markdown("### 🔐 Answer your security questions")
            q1 = st.text_input("What is your grandmother’s first name?")
            q2 = st.text_input("What elementary school did you attend?")
            q3 = st.text_input("What is your favorite color?")

            new_pass = st.text_input("New Password", type="password")
            confirm_new = st.text_input("Confirm New Password", type="password")

            if st.button("Reset Password"):
                answers = user["security_questions"]
                if (
                    q1.strip().lower() == answers["grandma"] and
                    q2.strip().lower() == answers["elementary"] and
                    q3.strip().lower() == answers["color"]
                ):
                    if new_pass == confirm_new:
                        user["password"] = new_pass
                        save_users(users)
                        st.success("✅ Password reset successfully. You may now log in.")
                    else:
                        st.error("❌ Passwords do not match.")
                else:
                    st.error("❌ One or more security answers are incorrect.")
        else:
            st.info("Enter a valid username to begin recovery.")
