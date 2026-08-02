from app.services.weather_service import weather_service

print(

    weather_service.get_weather(

        rainfall_override=60

    )

)