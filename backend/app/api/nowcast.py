from fastapi import APIRouter, HTTPException

from app.services.prediction_service import prediction_service

router = APIRouter()


@router.get("/nowcast")
def get_nowcast(rain: float, offset: int):

    if rain < 0 or rain > 120:
        raise HTTPException(
            status_code=400,
            detail="Rainfall must be between 0 and 120 mm/hr"
        )

    if offset not in [0, 30, 60, 90, 120]:
        raise HTTPException(
            status_code=400,
            detail="Offset must be 0,30,60,90 or 120"
        )

    return prediction_service.predict(
        rainfall=rain,
        offset=offset
    )