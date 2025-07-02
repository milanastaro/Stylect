from dotenv import load_dotenv
import os
import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")

def get_current_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=New York&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
    except:
        return None
