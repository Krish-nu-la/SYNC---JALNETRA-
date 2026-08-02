from fastapi import APIRouter

from app.services.prediction_service import prediction_service
from app.services.explanation_service import explanation_service

router = APIRouter()


@router.get("/explain")
def explain(zone: str, rain: float, offset: int):

    prediction = prediction_service.predict(
        rainfall=rain,
        offset=offset
    )

    for z in prediction["zones"]:

        if z["id"] == zone:

            return explanation_service.explain(
                zone,
                z["depthCm"]
            )

    return {
        "error": "Zone not found"
    }