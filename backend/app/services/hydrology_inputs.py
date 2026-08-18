from dataclasses import dataclass


@dataclass
class HydrologyInputs:
    """
    Hydrological inputs consumed by the flood prediction pipeline.

    Current implementation uses rainfall-derived proxies.
    These are deliberately marked as estimated so they can later
    be replaced by real gauge/river observations.
    """

    river_discharge_m3_s: float
    water_level_m: float
    historical_floods: float
    infrastructure: float
    source: str


class HydrologyInputService:

    def from_scenario(self, rainfall_mm: float) -> HydrologyInputs:
        rainfall_mm = max(0.0, float(rainfall_mm))

        return HydrologyInputs(
            river_discharge_m3_s=rainfall_mm * 2.0,
            water_level_m=rainfall_mm / 100.0,
            historical_floods=4.0,
            infrastructure=7.0,
            source="scenario-proxy",
        )


hydrology_input_service = HydrologyInputService()