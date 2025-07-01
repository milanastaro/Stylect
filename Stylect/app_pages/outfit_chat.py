import streamlit as st
from utils.db import get_user_wardrobe
from utils.outfit_ai import suggest_outfit, suggest_products_to_buy
from PIL import Image
import random

def show():
    st.title("👗 Stylect AI Stylist")
    st.write("Chat with your personal fashion assistant! Ask for styling advice, suggestions, or help with an outfit.")

    username = st.session_state.user_info.get("username")
    wardrobe = get_user_wardrobe(username)

    # Chat history state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    prompt = st.chat_input("Ask me something fashion-related...")

    # Sidebar: upload or import image
    st.sidebar.header("📸 Add an Item")
    uploaded = st.sidebar.file_uploader("Upload new item image", type=["jpg", "jpeg", "png"])

    closet_picker = st.sidebar.selectbox(
        "Or choose from your wardrobe",
        options=["None"] + [item["name"] for item in wardrobe]
    )

    base_items = []

    # Process uploaded image (not yet AI-tagged, placeholder use)
    if uploaded:
        st.sidebar.image(uploaded, width=150, caption="Uploaded item")
        st.session_state.chat_history.append(("user", "Here’s a new item I’m thinking of styling."))
        st.session_state.chat_history.append(("image", uploaded))

    # Add closet item to base_items
    if closet_picker != "None":
        item = next((i for i in wardrobe if i["name"] == closet_picker), None)
        if item:
            base_items.append(item)
            st.sidebar.image(item["image"], width=150, caption=item["name"])
            st.session_state.chat_history.append(("user", f"Can you style this: {item['name']}?"))

    # Process prompt
    if prompt:
        st.session_state.chat_history.append(("user", prompt))

        if "suggest" in prompt.lower() and any(word in prompt.lower() for word in ["buy", "shop", "skirt", "shoes", "tops"]):
            results = suggest_products_to_buy(prompt)
            st.session_state.chat_history.append(("assistant", "Here are some items I recommend:"))
            for item in results:
                st.session_state.chat_history.append(("product", item))
        else:
            # Use mood detection (simple keyword matching)
            mood = None
            for option in ["edgy", "clean girl", "minimal", "vintage", "bold", "trendy", "comfy", "colorful"]:
                if option in prompt.lower():
                    mood = option
                    break

            # Run outfit generator
            outfit = suggest_outfit(
                wardrobe=wardrobe,
                mood=mood,
                preferred_colors=None,
                base_items=base_items
            )

            if not outfit:
                st.session_state.chat_history.append(("assistant", "Hmm, I couldn't find a good match. Try uploading more items or changing your request."))
            else:
                st.session_state.chat_history.append(("assistant", "Here's a styled outfit I put together for you:"))
                for item in outfit:
                    st.session_state.chat_history.append(("wardrobe_item", item))

    # Display chat
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            with st.chat_message("user"):
                st.write(message)
        elif sender == "assistant":
            with st.chat_message("assistant"):
                st.write(message)
        elif sender == "image":
            with st.chat_message("user"):
                st.image(Image.open(message), caption="User-uploaded item", width=200)
        elif sender == "product":
            with st.chat_message("assistant"):
                st.image(message["image"], width=180)
                st.markdown(f"[{message['name']}]({message['link']}) — *{message['price']}*")
        elif sender == "wardrobe_item":
            with st.chat_message("assistant"):
                st.image(message["image"], width=180)
                st.markdown(f"**{message['name']}** — *{message['category']}*")
                st.markdown(f"Tags: `{', '.join(message['tags'])}`")
