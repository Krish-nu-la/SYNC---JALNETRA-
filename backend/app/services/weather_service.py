import requests

from app.core.config import settings


class WeatherService:

    def __init__(self):

        self.provider = settings.WEATHER_PROVIDER

    def get_weather(
        self,
        rainfall_override=None
    ):

        if self.provider == "slider":

            rainfall = rainfall_override

            return {

                "rainfall_mm": rainfall,

                "temperature_c": 29,

                "humidity_percent": 85,

                "river_discharge_m³_s": rainfall * 2,

                "water_level_m": rainfall / 100,

                "historical_floods": 4,

                "infrastructure": 7

            }

        return self.get_openmeteo()

    def get_openmeteo(self):

        url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        params = {

            "latitude": 9.98,

            "longitude": 76.28,

            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation"
            ]

        }

        response = requests.get(

            url,

            params=params,

            timeout=10

        )

        data = response.json()["current"]

        rainfall = data.get(

            "precipitation",

            0

        )

        return {

            "rainfall_mm": rainfall,

            "temperature_c": data["temperature_2m"],

            "humidity_percent": data["relative_humidity_2m"],

            "river_discharge_m³_s": rainfall * 2,

            "water_level_m": rainfall / 100,

            "historical_floods": 4,

            "infrastructure": 7

        }


weather_service = WeatherService()

