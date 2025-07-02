import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image

POSTS_FILE = "data/style_feed.json"
UPLOAD_DIR = "data/feed_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def render_post(post, idx, user, posts):
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(post["image"], use_column_width=True)
    with col2:
        st.markdown(f"**@{post['username']}**")
        st.caption(post["timestamp"])
        st.write(post["caption"])
        if post["tags"]:
            st.markdown(f"`{post['tags']}`")

        # Emoji Reactions
        emojis = ["❤️", "🔥", "👏", "😍", "👍"]
        st.markdown("React:")
        reaction_row = st.columns(len(emojis))
        for i, emoji in enumerate(emojis):
            with reaction_row[i]:
                if st.button(emoji, key=f"react_{idx}_{emoji}"):
                    post["reactions"][emoji] = post["reactions"].get(emoji, 0) + 1
                    save_posts(posts)
                    st.experimental_rerun()
        if post["reactions"]:
            st.caption("Reactions: " + "  ".join(f"{k} {v}" for k, v in post["reactions"].items()))

        # Poll
        if post.get("poll"):
            st.markdown("🗳️ **Vote on this outfit**")
            if user["username"] in post["votes"]:
                st.success(f"You voted: {post['votes'][user['username']]}")
            else:
                vote = st.radio("Your vote:", ["Love it", "Needs work", "Not my style"], key=f"vote_{idx}")
                if st.button("Submit Vote", key=f"submit_vote_{idx}"):
                    post["votes"][user["username"]] = vote
                    save_posts(posts)
                    st.success("✅ Vote submitted!")
                    st.experimental_rerun()

        # Comments
        st.markdown("💬 **Comments:**")
        for comment in post["comments"]:
            st.markdown(f"- **{comment['user']}**: {comment['text']}")
        comment_input = st.text_input(f"Add a comment", key=f"comment_{idx}")
        if st.button("Submit Comment", key=f"submit_comment_{idx}"):
            if comment_input.strip():
                post["comments"].append({"user": user["username"], "text": comment_input.strip()})
                save_posts(posts)
                st.experimental_rerun()

def style_feed():
    st.title("🧢 Style Feed")
    user = st.session_state.get("user_info")

    if not user:
        st.warning("You must be logged in to view or post to the style feed.")
        return

    posts = load_posts()
    tabs = st.tabs(["📸 New Post", "👥 Following Feed", "🌍 Global Feed"])

    # ------------------ 📸 POST TAB ------------------
    with tabs[0]:
        st.subheader("📸 Share a New Look")
        uploaded_image = st.file_uploader("Upload an outfit photo", type=["jpg", "jpeg", "png"])
        caption = st.text_input("Caption your outfit")
        tags = st.text_input("Add tags (e.g. #vintage #clean #streetwear)")
        is_poll = st.checkbox("Allow voting on this post")

        if st.button("Post"):
            if uploaded_image is None or caption.strip() == "":
                st.error("Please add both an image and a caption.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_name = f"{user['username']}_{int(datetime.now().timestamp())}.jpg"
                file_path = os.path.join(UPLOAD_DIR, file_name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_image.read())

                new_post = {
                    "username": user["username"],
                    "caption": caption,
                    "tags": tags,
                    "timestamp": timestamp,
                    "image": file_path,
                    "reactions": {},
                    "comments": [],
                    "poll": is_poll,
                    "votes": {}
                }
                posts.insert(0, new_post)
                save_posts(posts)
                st.success("✅ Post added to the feed!")
                st.experimental_rerun()

    # ------------------ 👥 FOLLOWING FEED ------------------
    with tabs[1]:
        st.subheader("👥 Following Feed")
        following = user.get("profile", {}).get("following", [])
        following_posts = [p for p in posts if p["username"] in following]

        if not following_posts:
            st.info("You aren't following anyone who has posted yet.")
        else:
            for idx, post in enumerate(following_posts):
                render_post(post, idx, user, posts)

    # ------------------ 🌍 GLOBAL FEED ------------------
    with tabs[2]:
        st.subheader("🌍 Global Feed")
        for idx, post in enumerate(posts):
            render_post(post, idx, user, posts)
