from datetime import datetime
import time

from app.ml.predictor import predictor
from app.services.risk_service import risk_service


class PredictionService:

    def predict(
        self,
        rainfall,
        offset
    ):

        # Start timer
        start = time.perf_counter()

        # AI Prediction
        predictions = predictor.predict(
            rainfall,
            offset
        )

        zones = []

        for p in predictions:

            zone = p["zone"]

            result = risk_service.calculate(
                p["depth_cm"]
            )

            zones.append({

                "id": zone["id"],

                "name": zone["name"],

                "lat": zone["lat"],

                "lng": zone["lng"],

                "depthCm": result["depthCm"],

                "risk": result["risk"],

                "level": result["level"],

                "population": zone["population"],

                "trend": "steady",

                # AI Confidence
                "confidence": p["confidence"]

            })

        # Stop timer
        processing_time = (
            time.perf_counter() - start
        ) * 1000

        return {

            "generatedAt": datetime.utcnow().isoformat() + "Z",

            "processingTimeMs": round(
                processing_time,
                2
            ),

            "rainfallMmHr": rainfall,

            "timeOffsetMin": offset,

            "zones": zones

        }


prediction_service = PredictionService()