from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "loaded",
        "version": "1.0.0"
    }