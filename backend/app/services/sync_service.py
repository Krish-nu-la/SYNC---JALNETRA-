import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.services.weather_service import weather_service
from app.ml.feature_builder import feature_builder
from app.ml.model_loader import model_loader


class SyncService:
    """
    Builds and stores the latest 2-hour JalNetra forecast package.

    Normal forecast frames:
        0, 30, 60, 90, 120 minutes

    The saved snapshot allows the application to continue
    operating when the network is unavailable.
    """

    OFFSETS = [0, 30, 60, 90, 120]

    SYNC_INTERVAL_MINUTES = 30
    SNAPSHOT_MAX_AGE_SECONDS = 7200
    SYNC_TIMEOUT_SECONDS = 60

    SNAPSHOT_PATH = Path(
        "data/latest_snapshot.json"
    )

    def __init__(self):
        self.SNAPSHOT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        model_loader.load()

    def refresh(
        self,
        rainfall_override=None,
        sync_type="scheduled"
    ):
        """
        Generate a complete 2-hour forecast package
        and save it atomically.
        """

        started = time.perf_counter()

        forecasts = []

        for offset in self.OFFSETS:

            # Fetch the weather frame using the existing
            # WeatherService/Open-Meteo pipeline.
            weather = weather_service.get_weather(
                rainfall_override=(
                    rainfall_override
                    if offset == 0
                    else None
                ),
                offset=offset
            )

            # Build model features using the already
            # fetched weather frame.
            df = feature_builder.build(
                rainfall=weather["rainfall_mm"],
                offset=offset,
                weather_override=weather
            )

            zones = df["zone"]

            X = df.drop(
                columns=["zone"]
            )

            X = X[
                model_loader.features
            ]

            predictions = model_loader.model.predict(
                X
            )

            zone_results = []

            for zone, depth in zip(
                zones,
                predictions
            ):

                zone_results.append({
                    "id": zone["id"],
                    "name": zone["name"],
                    "lat": zone["lat"],
                    "lng": zone["lng"],
                    "depthCm": round(
                        float(depth),
                        2
                    ),
                    "population": zone["population"],
                })

            forecasts.append({
                "offsetMin": offset,

                "weather": weather,

                "zones": zone_results,
            })

            # Never allow the sync operation to run
            # indefinitely.
            elapsed = (
                time.perf_counter()
                - started
            )

            if elapsed > self.SYNC_TIMEOUT_SECONDS:
                raise TimeoutError(
                    "Forecast synchronization exceeded 60 seconds."
                )

        now = datetime.now(
            timezone.utc
        )

        snapshot = {

            "status": "live",

            "syncType": sync_type,

            "generatedAt":
                now.isoformat(),

            "nextSyncAt": (
                now
                + timedelta(
                    minutes=self.SYNC_INTERVAL_MINUTES
                )
            ).isoformat(),

            "expiresAt": (
                now
                + timedelta(hours=2)
            ).isoformat(),

            "processingTimeMs": round(
                (
                    time.perf_counter()
                    - started
                ) * 1000,
                2
            ),

            "forecasts": forecasts,
        }

        self._save_snapshot(
            snapshot
        )

        return snapshot

    def _save_snapshot(
        self,
        snapshot
    ):
        """
        Atomic write.

        The old snapshot remains intact if writing
        the new snapshot fails.
        """

        temporary_path = (
            self.SNAPSHOT_PATH.with_suffix(
                ".tmp"
            )
        )

        with open(
            temporary_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                snapshot,
                file,
                indent=2
            )

        temporary_path.replace(
            self.SNAPSHOT_PATH
        )

    def get_latest(self):
        """
        Return the latest locally stored forecast.

        This function does NOT require internet access.
        """

        if not self.SNAPSHOT_PATH.exists():

            return {
                "status": "unavailable",
                "message":
                    "No forecast snapshot available."
            }

        try:

            with open(
                self.SNAPSHOT_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                snapshot = json.load(
                    file
                )

            generated = datetime.fromisoformat(
                snapshot["generatedAt"]
            )

            now = datetime.now(
                timezone.utc
            )

            age_seconds = (
                now - generated
            ).total_seconds()

            snapshot[
                "dataAgeSeconds"
            ] = round(
                max(age_seconds, 0),
                2
            )

            if age_seconds > self.SNAPSHOT_MAX_AGE_SECONDS:

                snapshot["status"] = "stale"

            else:

                snapshot["status"] = "offline"

            return snapshot

        except (
            OSError,
            ValueError,
            KeyError,
            json.JSONDecodeError
        ):

            return {
                "status": "unavailable",
                "message":
                    "Stored forecast snapshot is invalid."
            }


sync_service = SyncService()