import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.database.session import init_db, SessionLocal
from backend.knowledge.seed_data import seed_database
from backend.ingestion.indexer import QdrantIndexer
from backend.api import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bis_assistant")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("Initializing ManakSetu Backend...")
    # Initialize DB schema
    init_db()

    # Seed data and index chunks
    db = SessionLocal()
    try:
        seed_database(db)
        indexer = QdrantIndexer()
        indexer.sync_database_chunks_to_qdrant()
        logger.info("Startup initialization complete.")
    except Exception as e:
        logger.error(f"Startup initialization error: {e}")
    finally:
        db.close()

    yield
    logger.info("Shutting down ManakSetu Backend...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Intelligent Assistant for Indian Standards & BIS Services (SIH26107)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."},
    )


@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "demo_mode": settings.DEMO_MODE,
        "llm_provider": settings.LLM_PROVIDER,
    }


# Mount all routers
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
