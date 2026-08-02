from app.services.forecast_service import forecast_service


class AnalyticsService:

    def generate(self, rainfall):

        forecast = forecast_service.generate(rainfall)

        latest = forecast["frames"][-1]

        zones = latest["zones"]

        depths = [z["depthCm"] for z in zones]

        analytics = {

            "averageDepth": round(sum(depths) / len(depths), 2),

            "maximumDepth": max(depths),

            "minimumDepth": min(depths),

            "safeZones": len([z for z in zones if z["level"] == "safe"]),

            "watchZones": len([z for z in zones if z["level"] == "watch"]),

            "highZones": len([z for z in zones if z["level"] == "high"]),

            "severeZones": len([z for z in zones if z["level"] == "severe"]),

            "populationAffected": sum(

                z["population"]

                for z in zones

                if z["level"] != "safe"

            )

        }

        return analytics


analytics_service = AnalyticsService()