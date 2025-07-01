def get_user_color_palette(username):
    path = f"data/users/{username}_palette.json"
    if os.path.exists(path):
        import json
        with open(path, "r") as f:
            return json.load(f).get("colors", [])
    return []
