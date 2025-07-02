import os
import streamlit as st

def get_user_color_palette(username):
    path = f"data/users/{username}_palette.json"
    if os.path.exists(path):
        import json
        with open(path, "r") as f:
            return json.load(f).get("colors", [])
    return []

def get_username():
    """Safely returns the logged-in username or stops the app if not logged in."""
    user = st.session_state.get("user_info")
    if user and "username" in user:
        return user["username"]
    else:
        st.warning("⚠️ You must be logged in to use this feature.")
        st.stop()