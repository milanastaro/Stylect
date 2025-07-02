import streamlit as st
import os
import json
import uuid
from datetime import datetime

# Data paths
CHAT_DIR = "data/chats/"
GROUP_DIR = "data/group_chats/"
GROUP_LIST = "data/groups.json"
WARDROBE_DIR = "data/wardrobes/"

os.makedirs(CHAT_DIR, exist_ok=True)
os.makedirs(GROUP_DIR, exist_ok=True)
os.makedirs(WARDROBE_DIR, exist_ok=True)

def load_wardrobe(username):
    path = os.path.join(WARDROBE_DIR, f"{username}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def load_groups():
    if not os.path.exists(GROUP_LIST):
        return []
    with open(GROUP_LIST, "r") as f:
        return json.load(f)

def save_groups(groups):
    with open(GROUP_LIST, "w") as f:
        json.dump(groups, f, indent=2)

def send_chat(path, sender, message, poll=None, reply_to=None):
    chat = []
    if os.path.exists(path):
        with open(path, "r") as f:
            chat = json.load(f)
    chat.append({
        "id": str(uuid.uuid4()),
        "sender": sender,
        "text": message,
        "timestamp": datetime.utcnow().isoformat(),
        "reactions": [],
        "poll": poll,
        "reply_to": reply_to
    })
    with open(path, "w") as f:
        json.dump(chat, f, indent=2)

def load_chat(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def display_chat(messages, chat_path, username):
    replying_to_id = st.session_state.get("replying_to")
    replying_to_text = None
    if replying_to_id:
        original = next((m for m in messages if m["id"] == replying_to_id), None)
        if original:
            replying_to_text = original["text"][:100]

    for msg in messages[-20:]:
        with st.chat_message("user" if msg["sender"] == username else "assistant"):
            # Show reply preview
            if msg.get("reply_to"):
                replied = next((m for m in messages if m["id"] == msg["reply_to"]), None)
                if replied:
                    st.markdown(f"> 💬 **Reply to:** _{replied['text'][:80]}_")

            st.markdown(msg["text"])

            # Reply button
            if st.button("↩️ Reply", key=msg["id"] + "_reply"):
                st.session_state["replying_to"] = msg["id"]
                st.experimental_rerun()

            # Poll voting
            if msg.get("poll"):
                poll = msg["poll"]
                st.markdown(f"**📊 {poll['question']}**")
                for i, opt in enumerate(poll["options"]):
                    if st.button(opt, key=msg["id"] + f"_vote_{i}"):
                        poll["votes"][username] = i
                        with open(chat_path, "w") as f:
                            json.dump(messages, f, indent=2)
                        st.experimental_rerun()
                st.caption("Votes: " + ", ".join(
                    [f"{opt} ({list(poll['votes'].values()).count(i)})"
                     for i, opt in enumerate(poll["options"])]))

            # Emoji reactions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("❤️", key=msg["id"] + "_h"):
                    msg["reactions"].append({"user": username, "emoji": "❤️"})
            with col2:
                if st.button("🔥", key=msg["id"] + "_f"):
                    msg["reactions"].append({"user": username, "emoji": "🔥"})
            with col3:
                if st.button("😂", key=msg["id"] + "_l"):
                    msg["reactions"].append({"user": username, "emoji": "😂"})
            if msg["reactions"]:
                summary = {}
                for r in msg["reactions"]:
                    e = r["emoji"]
                    summary[e] = summary.get(e, 0) + 1
                st.caption(" ".join([f"{k} x{v}" for k, v in summary.items()]))

    with st.chat_message("user"):
        if replying_to_text:
            st.info(f"Replying to: {replying_to_text}")
            if st.button("Cancel Reply"):
                del st.session_state["replying_to"]
                st.experimental_rerun()

        msg = st.chat_input("Send a message")
        if msg:
            send_chat(chat_path, username, msg, reply_to=replying_to_id)
            if "replying_to" in st.session_state:
                del st.session_state["replying_to"]
            st.experimental_rerun()

    # Closet item sharing
    with st.expander("🧺 Share from your closet"):
        wardrobe = load_wardrobe(username)
        if not wardrobe:
            st.info("Your wardrobe is empty.")
        else:
            item_names = [item["name"] for item in wardrobe]
            selected = st.selectbox("Choose item to share", item_names, key=f"share_{chat_path}")
            if st.button("📤 Share Item", key=f"send_{chat_path}"):
                item = next(i for i in wardrobe if i["name"] == selected)
                item_message = f"""
**{item['name']}**

Tags: {', '.join(item.get('tags', []))}

{"✅ Tradeable" if item.get("tradeable") else "❌ Not Tradeable"}

![Item]({item['image_url']})
"""
                send_chat(chat_path, username, item_message)
                st.success("Item shared!")
                st.experimental_rerun()

def show():
    username = st.session_state.user_info["username"]
    st.title("💬 Chats & Groups")
    tab1, tab2, tab3 = st.tabs(["📨 Direct Messages", "👥 Groups", "➕ Start New"])

    # Tab 1: DMs
    with tab1:
        st.subheader("📨 Start a conversation")
        target = st.text_input("Enter username")
        if st.button("Open Chat"):
            chat_id = "_".join(sorted([username, target]))
            st.session_state["current_dm"] = chat_id

        if "current_dm" in st.session_state:
            chat_path = os.path.join(CHAT_DIR, f"{st.session_state['current_dm']}.json")
            messages = load_chat(chat_path)
            display_chat(messages, chat_path, username)

    # Tab 2: Groups
    with tab2:
        st.subheader("👥 Your Groups")
        groups = load_groups()
        my_groups = [g for g in groups if g["visibility"] == "Public" or username in g.get("members", [])]

        for group in my_groups:
            with st.expander(group["name"]):
                st.markdown(f"📝 {group['description']}")

                # Owner tools
                if group.get("owner") == username:
                    st.warning("You are the group owner")
                    if st.button("🗑️ Delete Group", key=group["id"] + "_del"):
                        groups = [g for g in groups if g["id"] != group["id"]]
                        save_groups(groups)
                        st.success("Group deleted.")
                        st.experimental_rerun()
                    if group.get("pending"):
                        st.markdown("🔒 Pending join requests:")
                        for p in group["pending"]:
                            col1, col2 = st.columns(2)
                            col1.write(p)
                            if col2.button("✅ Approve", key=group["id"] + "_a_" + p):
                                group["members"].append(p)
                                group["pending"].remove(p)
                                save_groups(groups)
                                st.experimental_rerun()

                # Join handling
                if group["visibility"] == "Private" and username not in group["members"]:
                    if username not in group.get("pending", []):
                        if st.button("Request to Join", key=group["id"] + "_req"):
                            group.setdefault("pending", []).append(username)
                            save_groups(groups)
                            st.success("Request sent.")
                    else:
                        st.info("⏳ Request pending...")
                    continue

                # Group chat
                chat_path = os.path.join(GROUP_DIR, f"{group['id']}.json")
                messages = load_chat(chat_path)
                display_chat(messages, chat_path, username)

                with st.expander("📊 Create a poll"):
                    q = st.text_input("Poll question", key=group["id"] + "_q")
                    opts = st.text_area("Poll options (one per line)", key=group["id"] + "_opts")
                    if st.button("Send Poll", key=group["id"] + "_poll"):
                        poll = {
                            "question": q,
                            "options": [o.strip() for o in opts.splitlines() if o.strip()],
                            "votes": {}
                        }
                        send_chat(chat_path, username, f"📊 Poll: {q}", poll=poll)
                        st.success("Poll sent!")
                        st.experimental_rerun()

    # Tab 3: Create
    with tab3:
        st.subheader("➕ Start New")
        mode = st.radio("Choose", ["Direct Message", "Group Chat"])
        if mode == "Direct Message":
            target = st.text_input("Username")
            if st.button("Start Chat"):
                st.session_state["current_dm"] = "_".join(sorted([username, target]))
                st.success("Chat started!")
        else:
            name = st.text_input("Group Name")
            vis = st.selectbox("Visibility", ["Public", "Private"])
            desc = st.text_area("Description")
            if st.button("Create Group"):
                groups = load_groups()
                new_group = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "visibility": vis,
                    "description": desc,
                    "members": [username] if vis == "Private" else [],
                    "owner": username,
                    "pending": []
                }
                groups.append(new_group)
                save_groups(groups)
                st.success("Group created!")
                st.experimental_rerun()
