from app.core.constants import (
    SAFE_LIMIT,
    WATCH_LIMIT,
    HIGH_LIMIT,
)


class RiskService:

    def calculate(self, depth_cm: float):

        risk = min(1.0, depth_cm / 75)

        if depth_cm < SAFE_LIMIT:

            level = "safe"

            recommendation = "No significant water expected."

        elif depth_cm < WATCH_LIMIT:

            level = "watch"

            recommendation = "Surface water on roads. Drive slowly."

        elif depth_cm < HIGH_LIMIT:

            level = "high"

            recommendation = "Waterlogging likely. Avoid low-lying routes."

        else:

            level = "severe"

            recommendation = "Deep flooding. Avoid travel."

        return {

            "depthCm": round(depth_cm, 2),

            "risk": round(risk, 2),

            "level": level,

            "recommendation": recommendation

        }


risk_service = RiskService()