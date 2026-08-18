import requests

from app.core.config import settings


class WeatherService:
    """Fetch current/forecast weather inputs used by the flood model."""

    def __init__(self):
        self.provider = settings.WEATHER_PROVIDER

    def get_weather(self, rainfall_override=None, offset=0):
        if self.provider == "slider":
            return self._slider_weather(rainfall_override)

        try:
            return self.get_openmeteo(offset=offset, rainfall_override=rainfall_override)
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
            # Keep the prediction API usable if the external weather provider is down.
            return self._slider_weather(rainfall_override)

    @staticmethod
    def _slider_weather(rainfall):
        rainfall = float(rainfall or 0)
        return {
            "rainfall_mm": rainfall,
            "temperature_c": 29.0,
            "humidity_percent": 85.0,
            "river_discharge_m³_s": rainfall * 2.0,
            "water_level_m": rainfall / 100.0,
            "historical_floods": 4,
            "infrastructure": 7,
            "source": "scenario",
        }

    def get_openmeteo(self, offset=0, rainfall_override=None):
        # Open-Meteo hourly data gives us a genuinely different weather input
        # for each 30-minute forecast frame instead of ignoring `offset`.
        url = settings.OPENMETEO_URL
        horizon_hours = max(2, (offset // 60) + 2)
        params = {
            "latitude": settings.WEATHER_LATITUDE,
            "longitude": settings.WEATHER_LONGITUDE,
            "forecast_days": 2,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
            ],
            "forecast_hours": horizon_hours,
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        hourly = response.json()["hourly"]

        # A 30-minute frame maps to the nearest available hourly forecast.
        index = min(max(int(round(offset / 60)), 0), len(hourly["temperature_2m"]) - 1)
        forecast_rain = float(hourly["precipitation"][index] or 0)
        rainfall = float(rainfall_override) if offset == 0 and rainfall_override is not None else forecast_rain
        temperature = float(hourly["temperature_2m"][index])
        humidity = float(hourly["relative_humidity_2m"][index])

        return {
            "rainfall_mm": rainfall,
            "temperature_c": temperature,
            "humidity_percent": humidity,
            # These are proxy inputs until live river/gauge feeds are integrated.
            "river_discharge_m³_s": rainfall * 2.0,
            "water_level_m": rainfall / 100.0,
            "historical_floods": 4,
            "infrastructure": 7,
            "source": "open-meteo",
        }


weather_service = WeatherService()
