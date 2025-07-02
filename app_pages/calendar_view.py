import streamlit as st
from datetime import date
import json
import os

CALENDAR_PATH = "data/calendar.json"
WARDROBE_PATH = "data/wardrobes"

# Load/save calendar data
def load_calendar(username):
    if not os.path.exists(CALENDAR_PATH):
        return {}
    with open(CALENDAR_PATH, "r") as f:
        all_data = json.load(f)
    return all_data.get(username, {})

def save_calendar(username, user_calendar):
    if os.path.exists(CALENDAR_PATH):
        with open(CALENDAR_PATH, "r") as f:
            all_data = json.load(f)
    else:
        all_data = {}

    all_data[username] = user_calendar
    with open(CALENDAR_PATH, "w") as f:
        json.dump(all_data, f, indent=2)

# Page logic
def calendar_page():
    username = st.session_state.user_info["username"]
    st.title("📅 Outfit Calendar & Scheduler")

    user_calendar = load_calendar(username)

    selected_date = st.date_input("Select a date", date.today())
    selected_str = selected_date.isoformat()

    outfit_today = user_calendar.get(selected_str)

    st.subheader("👗 Outfit for " + selected_date.strftime("%B %d, %Y"))

    if outfit_today:
        st.markdown(f"**Outfit:** {outfit_today.get('name', 'N/A')}")
        st.markdown(f"**Tags:** {', '.join(outfit_today.get('tags', []))}")
        st.markdown(f"**Notes:** {outfit_today.get('notes', '')}")

        if outfit_today.get("image_path"):
            st.image(outfit_today["image_path"], use_column_width=True)

        if outfit_today.get("style_feed_link"):
            st.markdown(f"[🧵 View style feed post]({outfit_today['style_feed_link']})")

        if outfit_today.get("items"):
            st.markdown("**Items used:**")
            for item in outfit_today["items"]:
                st.markdown(f"- {item}")
    else:
        st.info("No outfit scheduled for this date.")

    st.divider()
    st.subheader("📅 Schedule a New Outfit")

    outfit_name = st.text_input("Outfit title")
    tags = st.multiselect("Tags", ["casual", "event", "work", "vacation", "rainy", "formal", "lazy day", "school"])
    notes = st.text_area("Notes")
    style_feed_link = st.text_input("Style Feed Post Link (optional)")

    uploaded_image = st.file_uploader("Upload outfit image (optional)", type=["png", "jpg", "jpeg"])
    image_path = None
    if uploaded_image:
        img_folder = f"data/user_images/{username}/calendar"
        os.makedirs(img_folder, exist_ok=True)
        image_path = os.path.join(img_folder, f"{selected_str}_{uploaded_image.name}")
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

    # Load wardrobe items
    wardrobe_items = []
    wardrobe_file = os.path.join(WARDROBE_PATH, f"{username}.json")
    if os.path.exists(wardrobe_file):
        with open(wardrobe_file, "r") as f:
            wardrobe_items = json.load(f)

    selected_items = st.multiselect("Select wardrobe items", [item["name"] for item in wardrobe_items])

    if st.button("✅ Save Outfit"):
        user_calendar[selected_str] = {
            "name": outfit_name,
            "tags": tags,
            "notes": notes,
            "style_feed_link": style_feed_link,
            "image_path": image_path,
            "items": selected_items
        }
        save_calendar(username, user_calendar)
        st.success("Outfit saved to calendar!")

    st.divider()
    st.subheader("🗓️ Upcoming Outfit Schedule")
    upcoming = sorted(user_calendar.items())[-10:]  # show last 10 entries
    for day, entry in upcoming:
        st.markdown(f"- **{day}**: {entry.get('name', 'Unnamed')} ({', '.join(entry.get('tags', []))})")
