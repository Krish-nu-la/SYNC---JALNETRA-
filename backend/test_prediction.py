from app.services.prediction_service import prediction_service

result = prediction_service.predict(

    rainfall=60,

    offset=60

)

print(result)