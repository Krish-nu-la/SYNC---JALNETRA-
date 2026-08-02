import pandas as pd

from app.ml.model_loader import model_loader
from app.ml.feature_builder import feature_builder


class Predictor:

    def __init__(self):

        model_loader.load()

    def predict(self, rainfall, offset):

        df = feature_builder.build(
            rainfall,
            offset
        )

        zones = df["zone"]

        X = df.drop(columns=["zone"])

        # Keep feature order exactly as during training
        X = X[model_loader.features]

        predictions = model_loader.model.predict(X)

        results = []

        for zone, depth in zip(zones, predictions):

            # Confidence based on rainfall (simple heuristic)
            if rainfall <= 20:
                confidence = 0.98
            elif rainfall <= 40:
                confidence = 0.96
            elif rainfall <= 60:
                confidence = 0.94
            elif rainfall <= 80:
                confidence = 0.91
            else:
                confidence = 0.88

            results.append({
                "zone": zone,
                "depth_cm": round(float(depth), 2),
                "confidence": confidence
            })

        return results


predictor = Predictor()