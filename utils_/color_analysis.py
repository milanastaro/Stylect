import os
import json
import numpy as np
from datetime import datetime
from PIL import Image
import cv2

PALETTE_FILE = "data/user_color_palettes.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Step 1: Analyze image and detect skin undertone
def analyze_face_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_roi = image[int(image.shape[0]*0.3):int(image.shape[0]*0.7),
                     int(image.shape[1]*0.3):int(image.shape[1]*0.7)]

    avg_color = np.mean(face_roi.reshape(-1, 3), axis=0)
    r, g, b = avg_color

    if r > g and r > b:
        return "warm"
    elif b > r and b > g:
        return "cool"
    else:
        return "neutral"

# Step 2: Return palette based on undertone
def get_color_palette(undertone):
    palettes = {
        "warm": {
            "name": "Spring/Summer",
            "swatches": ["#FFD700", "#FF8C00", "#FF6347", "#F4A460", "#DAA520"]
        },
        "cool": {
            "name": "Winter",
            "swatches": ["#4169E1", "#4682B4", "#5F9EA0", "#6A5ACD", "#2E8B57"]
        },
        "neutral": {
            "name": "Autumn",
            "swatches": ["#BDB76B", "#CD853F", "#8B4513", "#A0522D", "#556B2F"]
        }
    }
    return palettes.get(undertone, palettes["neutral"])

# Step 3: Save to user profile
def save_user_palette(username, undertone, palette):
    data = load_json(PALETTE_FILE)
    data[username] = {
        "undertone": undertone,
        "palette": palette,
        "analyzed_at": str(datetime.now())
    }
    save_json(PALETTE_FILE, data)

def load_user_palette(username):
    data = load_json(PALETTE_FILE)
    return data.get(username)
