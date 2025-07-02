import streamlit as st
import os
import json

USER_DIR = "data/users/"

def load_user_data(username):
    path = os.path.join(USER_DIR, f"{username}.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_user_data(username, data):
    path = os.path.join(USER_DIR, f"{username}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def show():
    username = st.session_state.user_info["username"]
    st.title("⚙️ Account Settings")

    user_data = load_user_data(username)

    # Profile picture
    st.subheader("🖼️ Profile Picture")
    current_pic = user_data.get("profile_picture", "https://via.placeholder.com/150")
    st.image(current_pic, width=150)
    new_pic = st.text_input("Paste a new profile picture URL", value=current_pic)

    # Bio
    st.subheader("📋 Bio")
    new_bio = st.text_area("Edit your bio", value=user_data.get("bio", ""), height=120)

    # Optionally allow changing username (not recommended for now)
    # new_username = st.text_input("Change username", value=username, disabled=True)

    if st.button("💾 Save Changes"):
        user_data["profile_picture"] = new_pic
        user_data["bio"] = new_bio
        save_user_data(username, user_data)
        st.success("✅ Profile updated successfully!")
