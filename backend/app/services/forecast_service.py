from datetime import datetime

from app.services.prediction_service import prediction_service
from app.services.cache_service import cache_service


class ForecastService:

    OFFSETS = [0, 30, 60, 90, 120]

    def generate(self, rainfall):

        # ----------------------------
        # Check Cache
        # ----------------------------
        cache_key = f"forecast_{rainfall}"

        cached = cache_service.get(cache_key)

        if cached:
            return cached

        # ----------------------------
        # Generate Forecast
        # ----------------------------
        frames = []

        for offset in self.OFFSETS:

            prediction = prediction_service.predict(
                rainfall=rainfall,
                offset=offset
            )

            frames.append({

                "offset": offset,

                "generatedAt": prediction["generatedAt"],

                "processingTimeMs": prediction["processingTimeMs"],

                "zones": prediction["zones"]

            })

        # ----------------------------
        # Final Result
        # ----------------------------
        result = {

            "generatedAt": datetime.utcnow().isoformat() + "Z",

            "rainfallMmHr": rainfall,

            "frames": frames

        }

        # ----------------------------
        # Save in Cache
        # ----------------------------
        cache_service.set(
            cache_key,
            result
        )

        return result


forecast_service = ForecastService()