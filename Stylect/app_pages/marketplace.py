import streamlit as st
from utils_.shop_engine import search_products, get_user_shop_items, save_user_shop_items, recommend_bundles, generate_ai_listing
from utils_.trade_engine import get_pending_trades, respond_to_trade, get_trade_history, get_trade_reputation, generate_dual_shipping_labels
import uuid, os
from PIL import Image

def show():
    username = st.session_state.user_info.get("username")
    st.title("🛍️ Marketplace")
    tab1, tab2, tab3, tab4, = st.tabs(["🛒 Shop", "📤 Sell", "🔁 Trade", "👗 Styling Services"])

    # ---------------------- 🛒 SHOP ---------------------- #
    with tab1:
        st.header("🛒 Browse Listings")
        query = st.text_input("Search for an item (e.g., black skirt)")
        size = st.selectbox("Size", ["Any", "XS", "S", "M", "L", "XL"])
        color = st.text_input("Color filter")
        brand = st.text_input("Brand filter")
        filters = {}
        if size != "Any": filters["size"] = size
        if color: filters["color"] = color
        if brand: filters["brand"] = brand

        if query:
            results = search_products(query, filters)
            for item in results:
                st.image(item["image"], width=160)
                st.markdown(f"**{item['title']}** — {item['price']}")
                st.caption(f"Size: {item.get('size')} | Brand: {item.get('brand')}")
                st.button("🛒 Add to Cart", key=f"cart_{uuid.uuid4()}")

        st.markdown("### 🎁 Recommended Bundles")
        bundles = recommend_bundles(username)
        for bundle in bundles:
            st.markdown(f"**{bundle['name']}** — {bundle['price']}")
            for item in bundle["items"]:
                st.image(item["image"], width=100, caption=item["title"])

    # ---------------------- 📤 SELL ---------------------- #
    with tab2:
        st.header("📤 List an Item")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, width=300)
            ai_data = generate_ai_listing(uploaded_file)

            title = st.text_input("Item Title", ai_data["title"])
            tags = st.text_input("Tags", ", ".join(ai_data["tags"]))
            price = st.text_input("Price", ai_data["price"])
            brand = st.text_input("Brand")
            size = st.selectbox("Size", ["XS", "S", "M", "L", "XL"])
            color = st.text_input("Color")
            if st.button("✅ Publish Listing"):
                image_id = f"{uuid.uuid4()}.jpg"
                path = f"data/shop_images/{image_id}"
                os.makedirs("data/shop_images", exist_ok=True)
                with open(path, "wb") as f:
                    f.write(uploaded_file.read())

                item = {
                    "title": title,
                    "tags": [t.strip() for t in tags.split(",")],
                    "price": price,
                    "brand": brand,
                    "size": size,
                    "color": color,
                    "image": path,
                    "owner": username
                }
                user_items = get_user_shop_items(username)
                user_items.append(item)
                save_user_shop_items(username, user_items)
                st.success("Item listed successfully!")

        st.markdown("---")
        st.subheader("📦 Your Inventory")
        inventory = get_user_shop_items(username)
        for item in inventory:
            st.image(item["image"], width=180)
            st.markdown(f"**{item['title']}** — {item['price']}")
            st.caption(f"Size: {item.get('size')} | Brand: {item.get('brand')}")

    # ---------------------- 🔁 TRADE ---------------------- #
        # ---------------------- 🔁 TRADE ---------------------- #
    with tab3:
        st.header("🔁 Your Trades")

        pending = get_pending_trades(username)
        if not pending:
            st.info("No pending trades.")
        else:
            for tid, trade in pending.items():
                st.markdown(f"**Trade ID:** `{tid}`")
                st.markdown(f"- From: `{trade['from']}` → `{trade['to']}`")
                st.markdown(f"- Swap: **{trade['item_from']['title']}** ⇄ **{trade['item_to']['title']}**")
                st.image(trade["item_from"]["image"], width=120, caption="Their Item")
                st.image(trade["item_to"]["image"], width=120, caption="Your Item")
                if username == trade["to"]:
                    col1, col2 = st.columns(2)
                    if col1.button("✅ Accept", key=f"accept_{tid}"):
                        respond_to_trade(tid, True)
                        st.success("Trade accepted.")
                        st.rerun()
                    if col2.button("❌ Reject", key=f"reject_{tid}"):
                        respond_to_trade(tid, False)
                        st.warning("Trade rejected.")
                        st.rerun()
                else:
                    st.caption("Waiting on other user.")
                st.markdown("---")

        st.subheader("📜 Trade History")
        history = get_trade_history(username)
        for tid, t in history.items():
            st.markdown(f"`{tid}` — {t['status'].capitalize()} | {t['item_from']['title']} ⇄ {t['item_to']['title']}")
            if t["status"] == "accepted":
                labels = generate_dual_shipping_labels(t["item_from"], t["item_to"])
                st.code(labels["from_label"])
                st.code(labels["to_label"])

                # Review section
                other_user = t["from"] if username == t["to"] else t["to"]
                st.markdown(f"**Leave a review for `{other_user}`**")
                rating = st.slider("Rating", 1, 5, 5, key=f"rate_{tid}")
                comment = st.text_area("Comment", key=f"comment_{tid}")
                if st.button("📝 Submit Review", key=f"submit_{tid}"):
                    from utils_.trade_engine import submit_trade_review
                    success = submit_trade_review(
                        user=other_user,
                        from_user=username,
                        trade_id=tid,
                        rating=rating,
                        comment=comment
                    )
                    if success:
                        st.success("Review submitted.")
                    else:
                        st.warning("You've already reviewed this trade.")

        st.markdown(" 👤 View Trade Profile")
        selected_user = st.text_input("Enter a username to view their trade reputation")
        if selected_user:
            from utils_.trade_engine import get_trade_reviews, calculate_trade_rating
            rating = calculate_trade_rating(selected_user)
            reviews = get_trade_reviews(selected_user)

            if not reviews:
                st.info("No reviews found.")
            else:
                st.metric(label="⭐ Average Rating", value=rating)
                for r in reviews:
                    st.markdown(f"**From:** `{r['from']}` — ⭐ {r['rating']}")
                    st.markdown(f"*{r['comment']}*")
                    st.caption(f"{r['date']} | Trade ID: `{r['trade_id']}`")
                    st.markdown("---")

        st.metric("🎖️ Your Reputation", get_trade_reputation(username))


    # ---------------------- 👗 STYLING SERVICES ---------------------- #
    with tab4:
        from utils_.styling_services import (
            add_service, get_services, get_user_bookings,
            get_stylist_services, book_service
        )

        st.header("👗 Styling Services")

        tabs = st.tabs(["🔍 Browse", "🧑‍🎨 Offer Service", "📖 My Bookings", "🛠 My Listings"])
        username = st.session_state.user_info.get("username")

        # 🔍 Browse
        with tabs[0]:
            st.subheader("🔍 Browse Styling Services")
            keyword = st.text_input("Search by keyword or tag")
            results = get_services(keyword)

            if not results:
                st.info("No styling services found.")
            else:
                for sid, service in results.items():
                    st.markdown(f"### {service['title']} — ${service['price']}")
                    st.caption(f"By `{service['stylist']}` | Tags: {', '.join(service['tags'])}")
                    st.markdown(service['description'])
                    if st.button("📩 Book this Service", key=f"book_{sid}"):
                        book_service(sid, username)
                        st.success("Service booked!")

        # 🧑‍🎨 Offer Service
        with tabs[1]:
            st.subheader("🧑‍🎨 Offer a Styling Service")
            title = st.text_input("Service Title")
            description = st.text_area("Describe what you offer")
            price = st.text_input("Price in USD (e.g., 10.00)")
            tags = st.text_input("Tags (comma-separated)")

            if st.button("✅ Publish Service"):
                tag_list = [t.strip() for t in tags.split(",")]
                add_service(username, title, description, price, tag_list)
                st.success("Service published!")

        # 📖 My Bookings
        with tabs[2]:
            st.subheader("📖 Services You Booked")
            bookings = get_user_bookings(username)
            if not bookings:
                st.info("You haven’t booked any styling services yet.")
            else:
                services = get_services()
                for bid, b in bookings.items():
                    s = services.get(b["service_id"])
                    if s:
                        st.markdown(f"**{s['title']}** by `{s['stylist']}`")
                        st.caption(f"Booked on {b['booked_at']}")
                        st.markdown("---")

        # 🛠 My Listings
        with tabs[3]:
            st.subheader("🛠 Your Styling Listings")
            your_services = get_stylist_services(username)
            if not your_services:
                st.info("You haven’t offered any services yet.")
            else:
                for sid, s in your_services.items():
                    st.markdown(f"**{s['title']}** — ${s['price']}")
                    st.caption(f"Tags: {', '.join(s['tags'])}")
                    st.markdown(s['description'])
                    st.markdown("---")
