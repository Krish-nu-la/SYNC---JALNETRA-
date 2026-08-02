import joblib
from pathlib import Path

from app.core.logger import logger


class ModelLoader:

    def __init__(self):

        self.model = None
        self.encoders = None
        self.features = None

    def load(self):

        if self.model is not None:
            return self.model

        model_dir = Path("app/ml/models")

        self.model = joblib.load(
            model_dir / "flood_model.pkl"
        )

        self.encoders = joblib.load(
            model_dir / "encoders.pkl"
        )

        self.features = joblib.load(
            model_dir / "feature_columns.pkl"
        )

        logger.info("AI Model Loaded")

        return self.model


model_loader = ModelLoader()