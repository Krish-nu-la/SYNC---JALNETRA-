class TrendService:

    def calculate(
        self,
        previous_depth,
        current_depth
    ):

        diff = current_depth - previous_depth

        if diff > 2:

            return "rising"

        elif diff < -2:

            return "falling"

        return "steady"


trend_service = TrendService()