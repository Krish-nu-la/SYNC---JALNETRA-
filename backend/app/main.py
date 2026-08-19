from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.api.alerts import router as alerts_router
from app.api.analytics import router as analytics_router
from app.api.climatology import router as climatology_router
from app.api.dashboard import router as dashboard_router
from app.api.explain import router as explain_router
from app.api.forecast import router as forecast_router
from app.api.health import router as health_router
from app.api.nowcast import router as nowcast_router
from app.api.reports import router as reports_router
from app.api.sync import router as sync_router

from app.database.database import Base, engine
from app.ml.model_loader import model_loader
from app.services.sync_service import sync_service


scheduler = AsyncIOScheduler()


def scheduled_sync():
    try:
        result = sync_service.refresh(
            sync_type="scheduled"
        )

        print(
            f"Scheduled sync completed: "
            f"{result['processingTimeMs']} ms"
        )

    except Exception as exc:
        print(
            f"Scheduled sync failed: {exc}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading AI Model...")

    model_loader.load()

    Base.metadata.create_all(
        bind=engine
    )

    print("AI Model Loaded Successfully.")

    scheduled_sync()

    scheduler.add_job(
        scheduled_sync,
        "interval",
        minutes=30,
        id="jalnetra_weather_sync",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print(
        "JalNetra automatic sync started "
        "(every 30 minutes)."
    )

    yield

    if scheduler.running:
        scheduler.shutdown(
            wait=False
        )

    print(
        "JalNetra API Shutting Down..."
    )


app = FastAPI(
    title="JalNetra API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to JalNetra",
        "docs": "/docs",
    }


app.include_router(health_router)
app.include_router(nowcast_router)
app.include_router(forecast_router)
app.include_router(dashboard_router)
app.include_router(alerts_router)
app.include_router(analytics_router)
app.include_router(explain_router)
app.include_router(reports_router)
app.include_router(climatology_router)
app.include_router(sync_router)
