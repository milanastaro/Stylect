import streamlit as st

def home_page():
    username = st.session_state.user_info.get("username", "Stylect User")
    is_new = st.session_state.get("is_new_user", False)

    if is_new:
        st.title(f"👋 Welcome to Stylect, {username}!")
        st.markdown("You're all set up — here's a quick tour of what you can do:")

        with st.expander("👗 Outfit Generator"):
            st.markdown("""
            Let the AI style you using your wardrobe, the weather, your style preferences, and color analysis.
            """)

        with st.expander("🎨 Color Analysis"):
            st.markdown("""
            Upload a photo of your face and we’ll create a personalized color palette for you.
            """)

        with st.expander("🛍️ Shop & Trade"):
            st.markdown("""
            Buy, sell, trade, or bundle items with other users. Earn reviews and grow your seller reputation.
            """)

        with st.expander("📅 Outfit Calendar"):
            st.markdown("""
            Schedule outfits for future events and track what you’ve worn day to day.
            """)

        with st.expander("🎭 Style Feed & Social"):
            st.markdown("""
            Post outfits, create polls, react with emojis, join chats or groups, and connect with friends!
            """)

        with st.expander("🏆 Profile & Badges"):
            st.markdown("""
            Customize your profile, set privacy settings, and earn badges for activity and style!
            """)

        with st.expander("🛠️ Admin Tools (if applicable)"):
            st.markdown("""
            If you're an admin or the CEO, you’ll get access to moderation tools, user reports, and even an AI code editor.
            """)

        st.success("Tour complete! You're ready to use Stylect 🦋")
        if st.button("✨ Start Styling Now"):
            st.session_state.is_new_user = False
            st.experimental_rerun()

    else:
        st.title(f"👋 Welcome back, {username}!")
        st.markdown("Explore your wardrobe, check the calendar, or see what's trending on the style feed.")
