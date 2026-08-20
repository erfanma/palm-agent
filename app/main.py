from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, auth, readings
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title="Palmistry AI Agent & Services API",
    description="Unified API combining visual AI palmistry analysis, user authentication, profile sync, and wizard reading persistence.",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin client integration (Flutter mobile, web, desktop, emulator)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on server startup
@app.on_event("startup")
def startup_event():
    init_db()

# Mount all service routers
app.include_router(analyze.router)
app.include_router(auth.router)
app.include_router(readings.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint confirming API status and model configuration."""
    return {
        "status": "healthy",
        "service": "Palmistry AI Agent & Services",
        "model_provider": settings.MODEL_PROVIDER,
        "configured_model": settings.GEMINI_MODEL if settings.MODEL_PROVIDER == "google" else settings.OPENAI_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
