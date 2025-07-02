import streamlit as st
from utils_.shop_engine import search_products, get_user_shop_items, recommend_bundles
import random

def show():
    st.title("🛍️ Stylect Shop")
    st.write("Browse, buy, or sell fashion with the community.")

    st.markdown("### 🔍 Search Listings")
    query = st.text_input("What are you looking for? (e.g., black skirt, pink boots)")

    col1, col2, col3 = st.columns(3)
    with col1:
        size = st.selectbox("Size", ["Any", "XS", "S", "M", "L", "XL"])
    with col2:
        color = st.text_input("Color filter (optional)")
    with col3:
        brand = st.text_input("Brand filter (optional)")

    filters = {}
    if size != "Any":
        filters["size"] = size
    if color:
        filters["color"] = color
    if brand:
        filters["brand"] = brand

    if query:
        results = search_products(query, filters=filters)
        st.subheader(f"🔎 Results for '{query}'")
        if not results:
            st.warning("No listings found.")
        for item in results:
            st.image(item["image"], width=180)
            st.markdown(f"**{item['title']}** — {item['price']}")
            st.caption(f"Brand: {item.get('brand', 'N/A')}, Size: {item.get('size', 'N/A')}")
            st.button("💖 Favorite", key=f"fav_{item['title']}_{random.random()}")
            st.button("🛒 Add to Cart", key=f"cart_{item['title']}_{random.random()}")

    st.markdown("---")
    st.subheader("🎁 Recommended Bundles")
    bundles = recommend_bundles(st.session_state.user_info.get("username"))
    for bundle in bundles:
        st.markdown(f"**{bundle['name']}** — {bundle['price']}")
        for item in bundle["items"]:
            st.image(item["image"], width=120, caption=item["title"])
        st.button("🛍️ View Bundle", key=f"bundle_{bundle['name']}")

    st.markdown("---")
    st.subheader("🧾 My Shop Inventory")
    items = get_user_shop_items(st.session_state.user_info.get("username"))
    if not items:
        st.info("You have not listed anything for sale yet.")
    else:
        for item in items:
            st.image(item["image"], width=180)
            st.markdown(f"**{item['title']}** — {item['price']}")
            st.caption(f"Size: {item.get('size')}, Brand: {item.get('brand')}")
