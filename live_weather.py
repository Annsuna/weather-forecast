import requests
import pandas as pd
import matplotlib.pyplot as plt

LATITUDE = 37.4419
LONGITUDE = -122.1430

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "forecast_days": 3,
    "timezone": "America/Los_Angeles"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Request failed.")
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    exit()

data = response.json()

df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temperature_c": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "wind_speed": data["hourly"]["wind_speed_10m"]
})

df["time"] = pd.to_datetime(df["time"])

print(df.head())
print("\nData shape:", df.shape)

df.to_csv("palo_alto_weather.csv", index=False)
print("\nSaved to palo_alto_weather.csv")

plt.figure(figsize=(10, 5))
plt.plot(df["time"], df["temperature_c"], marker="o")
plt.title("Palo Alto Temperature Forecast")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
