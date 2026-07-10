import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

url = f"https://api.openweathermap.org/data/2.5/weather?q=Bangalore&appid={api_key}&units=metric"

response = requests.get(url)

print("Status code:", response.status_code)

data = response.json()
print("City:", data["name"])
print("Temperature:", data["main"]["temp"], "°C")
print("Weather:", data["weather"][0]["description"])
