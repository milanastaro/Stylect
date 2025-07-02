import streamlit as st
import os
import json

WARDROBE_DIR = "data/wardrobes/"

def load_wardrobe(username):
    path = os.path.join(WARDROBE_DIR, f"{username}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def show():
    username = st.session_state.user_info["username"]
    st.title(f"👚 {username}'s Wardrobe")

    wardrobe = load_wardrobe(username)

    if not wardrobe:
        st.info("Your wardrobe is empty. Start adding items!")
        return

    # Filters
    categories = sorted(set(item["category"] for item in wardrobe))
    selected_category = st.selectbox("Filter by category", ["All"] + categories)

    filtered = wardrobe if selected_category == "All" else [
        item for item in wardrobe if item["category"] == selected_category
    ]

    st.markdown(f"### Showing {len(filtered)} item(s)")

    # Display grid
    for item in filtered:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(item["image_url"], width=100)
            with cols[1]:
                st.markdown(f"**Name:** {item['name']}")
                st.markdown(f"**Category:** {item['category']}")
                st.markdown(f"**Tags:** {', '.join(item.get('tags', []))}")
                if item.get("tradeable"):
                    st.success("🪙 Listed for trade")
