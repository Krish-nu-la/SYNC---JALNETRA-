import pandas as pd

from app.ml.model_loader import model_loader
from app.services.hydrology_service import hydrology_service
from app.services.weather_service import weather_service
from app.services.zone_service import ZoneService


class FeatureBuilder:
    def __init__(self):
        self.zone_service = ZoneService()
        model_loader.load()

    def build(self, rainfall, offset=0):
        weather = weather_service.get_weather(rainfall, offset=offset)
        zones = self.zone_service.get_all_zones()
        rows = []

        for zone in zones:
            hydrology = hydrology_service.calculate(rainfall, zone, weather)

            land = model_loader.encoders["land_cover"].transform([zone["land_cover"]])[0]
            soil = model_loader.encoders["soil_type"].transform([zone["soil_type"]])[0]

            rainfall_discharge = rainfall * weather["river_discharge_m³_s"]
            rainfall_waterlevel = rainfall * weather["water_level_m"]
            terrain_risk = hydrology["runoff"]
            population_density = zone["population"] / 10
            population_risk = population_density * weather["historical_floods"]
            weather_severity = (
                rainfall + weather["temperature_c"] + weather["humidity_percent"]
            ) / 3
            infra_risk = 10 - weather["infrastructure"]

            rows.append({
                "latitude": zone["lat"],
                "longitude": zone["lng"],
                "rainfall_mm": rainfall,
                "temperature_c": weather["temperature_c"],
                "humidity_percent": weather["humidity_percent"],
                "river_discharge_m³_s": weather["river_discharge_m³_s"],
                "water_level_m": weather["water_level_m"],
                "elevation_m": zone["elevation"],
                "land_cover": land,
                "soil_type": soil,
                "population_density": population_density,
                "infrastructure": weather["infrastructure"],
                "historical_floods": weather["historical_floods"],
                "rainfall_discharge": rainfall_discharge,
                "rainfall_waterlevel": rainfall_waterlevel,
                "terrain_risk": terrain_risk,
                "population_risk": population_risk,
                "weather_severity": weather_severity,
                "infra_risk": infra_risk,
                "zone": zone,
            })

        return pd.DataFrame(rows)


feature_builder = FeatureBuilder()
