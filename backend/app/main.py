from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.nowcast import router as nowcast_router
from app.api.health import router as health_router
from app.api.reports import router as reports_router
from app.ml.model_loader import model_loader
from app.api.forecast import router as forecast_router
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.analytics import router as analytics_router
from app.api.explain import router as explain_router
from app.database.database import Base
from app.database.database import engine



@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading AI Model...")

    model_loader.load()

    Base.metadata.create_all(bind=engine)

    print("AI Model Loaded Successfully.")

    yield

    print("JalNetra API Shutting Down...")


app = FastAPI(

    title="JalNetra API",

    version="1.0.0",

    lifespan=lifespan

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

app.include_router(nowcast_router)
app.include_router(health_router)


@app.get("/")
def root():

    return {

        "message": "Welcome to JalNetra",

        "docs": "/docs"

    }

app.include_router(forecast_router)

app.include_router(dashboard_router)

app.include_router(alerts_router)

app.include_router(analytics_router)

app.include_router(explain_router)

app.include_router(reports_router)