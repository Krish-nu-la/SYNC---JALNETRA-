Write-Host "====================================="
Write-Host "   JalNetra Backend Foundation"
Write-Host "====================================="

# -----------------------
# Create Folder Structure
# -----------------------

$folders = @(
"app",
"app/api",
"app/core",
"app/database",
"app/models",
"app/schemas",
"app/services",
"app/utils"
)

foreach ($folder in $folders){
    if(!(Test-Path $folder)){
        New-Item -ItemType Directory -Path $folder | Out-Null
    }
}

# -----------------------
# Create __init__.py
# -----------------------

$initFiles = @(
"app/__init__.py",
"app/api/__init__.py",
"app/core/__init__.py",
"app/database/__init__.py",
"app/models/__init__.py",
"app/schemas/__init__.py",
"app/services/__init__.py",
"app/utils/__init__.py"
)

foreach($file in $initFiles){
    if(!(Test-Path $file)){
        New-Item -ItemType File -Path $file | Out-Null
    }
}

# -----------------------
# Create Config
# -----------------------

@'
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME","JalNetra Backend")
VERSION = os.getenv("VERSION","1.0.0")
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./jalnetra.db")
WEATHER_API = os.getenv("WEATHER_API","https://api.open-meteo.com/v1/forecast")
'@ | Set-Content app/core/config.py

# -----------------------
# Database
# -----------------------

@'
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
'@ | Set-Content app/database/database.py

# -----------------------
# Main
# -----------------------

@'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, VERSION

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="AI Flood Decision Support Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "project":"JalNetra",
        "status":"Running",
        "version":VERSION
    }

@app.get("/health")
async def health():
    return {
        "status":"Healthy"
    }
'@ | Set-Content app/main.py

# -----------------------
# Environment
# -----------------------

@'
APP_NAME=JalNetra Backend
VERSION=1.0.0
DATABASE_URL=sqlite:///./jalnetra.db
WEATHER_API=https://api.open-meteo.com/v1/forecast
'@ | Set-Content .env

# -----------------------
# Git Ignore
# -----------------------

@'
.venv/
__pycache__/
*.pyc
*.db
.env
'@ | Set-Content .gitignore

Write-Host ""
Write-Host "Foundation Created Successfully!"
Write-Host ""
Write-Host "Run:"
Write-Host "python -m uvicorn app.main:app --reload"