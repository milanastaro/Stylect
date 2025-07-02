import streamlit as st
import json
import os

def load_user_data(username):
    user_path = f"data/users/{username}.json"
    if not os.path.exists(user_path):
        return {}
    with open(user_path, "r") as f:
        return json.load(f)

def load_user_posts(username):
    if not os.path.exists("data/style_feed.json"):
        return []
    with open("data/style_feed.json", "r") as f:
        all_posts = json.load(f)
    return [p for p in all_posts if p["username"] == username]

def load_trade_reviews(username):
    if not os.path.exists("data/trade_reviews.json"):
        return []
    with open("data/trade_reviews.json", "r") as f:
        all_reviews = json.load(f)
    return [r for r in all_reviews if r["to_user"] == username]

def show():
    username = st.session_state.user_info["username"]
    user_data = load_user_data(username)
    user_posts = load_user_posts(username)
    user_reviews = load_trade_reviews(username)

    st.title(f"👤 {username}'s Profile")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(user_data.get("profile_picture", "https://via.placeholder.com/150"), width=150)
        st.markdown("**Badges:**")
        for badge in user_data.get("badges", []):
            st.success(f"🏅 {badge}")

    with col2:
        st.subheader("📋 Bio")
        st.markdown(user_data.get("bio", "_No bio set._"))

        st.subheader("⭐ Ratings & Reviews")
        if user_reviews:
            for r in user_reviews:
                st.markdown(f"- **{r['from_user']}**: _{r['review']}_ ({r['rating']}/5)")
        else:
            st.info("You have no reviews yet.")

    st.markdown("---")
    st.subheader("📸 Your Outfit Posts")

    if user_posts:
        for post in user_posts:
            st.image(post.get("image_url"), width=300)
            st.caption(post.get("caption", ""))
    else:
        st.info("You haven’t posted any outfits yet.")
