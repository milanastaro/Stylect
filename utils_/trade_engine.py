import json
import os
import uuid
from datetime import datetime

PENDING_FILE = "data/trades_pending.json"
HISTORY_FILE = "data/trades_history.json"
REPUTATION_FILE = "data/trade_reputation.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def send_trade_request(from_user, to_user, item_from, item_to):
    trades = load_json(PENDING_FILE)

    trade_id = str(uuid.uuid4())
    trades[trade_id] = {
        "from": from_user,
        "to": to_user,
        "item_from": item_from,
        "item_to": item_to,
        "status": "pending",
        "timestamp": str(datetime.now())
    }

    save_json(PENDING_FILE, trades)
    return trade_id

def get_pending_trades(user):
    trades = load_json(PENDING_FILE)
    return {tid: t for tid, t in trades.items() if t["to"] == user or t["from"] == user}

def respond_to_trade(trade_id, accept=True):
    trades = load_json(PENDING_FILE)
    history = load_json(HISTORY_FILE)
    reputation = load_json(REPUTATION_FILE)

    if trade_id not in trades:
        return False

    trade = trades[trade_id]
    trade["status"] = "accepted" if accept else "rejected"
    trade["resolved_at"] = str(datetime.now())

    # Move to history
    history[trade_id] = trade
    save_json(HISTORY_FILE, history)

    # Remove from pending
    del trades[trade_id]
    save_json(PENDING_FILE, trades)

    # Update reputation (basic)
    if accept:
        reputation[trade["from"]] = reputation.get(trade["from"], 0) + 1
        reputation[trade["to"]] = reputation.get(trade["to"], 0) + 1
        save_json(REPUTATION_FILE, reputation)

    return True

def get_trade_history(user):
    history = load_json(HISTORY_FILE)
    return {tid: t for tid, t in history.items() if t["to"] == user or t["from"] == user}

def get_trade_reputation(user):
    rep = load_json(REPUTATION_FILE)
    return rep.get(user, 0)

def generate_dual_shipping_labels(item_from, item_to):
    # Placeholder for label logic
    return {
        "from_label": f"Shipping label for: {item_from['title']} (→ {item_to['owner']})",
        "to_label": f"Shipping label for: {item_to['title']} (→ {item_from['owner']})"
    }

REVIEW_FILE = "data/trade_reviews.json"

def submit_trade_review(user, from_user, trade_id, rating, comment):
    reviews = load_json(REVIEW_FILE)
    review = {
        "from": from_user,
        "trade_id": trade_id,
        "rating": rating,
        "comment": comment,
        "date": str(datetime.now().date())
    }

    if user not in reviews:
        reviews[user] = []

    # Check for duplicate review for same trade
    if any(r["trade_id"] == trade_id and r["from"] == from_user for r in reviews[user]):
        return False  # Prevent duplicate reviews

    reviews[user].append(review)
    save_json(REVIEW_FILE, reviews)
    return True

def get_trade_reviews(user):
    reviews = load_json(REVIEW_FILE)
    return reviews.get(user, [])

def calculate_trade_rating(user):
    reviews = get_trade_reviews(user)
    if not reviews:
        return None
    total = sum(r["rating"] for r in reviews)
    return round(total / len(reviews), 2)
