import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

cities = ["Mumbai", "Delhi", "Kolkata", "Chennai", "Hyderabad"]

for city in cities:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    print(f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}")