from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global application settings.
    """

    APP_NAME: str = "JalNetra API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MODEL_PATH: str = "app/ml/models/flood_model.pkl"

    ZONES_PATH: str = "app/data/zones.csv"

    LOG_DIR: str = "logs"

    WEATHER_PROVIDER: str = "slider"

    WINDY_API_KEY: str = ""

    OPENMETEO_URL: str = "https://api.open-meteo.com/v1/forecast"

    class Config:
        env_file = ".env"


settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent