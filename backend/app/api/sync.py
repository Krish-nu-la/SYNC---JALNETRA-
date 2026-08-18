from fastapi import APIRouter, HTTPException

from app.services.sync_service import sync_service

router = APIRouter(
    prefix="/sync",
    tags=["Sync"]
)


@router.get("/latest")
def get_latest_snapshot():

    return sync_service.get_latest()


@router.post("/refresh")
def refresh_snapshot():

    try:

        return sync_service.refresh(
            sync_type="manual"
        )

    except TimeoutError as exc:

        raise HTTPException(
            status_code=504,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Sync failed: {exc}"
        )


@router.post("/emergency")
def emergency_refresh():

    try:

        return sync_service.refresh(
            sync_type="emergency"
        )

    except TimeoutError as exc:

        raise HTTPException(
            status_code=504,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Emergency sync failed: {exc}"
        )