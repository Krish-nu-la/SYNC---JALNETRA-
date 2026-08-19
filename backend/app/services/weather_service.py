import requests

from app.core.config import settings
from app.services.hydrology_inputs import hydrology_input_service
from app.services.cache_service import cache_service


class WeatherService:
    """Fetch current/forecast weather inputs used by the flood model."""

    def __init__(self):
        self.provider = settings.WEATHER_PROVIDER

    def get_weather(self, rainfall_override=None, offset=0):
        if self.provider == "slider":
            return self._slider_weather(rainfall_override)

        try:
            return self.get_openmeteo(
                offset=offset,
                rainfall_override=rainfall_override,
            )
        except (
            requests.RequestException,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            return self._slider_weather(rainfall_override)

    @staticmethod
    def _slider_weather(rainfall):
        rainfall = float(rainfall or 0)
        hydrology = hydrology_input_service.from_scenario(rainfall)

        return {
            "rainfall_mm": rainfall,
            "temperature_c": 29.0,
            "humidity_percent": 85.0,
            "river_discharge_m³_s": hydrology.river_discharge_m3_s,
            "water_level_m": hydrology.water_level_m,
            "historical_floods": hydrology.historical_floods,
            "infrastructure": hydrology.infrastructure,
            "source": "scenario",
            "hydrology_source": hydrology.source,
        }

    def get_openmeteo(self, offset=0, rainfall_override=None):

        # -------------------------------------------------
        # CACHE THE OPEN-METEO HOURLY FORECAST
        # -------------------------------------------------
        cache_key = "openmeteo:hourly"

        hourly = cache_service.get(cache_key)

        if hourly is None:

            url = settings.OPENMETEO_URL

            params = {
                "latitude": settings.WEATHER_LATITUDE,
                "longitude": settings.WEATHER_LONGITUDE,
                "forecast_days": 2,
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                ],
                "forecast_hours": 6,
            }

            response = requests.get(
                url,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            hourly = response.json()["hourly"]

            # Cache the forecast for 5 minutes.
            cache_service.set(
                cache_key,
                hourly,
            )

        # -------------------------------------------------
        # SELECT FORECAST FRAME
        # -------------------------------------------------

        index = min(
            max(int(round(offset / 60)), 0),
            len(hourly["temperature_2m"]) - 1,
        )

        forecast_rain = float(
            hourly["precipitation"][index] or 0
        )

        rainfall = (
            float(rainfall_override)
            if offset == 0 and rainfall_override is not None
            else forecast_rain
        )

        temperature = float(
            hourly["temperature_2m"][index]
        )

        humidity = float(
            hourly["relative_humidity_2m"][index]
        )

        # -------------------------------------------------
        # HYDROLOGY
        # -------------------------------------------------

        hydrology = hydrology_input_service.from_scenario(
            rainfall
        )

        return {
            "rainfall_mm": rainfall,
            "temperature_c": temperature,
            "humidity_percent": humidity,
            "river_discharge_m³_s": hydrology.river_discharge_m3_s,
            "water_level_m": hydrology.water_level_m,
            "historical_floods": hydrology.historical_floods,
            "infrastructure": hydrology.infrastructure,
            "source": "open-meteo",
            "hydrology_source": hydrology.source,
        }


weather_service = WeatherService()