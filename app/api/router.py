from fastapi import APIRouter

from app.api.ask import router as ask_router
from app.api.documents import router as documents_router


API_PREFIX = "/api/v1"

router = APIRouter(prefix=API_PREFIX)
router.include_router(documents_router)
router.include_router(ask_router)
