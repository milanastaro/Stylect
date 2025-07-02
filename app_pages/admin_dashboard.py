import streamlit as st
import os
import json

# Replace this with your real CEO username
CEO_USERNAME = "your_username_here"

# File paths
FLAGGED_POSTS = "data/flagged_posts.json"
FLAGGED_MESSAGES = "data/flagged_messages.json"
FLAGGED_LISTINGS = "data/flagged_listings.json"
STYLING_QUEUE = "data/pending_styling.json"
GROUP_APPROVALS = "data/group_approvals.json"
BANNED_USERS = "data/banned_users.json"
ALL_USERS = "data/users.json"

# JSON helpers
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Main admin panel
def admin_controls():
    user = st.session_state.user_info["username"]

    # Only CEO and admins can access
    if user != CEO_USERNAME and not st.session_state.user_info.get("is_admin", False):
        st.error("🚫 Access denied.")
        return

    st.title("🛠️ Stylect Admin Panel")

    # Dashboard
    st.header("📊 System Overview")
    st.markdown(f"""
- 👥 **Users Registered**: {len(load_json(ALL_USERS))}
- 🚫 **Banned Users**: {len(load_json(BANNED_USERS))}
- ⚠️ **Flagged Posts**: {len(load_json(FLAGGED_POSTS))}
- 📬 **Flagged Messages**: {len(load_json(FLAGGED_MESSAGES))}
- 🛍️ **Flagged Listings**: {len(load_json(FLAGGED_LISTINGS))}
    """)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚠️ Flagged Content",
        "✅ Approvals Queue",
        "🚫 User Management",
        "👀 User Lookup",
        "📝 System Tools"
    ])

    # 1. Flagged Content
    with tab1:
        st.subheader("🚩 Flagged Posts")
        posts = load_json(FLAGGED_POSTS)
        for post in posts:
            with st.expander(f"Post by {post['user']}"):
                st.markdown(post['content'])
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=post["id"] + "_approve_post"):
                    posts.remove(post)
                    save_json(FLAGGED_POSTS, posts)
                    st.success("Post approved.")
                    st.experimental_rerun()
                if col2.button("🗑️ Remove", key=post["id"] + "_remove_post"):
                    posts.remove(post)
                    save_json(FLAGGED_POSTS, posts)
                    st.warning("Post removed.")
                    st.experimental_rerun()

        st.divider()
        st.subheader("📬 Flagged Messages")
        messages = load_json(FLAGGED_MESSAGES)
        for msg in messages:
            with st.expander(f"From {msg['sender']} to {msg['receiver']}"):
                st.markdown(msg['text'])
                col1, col2 = st.columns(2)
                if col1.button("✅ Keep", key=msg["id"] + "_keep_msg"):
                    messages.remove(msg)
                    save_json(FLAGGED_MESSAGES, messages)
                    st.success("Message kept.")
                    st.experimental_rerun()
                if col2.button("🗑️ Delete", key=msg["id"] + "_del_msg"):
                    messages.remove(msg)
                    save_json(FLAGGED_MESSAGES, messages)
                    st.warning("Message deleted.")
                    st.experimental_rerun()

        st.divider()
        st.subheader("🛍️ Flagged Listings")
        listings = load_json(FLAGGED_LISTINGS)
        for item in listings:
            with st.expander(f"{item['title']} by {item['seller']}"):
                st.markdown(item['description'])
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=item["id"] + "_approve_listing"):
                    listings.remove(item)
                    save_json(FLAGGED_LISTINGS, listings)
                    st.success("Listing approved.")
                    st.experimental_rerun()
                if col2.button("🗑️ Remove", key=item["id"] + "_remove_listing"):
                    listings.remove(item)
                    save_json(FLAGGED_LISTINGS, listings)
                    st.warning("Listing removed.")
                    st.experimental_rerun()

    # 2. Approvals Queue
    with tab2:
        st.subheader("👗 Styling Services")
        styling = load_json(STYLING_QUEUE)
        for entry in styling:
            with st.expander(f"{entry['stylist']} - {entry['title']}"):
                st.markdown(entry['description'])
                if st.button("✅ Approve Styling", key=entry["id"] + "_approve_style"):
                    styling.remove(entry)
                    save_json(STYLING_QUEUE, styling)
                    st.success("Approved.")
                    st.experimental_rerun()

        st.divider()
        st.subheader("👥 Group Requests")
        groups = load_json(GROUP_APPROVALS)
        for group in groups:
            with st.expander(f"{group['name']} by {group['owner']}"):
                st.markdown(group['description'])
                if st.button("✅ Approve Group", key=group["id"] + "_approve_group"):
                    groups.remove(group)
                    save_json(GROUP_APPROVALS, groups)
                    st.success("Group approved.")
                    st.experimental_rerun()

    # 3. Ban / Unban Users
    with tab3:
        st.subheader("🚫 Ban / Unban Users")
        users = load_json(ALL_USERS)
        banned = load_json(BANNED_USERS)

        to_ban = st.selectbox("Select user to ban", [u["username"] for u in users if u["username"] not in banned])
        if st.button("🚫 Ban User"):
            banned.append(to_ban)
            save_json(BANNED_USERS, banned)
            st.warning(f"{to_ban} banned.")

        to_unban = st.selectbox("Select user to unban", banned)
        if st.button("✅ Unban User"):
            banned.remove(to_unban)
            save_json(BANNED_USERS, banned)
            st.success(f"{to_unban} unbanned.")

    # 4. User Lookup
    with tab4:
        st.subheader("🔍 Lookup User")
        query = st.text_input("Enter username")
        if query:
            match = next((u for u in users if u["username"] == query), None)
            if match:
                st.json(match)
            else:
                st.error("User not found.")

    # 5. System Tools (CEO Only)
    with tab5:
        if user != CEO_USERNAME:
            st.warning("Only the CEO can access these tools.")
        else:
            st.subheader("🧠 AI Code Assistant")
            st.markdown("Let the AI assistant help you modify code files.")

            code_target = st.text_input("Enter file path (e.g., app/outfit_ai.py)")
            code_instruction = st.text_area("Describe what you want to change")
            if st.button("🛠️ Suggest Code"):
                try:
                    with open(code_target, "r") as f:
                        existing_code = f.read()
                    # Simulated response
                    suggestion = f"# Requested change: {code_instruction}\n\n{existing_code}"
                    st.code(suggestion, language="python")
                    if st.button("✅ Confirm Change"):
                        with open(code_target, "w") as f:
                            f.write(suggestion)
                        st.success("File updated.")
                except Exception as e:
                    st.error(f"Failed: {e}")

            st.divider()
            st.subheader("🛡️ Admin Permissions")

            admins = [u for u in users if u.get("is_admin")]
            st.markdown("### 👮 Current Admins")
            for a in admins:
                st.markdown(f"- {a['username']}")

            new_admin = st.selectbox("➕ Grant Admin", [u["username"] for u in users if not u.get("is_admin")])
            if st.button("Grant Admin"):
                for u in users:
                    if u["username"] == new_admin:
                        u["is_admin"] = True
                save_json(ALL_USERS, users)
                st.success(f"{new_admin} is now an admin.")
                st.experimental_rerun()

            remove_admin = st.selectbox("❌ Revoke Admin", [a["username"] for a in admins])
            if st.button("Revoke Admin"):
                for u in users:
                    if u["username"] == remove_admin:
                        u["is_admin"] = False
                save_json(ALL_USERS, users)
                st.warning(f"{remove_admin}'s admin access revoked.")
                st.experimental_rerun()
