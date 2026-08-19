from pathlib import Path

import pandas as pd


class ClimatologyService:
    """Historical rainfall climatology for the Ernakulam/Kochi region."""

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "raw"
            / "Indian Rainfall Dataset District-wise Daily Measurements.csv"
            / "Indian Rainfall Dataset District-wise Daily Measurements.csv"
        )

        self._data = None

    def _load(self):
        if self._data is None:
            df = pd.read_csv(self.data_path, sep=";")

            ernakulam = df[
                df["district"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("ernakulam")
            ].copy()

            if ernakulam.empty:
                raise ValueError("Ernakulam climatology data not found.")

            day_columns = [
                column
                for column in ernakulam.columns
                if str(column).endswith(("st", "nd", "rd", "th"))
            ]

            ernakulam["monthly_total_mm"] = ernakulam[day_columns].sum(axis=1)
            ernakulam["max_daily_mm"] = ernakulam[day_columns].max(axis=1)
            ernakulam["rainy_days"] = (
                ernakulam[day_columns] > 0
            ).sum(axis=1)

            self._data = ernakulam

        return self._data

    def get_month(self, month: int):
        if not 1 <= month <= 12:
            raise ValueError("month must be between 1 and 12")

        df = self._load()

        row = df[df["month"] == month]

        if row.empty:
            raise ValueError(f"No climatology data for month {month}.")

        row = row.iloc[0]

        return {
            "month": int(month),
            "monthly_total_mm": round(
                float(row["monthly_total_mm"]),
                2,
            ),
            "max_daily_mm": round(
                float(row["max_daily_mm"]),
                2,
            ),
            "rainy_days": int(row["rainy_days"]),
            "source": "historical-ernakulam-climatology",
        }

    def get_annual_total(self):
        df = self._load()

        return round(
            float(df["monthly_total_mm"].sum()),
            2,
        )


climatology_service = ClimatologyService()