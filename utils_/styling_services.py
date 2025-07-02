import json
import os
import uuid
from datetime import datetime

SERVICES_FILE = "data/styling_services.json"
BOOKINGS_FILE = "data/styling_bookings.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Add a new styling service
def add_service(stylist, title, description, price, tags):
    services = load_json(SERVICES_FILE)
    service_id = str(uuid.uuid4())
    services[service_id] = {
        "stylist": stylist,
        "title": title,
        "description": description,
        "price": price,
        "tags": tags,
        "created_at": str(datetime.now())
    }
    save_json(SERVICES_FILE, services)
    return service_id

# Get all services or filter by tag/keyword
def get_services(keyword=None):
    services = load_json(SERVICES_FILE)
    if not keyword:
        return services
    return {
        sid: s for sid, s in services.items()
        if keyword.lower() in s["title"].lower() or keyword.lower() in s["description"].lower()
    }

# Get all services by one stylist
def get_stylist_services(username):
    services = load_json(SERVICES_FILE)
    return {
        sid: s for sid, s in services.items()
        if s["stylist"] == username
    }

# Book a styling service
def book_service(service_id, buyer):
    bookings = load_json(BOOKINGS_FILE)
    booking_id = str(uuid.uuid4())
    bookings[booking_id] = {
        "service_id": service_id,
        "buyer": buyer,
        "booked_at": str(datetime.now())
    }
    save_json(BOOKINGS_FILE, bookings)
    return booking_id

# Get all bookings for a user
def get_user_bookings(username):
    bookings = load_json(BOOKINGS_FILE)
    return {
        bid: b for bid, b in bookings.items()
        if b["buyer"] == username
    }
