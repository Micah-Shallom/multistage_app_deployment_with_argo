

import requests

API_KEY = "e1a86fb0740d40ce8bd202845231103"  # Replace with your actual API key
CITY = "New York"  # Replace with the name of the city you want to fetch the weather for
DAYS = 5  # Number of days of forecast to retrieve

url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days={DAYS}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for forecast in data['forecast']['forecastday']:
        date = forecast['date']
        condition = forecast['day']['condition']['text']
        temp = forecast['day']['avgtemp_f']
        print(f"{date}: {condition}, {temp} F")
else:
    print(f"Failed to fetch forecast for {CITY}. Status code: {response.status_code}")
