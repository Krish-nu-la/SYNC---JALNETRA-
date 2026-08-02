import pandas as pd

from app.core.config import settings


class ZoneService:

    def __init__(self):

        self.df = pd.read_csv(settings.ZONES_PATH)

    def get_all_zones(self):

        return self.df.to_dict(
            orient="records"
        )

    def get_zone(self, zone_id):

        zone = self.df[
            self.df["id"] == zone_id
        ]

        if zone.empty:

            return None

        return zone.iloc[0].to_dict()