import datetime
import requests
import os

CACHE_FILE = "data/holidays_cache.json"

def fetch_holidays_from_api(year=2025, country_code="US"):
    """
    Pulls international holiday data from the Nager.Date API and caches it.
    """
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    try:
        response = requests.get(url)
        data = response.json()

        # Save a simplified cache by MM-DD
        simplified = {}
        for holiday in data:
            date = holiday["date"]  # Format: 2025-12-25
            name = holiday["name"]
            month_day = "-".join(date.split("-")[1:])
            simplified.setdefault(month_day, []).append(name)

        os.makedirs("data", exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            import json
            json.dump(simplified, f, indent=2)

        return simplified

    except Exception as e:
        print("Failed to fetch holidays:", e)
        return {}

def load_cached_holidays():
    if not os.path.exists(CACHE_FILE):
        return fetch_holidays_from_api()
    import json
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def get_holidays_for_date(month, day):
    holidays = load_cached_holidays()
    key = f"{month:02d}-{day:02d}"
    return holidays.get(key, [])

def get_today_holidays():
    now = datetime.datetime.now()
    return get_holidays_for_date(now.month, now.day)

def get_holiday_styling(date=None):
    if not date:
        date = datetime.datetime.now()

    month, day = date.month, date.day
    holidays = get_holidays_for_date(month, day)

    suggestions = {
        "Valentine": {"colors": ["red", "pink"], "styles": ["romantic", "feminine"]},
        "Halloween": {"colors": ["black", "orange"], "styles": ["edgy", "costume"]},
        "Christmas": {"colors": ["red", "green", "gold"], "styles": ["cozy", "festive"]},
        "Easter": {"colors": ["pastels"], "styles": ["soft", "spring"]},
        "Independence": {"colors": ["red", "white", "blue"], "styles": ["patriotic"]},
        "New Year": {"colors": ["silver", "black", "gold"], "styles": ["party", "formal"]}
    }

    matched = []
    for h in holidays:
        for keyword, theme in suggestions.items():
            if keyword.lower() in h.lower():
                matched.append({
                    "holiday": h,
                    "theme": theme
                })
    return matched
