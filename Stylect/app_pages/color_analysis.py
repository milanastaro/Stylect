import streamlit as st
from PIL import Image
import os
import uuid

from utils_.color_analysis import (
    analyze_face_image,
    get_color_palette,
    save_user_palette,
    load_user_palette
)

def show():
    username = st.session_state.user_info.get("username")
    st.title("🎨 Color Analysis")
    st.markdown("""
        Upload a clear photo of your face in natural lighting (no makeup or filters).  
        We'll analyze your undertone and show you your best color palette.
    """)

    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        temp_dir = "data/temp_faces"
        os.makedirs(temp_dir, exist_ok=True)
        img_id = f"{uuid.uuid4()}.jpg"
        img_path = os.path.join(temp_dir, img_id)
        with open(img_path, "wb") as f:
            f.write(uploaded_file.read())

        st.image(Image.open(img_path), width=300, caption="Your Uploaded Image")

        undertone = analyze_face_image(img_path)
        palette_info = get_color_palette(undertone)

        st.markdown(f"### 🌈 Detected Undertone: **{undertone.title()}**")
        st.markdown(f"**Recommended Palette: {palette_info['name']}**")

        cols = st.columns(len(palette_info["swatches"]))
        for i, color in enumerate(palette_info["swatches"]):
            with cols[i]:
                st.markdown(
                    f"<div style='background-color:{color}; width:100%; height:60px; border-radius:8px'></div>",
                    unsafe_allow_html=True
                )
                st.caption(color)

        if st.button("✅ Save My Color Profile"):
            save_user_palette(username, undertone, palette_info["swatches"])
            st.success("Your palette has been saved and will be used in outfit suggestions.")

    st.markdown("---")
    st.subheader("🗂️ My Saved Palette")
    data = load_user_palette(username)
    if data:
        st.markdown(f"**Undertone:** {data['undertone'].title()} | Saved: {data['analyzed_at']}")
        cols = st.columns(len(data["palette"]))
        for i, color in enumerate(data["palette"]):
            with cols[i]:
                st.markdown(
                    f"<div style='background-color:{color}; width:100%; height:60px; border-radius:8px'></div>",
                    unsafe_allow_html=True
                )
                st.caption(color)
    else:
        st.info("You haven’t saved a color analysis yet.")
