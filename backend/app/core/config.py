from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "JalNetra API"
    VERSION: str = "1.1.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MODEL_PATH: str = "app/ml/models/flood_model.pkl"
    ENCODERS_PATH: str = "app/ml/models/encoders.pkl"
    FEATURE_COLUMNS_PATH: str = "app/ml/models/feature_columns.pkl"

    ZONES_PATH: str = "app/data/zones.csv"
    LOG_DIR: str = "logs"

    WEATHER_PROVIDER: str = "openmeteo"
    OPENMETEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    WEATHER_LATITUDE: float = 9.98
    WEATHER_LONGITUDE: float = 76.28

    # Comma-separated origins. Use * only for local/demo deployments.
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500"


settings = Settings()
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def cors_origins() -> list[str]:
    return [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
