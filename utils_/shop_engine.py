import os
import json
import random

SHOP_FILE = "data/shop_listings.json"
BUNDLE_FILE = "data/shop_bundles.json"
INVENTORY_FOLDER = "data/shop_users/"

def load_shop_data():
    if not os.path.exists(SHOP_FILE):
        return []
    with open(SHOP_FILE, "r") as f:
        return json.load(f)

def search_products(prompt, filters=None):
    """
    Returns a list of items matching prompt and optional filters like color, brand, size.
    """
    listings = load_shop_data()
    results = []

    for item in listings:
        match = prompt.lower() in item["title"].lower() or any(prompt.lower() in tag.lower() for tag in item.get("tags", []))
        if filters:
            for key, value in filters.items():
                if key in item and item[key].lower() != value.lower():
                    match = False
        if match:
            results.append(item)

    return results

def get_user_shop_items(user_id):
    path = os.path.join(INVENTORY_FOLDER, f"{user_id}_inventory.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_user_shop_items(user_id, items):
    os.makedirs(INVENTORY_FOLDER, exist_ok=True)
    path = os.path.join(INVENTORY_FOLDER, f"{user_id}_inventory.json")
    with open(path, "w") as f:
        json.dump(items, f, indent=2)

def recommend_bundles(user_id):
    """
    Returns bundle suggestions (can later be filtered by interest or style).
    """
    if not os.path.exists(BUNDLE_FILE):
        return []
    with open(BUNDLE_FILE, "r") as f:
        all_bundles = json.load(f)

    return random.sample(all_bundles, min(len(all_bundles), 3))

def generate_ai_listing(image_file):
    """
    Placeholder: Given an image file, return a dummy AI-generated title, tags, and price.
    In future, this will use a vision model.
    """
    return {
        "title": "Ribbed Crop Top",
        "tags": ["pink", "crop", "casual", "summer"],
        "price": "$14.99"
    }
