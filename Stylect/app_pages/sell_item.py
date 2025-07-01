import streamlit as st
from utils.shop_engine import generate_ai_listing, get_user_shop_items, save_user_shop_items
from PIL import Image
import uuid
import os

def show():
    st.title("🧾 Sell an Item")
    st.write("Upload a fashion item to list it for sale in the Stylect Shop.")

    username = st.session_state.user_info.get("username")
    uploaded_file = st.file_uploader("📸 Upload a photo of the item", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Preview", width=300)

        # Run AI listing generator (placeholder)
        ai_data = generate_ai_listing(uploaded_file)

        st.markdown("### ✨ Suggested Details (you can edit them)")

        title = st.text_input("Item Title", ai_data["title"])
        tags = st.text_input("Tags (comma-separated)", ", ".join(ai_data["tags"]))
        price = st.text_input("Price (e.g., $24.99)", ai_data["price"])
        brand = st.text_input("Brand (optional)")
        size = st.selectbox("Size", ["XS", "S", "M", "L", "XL"])
        color = st.text_input("Color")

        confirm = st.button("✅ Publish Item")

        if confirm:
            image_id = f"{uuid.uuid4()}.jpg"
            img_path = f"data/shop_images/{image_id}"
            os.makedirs("data/shop_images", exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(uploaded_file.read())

            item = {
                "title": title,
                "tags": [t.strip() for t in tags.split(",")],
                "price": price,
                "brand": brand,
                "size": size,
                "color": color,
                "image": img_path,
                "owner": username
            }

            current = get_user_shop_items(username)
            current.append(item)
            save_user_shop_items(username, current)

            st.success("🎉 Item listed for sale!")
