from app.ml.feature_builder import feature_builder
from app.ml.model_loader import model_loader


class Predictor:
    def __init__(self):
        model_loader.load()

    def predict(self, rainfall, offset=0):
        df = feature_builder.build(rainfall, offset=offset)
        zones = df["zone"]
        X = df.drop(columns=["zone"])
        X = X[model_loader.features]

        predictions = model_loader.model.predict(X)

        # Confidence is only meaningful when the model exposes probabilities.
        # Never present a hand-written rainfall heuristic as AI confidence.
        probabilities = None
        if hasattr(model_loader.model, "predict_proba"):
            try:
                probabilities = model_loader.model.predict_proba(X)
            except (AttributeError, ValueError):
                probabilities = None

        results = []
        for index, (zone, depth) in enumerate(zip(zones, predictions)):
            confidence = None
            if probabilities is not None and len(probabilities[index]):
                confidence = round(float(max(probabilities[index])), 3)

            results.append({
                "zone": zone,
                "depth_cm": round(float(depth), 2),
                "confidence": confidence,
            })

        return results


predictor = Predictor()
