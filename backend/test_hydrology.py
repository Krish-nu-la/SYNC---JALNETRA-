from app.services.zone_service import ZoneService
from app.services.weather_service import weather_service
from app.services.hydrology_service import hydrology_service

zone = ZoneService().get_zone("kaloor")

weather = weather_service.get_weather(60)

result = hydrology_service.calculate(

    rainfall=60,

    zone=zone,

    weather=weather

)

print(result)