import streamlit as st
from utils_.weather import get_current_weather
from utils_.db import get_user_color_palette
from utils_.outfit_ai import suggest_outfit
from utils_.wardrobe_engine import get_user_wardrobe

def show():
    st.title("🧠 Smart Outfit Generator")
    st.write("Stylect will suggest a personalized outfit based on your wardrobe, weather, preferences, and style.")

    username = st.session_state.user_info.get("username")
    wardrobe = get_user_wardrobe(username)

    if not wardrobe:
        st.warning("You need to upload clothing to your wardrobe first.")
        return

    with st.spinner("🌦️ Fetching current weather..."):
        weather = get_current_weather()
        if not weather:
            st.error("Could not get weather data. Try again later.")
            return

    st.success(f"Current weather: **{weather['description']}**, **{weather['temperature']}°C**")

    st.markdown("### 🎯 Your Preferences")
    occasion = st.selectbox("What's the occasion?", ["Casual", "Work", "Date", "Formal", "Party", "Outdoor"])
    mood = st.selectbox("Choose a style mood or aesthetic", [
        "Neutral", "Bold", "Comfy", "Trendy", "Minimal", "Edgy", "Clean girl", "Colorful", "Vintage"
    ])
    
    color_pref = st.multiselect("Any specific colors you want to wear today?", [
        "Black", "White", "Beige", "Pink", "Red", "Blue", "Green", "Purple", "Brown", "Gray", "Yellow", "Orange"
    ])

    use_color_analysis = False
    if st.checkbox("🎨 Use my color analysis results?"):
        user_palette = get_user_color_palette(username)
        if user_palette:
            st.success("We'll prioritize colors from your personal palette.")
            use_color_analysis = True
        else:
            st.warning("No color analysis data found. Try uploading a face photo in your profile first.")
    
    if st.button("👚 Generate My Outfit"):
        with st.spinner("Generating your perfect look..."):
            outfit = suggest_outfit(
                wardrobe=wardrobe,
                weather=weather,
                occasion=occasion,
                mood=mood,
                preferred_colors=color_pref,
                use_color_palette=use_color_analysis,
                username=username
            )

        if not outfit:
            st.warning("No outfit could be generated with the current filters. Try changing your inputs or uploading more wardrobe items.")
        else:
            st.subheader("✨ Your AI-Recommended Outfit")
            for item in outfit:
                st.image(item["image"], width=200)
                st.markdown(f"**{item['name']}** — *{item['category']}*")
                st.markdown(f"Tags: `{', '.join(item['tags'])}`")
