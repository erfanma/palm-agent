from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze
from app.core.config import settings

app = FastAPI(
    title="Palmistry AI Agent API",
    description="LangChain-powered multi-modal AI service for visual hand and palmistry analysis.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin web client integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include palmistry router
app.include_router(analyze.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint confirming API status and model configuration."""
    return {
        "status": "healthy",
        "service": "Palmistry AI Agent",
        "model_provider": settings.MODEL_PROVIDER,
        "configured_model": settings.GEMINI_MODEL if settings.MODEL_PROVIDER == "google" else settings.OPENAI_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
