import streamlit as st
from PIL import Image
import os
import uuid

from utils_.social_engine import (
    create_post, get_all_posts, react_to_post, comment_on_post,
    follow_user, unfollow_user, get_follow_data
)

POST_IMG_DIR = "data/post_images"
os.makedirs(POST_IMG_DIR, exist_ok=True)

def show():
    username = st.session_state.user_info.get("username")
    st.title("📸 Stylect Social Feed")

    tabs = st.tabs(["🆕 Create Post", "📰 Feed", "👥 Following"])

    # 🆕 Create a post
    with tabs[0]:
        st.subheader("New Outfit Post")
        img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        caption = st.text_input("Add a caption")
        allow_vote = st.checkbox("Enable community voting on this outfit")

        if st.button("📤 Post"):
            if img_file:
                file_id = f"{uuid.uuid4()}.jpg"
                save_path = os.path.join(POST_IMG_DIR, file_id)
                with open(save_path, "wb") as f:
                    f.write(img_file.read())

                img_url = save_path
                create_post(username, img_url, caption, allow_vote)
                st.success("Posted successfully!")
            else:
                st.warning("Please upload an image.")

    # 📰 Feed
    with tabs[1]:
        st.subheader("Explore Outfits")
        posts = get_all_posts()
        if not posts:
            st.info("No posts yet. Be the first to share!")
        else:
            for post_id, post in reversed(posts.items()):
                st.markdown(f"**{post['user']}** — *{post['created_at']}*")
                st.image(post["image"], use_column_width=True)
                st.caption(post["caption"])

                # Reactions
                emojis = ["❤️", "🔥", "😍", "👍"]
                cols = st.columns(len(emojis))
                for i, emoji in enumerate(emojis):
                    with cols[i]:
                        if st.button(emoji, key=f"{emoji}_{post_id}"):
                            react_to_post(post_id, emoji, username)

                # Display reaction counts
                if post["emoji_reactions"]:
                    reaction_summary = " | ".join(
                        f"{e} {len(u)}" for e, u in post["emoji_reactions"].items()
                    )
                    st.caption(f"Reactions: {reaction_summary}")

                # Comments
                st.markdown("**💬 Comments**")
                for c in post["comments"]:
                    st.markdown(f"- **{c['user']}**: {c['comment']}")

                new_comment = st.text_input("Add a comment", key=f"cmt_{post_id}")
                if st.button("Submit", key=f"btn_cmt_{post_id}"):
                    comment_on_post(post_id, username, new_comment)
                    st.success("Comment added!")

                st.markdown("---")

    # 👥 Following / Followers
    with tabs[2]:
        st.subheader("My Network")
        data = get_follow_data(username)
        st.write(f"**You follow:** {', '.join(data['following']) or 'No one yet.'}")
        st.write(f"**Your followers:** {', '.join(data['followers']) or 'No followers yet.'}")

        st.markdown("### Follow a new user")
        target = st.text_input("Enter username to follow")
        col1, col2 = st.columns(2)
        if col1.button("➕ Follow"):
            follow_user(username, target)
            st.success(f"You are now following {target}")
        if col2.button("🚫 Unfollow"):
            unfollow_user(username, target)
            st.success(f"You unfollowed {target}")
