from app.services.forecast_service import forecast_service


class AlertService:

    def generate(self, rainfall):

        forecast = forecast_service.generate(rainfall)

        latest = forecast["frames"][-1]

        alerts = []

        for zone in latest["zones"]:

            if zone["level"] == "safe":
                continue

            alerts.append({

                "zone": zone["name"],

                "level": zone["level"],

                "depthCm": zone["depthCm"],

                "trend": zone["trend"],

                "population": zone["population"],

                "message":

                    f"{zone['depthCm']} cm water expected."

            })

        alerts.sort(

            key=lambda x: x["depthCm"],

            reverse=True

        )

        return alerts


alert_service = AlertService()