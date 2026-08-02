from app.services.forecast_service import forecast_service


class DashboardService:

    def build(self, rainfall):

        forecast = forecast_service.generate(rainfall)

        latest = forecast["frames"][-1]

        zones = latest["zones"]

        deepest = max(
            zones,
            key=lambda z: z["depthCm"]
        )

        avg_risk = sum(
            z["risk"] for z in zones
        ) / len(zones)

        warning = len(
            [
                z for z in zones
                if z["level"] in ["high", "severe"]
            ]
        )

        population = sum(
            z["population"]
            for z in zones
            if z["level"] != "safe"
        )

        if deepest["depthCm"] >= 50:
            action = "EVACUATE"

        elif deepest["depthCm"] >= 25:
            action = "PREPARE"

        elif deepest["depthCm"] >= 10:
            action = "WATCH"

        else:
            action = "SAFE"

        return {

            "generatedAt": forecast["generatedAt"],

            "deepestZone": deepest["name"],

            "deepestDepth": deepest["depthCm"],

            "riskIndex": round(avg_risk, 2),

            "zonesInWarning": warning,

            "populationAffected": population,

            "recommendedAction": action

        }


dashboard_service = DashboardService()