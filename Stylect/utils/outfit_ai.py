import random

def suggest_outfit(
    wardrobe,
    weather=None,
    occasion=None,
    mood=None,
    preferred_colors=None,
    use_color_palette=False,
    username=None,
    base_items=None,
    prompt=None
):
    """
    Returns a list of wardrobe items to form an outfit, based on weather, style preferences,
    selected base items, and free-form prompts.
    """
    from utils.db import get_user_color_palette

    filtered = wardrobe

    # Apply color filter
    if preferred_colors:
        filtered = [item for item in filtered if any(
            color.lower() in item.get("tags", []) for color in preferred_colors
        )]

    # Apply color palette filter
    if use_color_palette and username:
        palette = get_user_color_palette(username)
        if palette:
            filtered = [item for item in filtered if any(
                color.lower() in item.get("tags", []) for color in palette
            )]

    # Apply mood / aesthetic filter
    if mood and mood.lower() != "neutral":
        filtered = [item for item in filtered if mood.lower() in [t.lower() for t in item.get("tags", [])]]

    # Add base items if selected (e.g., “Use this skirt”)
    outfit = base_items.copy() if base_items else []

    # Weather-based logic
    if weather:
        temp = weather["temperature"]
        description = weather["description"].lower()

        if temp < 15 or "rain" in description:
            outerwear = [i for i in filtered if i["category"].lower() == "outerwear"]
            if outerwear and not any(i for i in outfit if i["category"].lower() == "outerwear"):
                outfit.append(random.choice(outerwear))

    # Suggest missing core items if not already chosen
    categories_needed = ["top", "bottom", "shoes"]
    for cat in categories_needed:
        if not any(i for i in outfit if i["category"].lower() == cat):
            options = [i for i in filtered if i["category"].lower() == cat]
            if options:
                outfit.append(random.choice(options))

    # Optionally add accessories
    accessories = [i for i in filtered if i["category"].lower() == "accessories"]
    if accessories and random.random() > 0.4:
        outfit.append(random.choice(accessories))

    return outfit


def suggest_products_to_buy(prompt):
    """
    Given a user prompt like 'black mini skirt', return dummy product suggestions.
    Later, this will hook into real APIs or product scrapers.
    """
    # Placeholder product search results
    sample_items = [
        {
            "name": "High-Waisted Black Mini Skirt",
            "price": "$39.99",
            "image": "https://example.com/skirt.jpg",
            "link": "https://shop.example.com/skirt"
        },
        {
            "name": "Pleated Faux Leather Mini Skirt",
            "price": "$49.95",
            "image": "https://example.com/leather-skirt.jpg",
            "link": "https://shop.example.com/leather"
        },
        {
            "name": "Stretch Knit Mini Skirt - Black",
            "price": "$29.90",
            "image": "https://example.com/knit-skirt.jpg",
            "link": "https://shop.example.com/knit"
        }
    ]
    return sample_items
