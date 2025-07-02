import json
import os
import uuid
from PIL import Image

WARDROBE_FILE = "data/wardrobes.json"
WARDROBE_IMAGE_FOLDER = "wardrobe_images"

# Ensure folders and file exist
def initialize_wardrobe_storage():
    os.makedirs("data", exist_ok=True)
    os.makedirs(WARDROBE_IMAGE_FOLDER, exist_ok=True)
    if not os.path.exists(WARDROBE_FILE):
        with open(WARDROBE_FILE, "w") as f:
            json.dump({}, f)

# Load all wardrobes
def load_all_wardrobes():
    initialize_wardrobe_storage()
    with open(WARDROBE_FILE, "r") as f:
        return json.load(f)

# Save all wardrobes
def save_all_wardrobes(data):
    with open(WARDROBE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Get wardrobe for a specific user
def get_user_wardrobe(username):
    wardrobes = load_all_wardrobes()
    return wardrobes.get(username, [])

# ✅ Save wardrobe item and uploaded image
def save_wardrobe_item(username, item, image_file=None):
    initialize_wardrobe_storage()
    wardrobes = load_all_wardrobes()

    # Save image if provided
    if image_file is not None:
        file_extension = os.path.splitext(image_file.name)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        image_path = os.path.join(WARDROBE_IMAGE_FOLDER, unique_filename)

        # Save image to disk
        image = Image.open(image_file)
        image.save(image_path)
        item["image"] = unique_filename
    else:
        item["image"] = None

    if username not in wardrobes:
        wardrobes[username] = []
    wardrobes[username].append(item)

    save_all_wardrobes(wardrobes)

# ✅ Remove an item by index
def remove_wardrobe_item(username, index):
    wardrobes = load_all_wardrobes()
    if username in wardrobes and 0 <= index < len(wardrobes[username]):
        item = wardrobes[username].pop(index)

        # Delete image file if it exists
        if item.get("image"):
            image_path = os.path.join(WARDROBE_IMAGE_FOLDER, item["image"])
            if os.path.exists(image_path):
                os.remove(image_path)

        save_all_wardrobes(wardrobes)
        return True
    return False
