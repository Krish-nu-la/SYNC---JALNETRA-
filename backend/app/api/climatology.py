from fastapi import APIRouter, HTTPException

from app.services.climatology_service import climatology_service


router = APIRouter(
    prefix="/climatology",
    tags=["climatology"],
)


@router.get("/ernakulam")
def get_ernakulam_climatology(month: int | None = None):
    try:
        if month is not None:
            return climatology_service.get_month(month)

        return {
            "annual_total_mm": climatology_service.get_annual_total(),
            "source": "historical-ernakulam-climatology",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )