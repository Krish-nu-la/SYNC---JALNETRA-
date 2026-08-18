from datetime import datetime, timedelta
import time

from sqlalchemy.orm import Session

from app.ml.predictor import predictor
from app.services.risk_service import risk_service
from app.services.alert_service import alert_service
from app.models.report import Report


class PredictionService:

    def predict(
        self,
        rainfall,
        offset,
        db: Session | None = None
    ):

        start = time.perf_counter()

        predictions = predictor.predict(
            rainfall,
            offset
        )

        zones = []

        for p in predictions:

            zone = p["zone"]

            # AI flood prediction
            result = risk_service.calculate(
                p["depth_cm"]
            )

            # Citizen report trend
            trend = self._calculate_trend(
                db,
                zone["id"]
            )

            # Recent citizen reports
            recent_reports = self._recent_report_count(
                db,
                zone["id"]
            )

            # Blocked roads
            blocked_roads = self._blocked_report_count(
                db,
                zone["id"]
            )

            # Alert engine
            alert = alert_service.evaluate(
                depth_cm=result["depthCm"],
                risk=result["risk"],
                level=result["level"],
                trend=trend,
                recent_reports=recent_reports,
                blocked_roads=blocked_roads
            )

            zones.append({

                "id": zone["id"],

                "name": zone["name"],

                "lat": zone["lat"],

                "lng": zone["lng"],

                "depthCm": result["depthCm"],

                "risk": result["risk"],

                "level": result["level"],

                "recommendation": alert["recommendation"],

                "population": zone["population"],

                "trend": trend,

                "confidence": p["confidence"],

                "alertLevel": alert["alertLevel"],

                "alertTriggered": alert["triggered"],

                "alertReasons": alert["reasons"],

                "recentReports": recent_reports,

                "blockedRoadReports": blocked_roads

            })

        processing_time = (
            time.perf_counter() - start
        ) * 1000

        return {

            "generatedAt":
                datetime.utcnow().isoformat() + "Z",

            "processingTimeMs":
                round(processing_time, 2),

            "rainfallMmHr":
                rainfall,

            "timeOffsetMin":
                offset,

            "zones":
                zones

        }

    # ==========================================
    # TREND
    # ==========================================

    def _calculate_trend(
        self,
        db: Session | None,
        zone_id: str
    ):

        if db is None:
            return "steady"

        since = (
            datetime.utcnow()
            - timedelta(minutes=60)
        )

        reports = (
            db.query(Report)
            .filter(
                Report.zone.ilike(zone_id),
                Report.created_at >= since,
                Report.depth_cm.isnot(None)
            )
            .order_by(
                Report.created_at.asc()
            )
            .all()
        )

        if len(reports) < 2:
            return "steady"

        # Compare latest two reports
        previous = reports[-2].depth_cm
        current = reports[-1].depth_cm

        difference = current - previous

        if difference >= 5:
            return "rising"

        if difference <= -5:
            return "falling"

        return "steady"

    # ==========================================
    # RECENT REPORT COUNT
    # ==========================================

    def _recent_report_count(
        self,
        db: Session | None,
        zone_id: str
    ):

        if db is None:
            return 0

        since = (
            datetime.utcnow()
            - timedelta(minutes=60)
        )

        return (
            db.query(Report)
            .filter(
                Report.zone.ilike(zone_id),
                Report.created_at >= since
            )
            .count()
        )

    # ==========================================
    # BLOCKED ROAD COUNT
    # ==========================================

    def _blocked_report_count(
        self,
        db: Session | None,
        zone_id: str
    ):

        if db is None:
            return 0

        since = (
            datetime.utcnow()
            - timedelta(minutes=60)
        )

        return (
            db.query(Report)
            .filter(
                Report.zone.ilike(zone_id),
                Report.created_at >= since,
                Report.road_blocked.is_(True)
            )
            .count()
        )


prediction_service = PredictionService()