from app.services.zone_service import ZoneService

zone_service = ZoneService()


class ExplanationService:

    def explain(self, zone_id, depth):

        zone = zone_service.get_zone(zone_id)

        if zone is None:

            return None

        reasons = []

        if zone["elevation"] < 3:

            reasons.append(

                "Low elevation increases water accumulation."

            )

        if zone["susceptibility"] > 0.8:

            reasons.append(

                "High flood susceptibility."

            )

        if zone["drain_capacity"] < 20:

            reasons.append(

                "Limited drainage capacity."

            )

        if depth > 25:

            reasons.append(

                "Predicted water depth exceeds the alert threshold."

            )

        return {

            "zone": zone["name"],

            "depthCm": depth,

            "explanation": reasons

        }


explanation_service = ExplanationService()