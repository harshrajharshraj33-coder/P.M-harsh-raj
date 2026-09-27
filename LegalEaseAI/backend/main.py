from fastapi import FastAPI
app = FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    description=(
        "LegalEase - "
        "AI-powered legal document draft generator"
    ),

    version="1.0.0",
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "message": "LegalEase API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {

        "status": "ok",

        "demo_mode": settings.demo_mode,

        "model": settings.gemini_model
    }


app.include_router(router)