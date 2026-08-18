class AlertService:

    def evaluate(
        self,
        depth_cm: float,
        risk: float,
        level: str,
        trend: str,
        recent_reports: int = 0,
        blocked_roads: int = 0,
    ):

        reasons = []

        # AI risk
        if level == "severe":

            alert = "severe"

            reasons.append(
                "Predicted water depth is in the severe range."
            )

        elif level == "high":

            alert = "high"

            reasons.append(
                "Predicted waterlogging is high."
            )

        elif level == "watch":

            alert = "watch"

            reasons.append(
                "Surface water is expected."
            )

        else:

            alert = "safe"

        # Rising water
        if trend == "rising":

            reasons.append(
                "Recent citizen reports indicate rising water levels."
            )

            if alert == "safe":
                alert = "watch"

            elif alert == "watch":
                alert = "high"

        # Multiple recent reports
        if recent_reports >= 3:

            reasons.append(
                f"{recent_reports} recent citizen reports were received."
            )

            if alert == "safe":
                alert = "watch"

        # Road blockage
        if blocked_roads > 0:

            reasons.append(
                f"{blocked_roads} recent report(s) indicate road blockage."
            )

            if alert in ["safe", "watch"]:
                alert = "high"

        recommendations = {

            "safe":
                "No significant flooding expected. Normal travel is advised.",

            "watch":
                "Monitor conditions and avoid unnecessary travel through low-lying roads.",

            "high":
                "Avoid waterlogged routes and consider alternative roads.",

            "severe":
                "Avoid travel through the affected zone and move to safer ground if necessary."
        }

        return {

            "alertLevel": alert,

            "triggered": alert != "safe",

            "reasons": reasons,

            "recommendation":
                recommendations[alert]

        }


alert_service = AlertService()