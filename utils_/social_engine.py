import json
import os
import uuid
from datetime import datetime

FOLLOW_FILE = "data/following.json"
POST_FILE = "data/posts.json"
GROUP_FILE = "data/groups.json"
CHAT_FILE = "data/chats.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- FOLLOWING ---------------- #
def follow_user(follower, target):
    data = load_json(FOLLOW_FILE)
    data.setdefault(follower, {"following": [], "followers": []})
    data.setdefault(target, {"following": [], "followers": []})

    if target not in data[follower]["following"]:
        data[follower]["following"].append(target)
    if follower not in data[target]["followers"]:
        data[target]["followers"].append(follower)
    save_json(FOLLOW_FILE, data)

def unfollow_user(follower, target):
    data = load_json(FOLLOW_FILE)
    data.setdefault(follower, {"following": [], "followers": []})
    data.setdefault(target, {"following": [], "followers": []})

    if target in data[follower]["following"]:
        data[follower]["following"].remove(target)
    if follower in data[target]["followers"]:
        data[target]["followers"].remove(follower)
    save_json(FOLLOW_FILE, data)

def get_follow_data(username):
    data = load_json(FOLLOW_FILE)
    return data.get(username, {"following": [], "followers": []})


# ---------------- POSTS ---------------- #
def create_post(username, image_url, caption, allow_voting=False):
    posts = load_json(POST_FILE)
    post_id = str(uuid.uuid4())
    posts[post_id] = {
        "user": username,
        "image": image_url,
        "caption": caption,
        "emoji_reactions": {},
        "comments": [],
        "allow_voting": allow_voting,
        "created_at": str(datetime.now())
    }
    save_json(POST_FILE, posts)
    return post_id

def react_to_post(post_id, emoji, username):
    posts = load_json(POST_FILE)
    if post_id not in posts:
        return
    posts[post_id]["emoji_reactions"].setdefault(emoji, [])
    if username not in posts[post_id]["emoji_reactions"][emoji]:
        posts[post_id]["emoji_reactions"][emoji].append(username)
    save_json(POST_FILE, posts)

def comment_on_post(post_id, username, comment):
    posts = load_json(POST_FILE)
    if post_id not in posts:
        return
    posts[post_id]["comments"].append({
        "user": username,
        "comment": comment,
        "time": str(datetime.now())
    })
    save_json(POST_FILE, posts)

def get_all_posts():
    return load_json(POST_FILE)


# ---------------- GROUPS ---------------- #
def create_group(name, creator, is_private=False):
    groups = load_json(GROUP_FILE)
    group_id = str(uuid.uuid4())
    groups[group_id] = {
        "name": name,
        "creator": creator,
        "members": [creator],
        "is_private": is_private,
        "requests": [],
        "created_at": str(datetime.now())
    }
    save_json(GROUP_FILE, groups)
    return group_id

def join_group(group_id, username):
    groups = load_json(GROUP_FILE)
    group = groups.get(group_id)
    if not group:
        return
    if group["is_private"]:
        if username not in group["requests"]:
            group["requests"].append(username)
    else:
        if username not in group["members"]:
            group["members"].append(username)
    save_json(GROUP_FILE, groups)

def approve_group_member(group_id, username):
    groups = load_json(GROUP_FILE)
    group = groups.get(group_id)
    if group and username in group["requests"]:
        group["requests"].remove(username)
        group["members"].append(username)
        save_json(GROUP_FILE, groups)

def get_user_groups(username):
    groups = load_json(GROUP_FILE)
    return {gid: g for gid, g in groups.items() if username in g["members"]}


# ---------------- CHATS ---------------- #
def send_chat_message(chat_id, sender, message):
    chats = load_json(CHAT_FILE)
    chats.setdefault(chat_id, [])
    chats[chat_id].append({
        "sender": sender,
        "message": message,
        "time": str(datetime.now())
    })
    save_json(CHAT_FILE, chats)

def get_chat(chat_id):
    chats = load_json(CHAT_FILE)
    return chats.get(chat_id, [])
