# API Configuration Guide

Smart Water Irrigator relies on external APIs to fetch real-time data.

## OpenWeatherMap API

1. Go to [OpenWeatherMap](https://openweathermap.org/).
2. Create a free account.
3. Navigate to "My API Keys" in your profile dropdown.
4. Generate a new key.
5. Copy the key and paste it into your `.env` file under `OPENWEATHERMAP_API_KEY`.

Note: The free tier allows up to 1,000 calls per day, which is plenty for prototype testing and small-scale usage. It provides access to Current Weather Data which includes temperature, humidity, and wind speed.
