from app.services.weather_service import weather_service
from app.services.prediction_service import prediction_service
from app.services.dashboard_service import dashboard_service
from app.services.analytics_service import analytics_service
from app.services.alert_service import alert_service


class PredictionController:

    def nowcast(self, rainfall, offset):

        return prediction_service.predict(
            rainfall,
            offset
        )

    def dashboard(self, rainfall):

        return dashboard_service.build(
            rainfall
        )

    def analytics(self, rainfall):

        return analytics_service.generate(
            rainfall
        )

    def alerts(self, rainfall):

        return alert_service.generate(
            rainfall
        )


prediction_controller = PredictionController()