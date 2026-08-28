# API Router Aggregator
from fastapi import APIRouter
from backend.api.chat import router as chat_router
from backend.api.standards import router as standards_router
from backend.api.compliance import router as compliance_router
from backend.api.sources import router as sources_router
from backend.api.history import router as history_router
from backend.api.feedback import router as feedback_router
from backend.api.ingestion_api import router as ingestion_router

api_router = APIRouter()
api_router.include_router(chat_router)
api_router.include_router(standards_router)
api_router.include_router(compliance_router)
api_router.include_router(sources_router)
api_router.include_router(history_router)
api_router.include_router(feedback_router)
api_router.include_router(ingestion_router)

__all__ = ["api_router"]
