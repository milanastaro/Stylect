import json
import os
import bcrypt

USER_DATA_FILE = "data/users.json"

def initialize_user_storage():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)

def load_users():
    initialize_user_storage()
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup_user(username, password, email, phone, security_answers):
    users = load_users()
    if username in users:
        return False, "Username already exists."

    users[username] = {
        "password": hash_password(password),
        "email": email,
        "phone": phone,
        "security_answers": security_answers
    }

    save_users(users)
    return True, "Account created successfully!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found."
    if not verify_password(password, users[username]["password"]):
        return False, "Incorrect password."
    return True, "Login successful."
