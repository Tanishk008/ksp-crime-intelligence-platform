from fastapi import APIRouter
from .cases import router as cases_router
from .entities import router as entities_router
from .conversations import router as conversations_router
from .map import router as map_router
from .alerts import router as alerts_router
from .reports import router as reports_router
from .admin import router as admin_router
from .auth import router as auth_router
from .search import router as search_router
from .network import router as network_router
from .voice import router as voice_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(cases_router)
api_router.include_router(entities_router)
api_router.include_router(conversations_router)
api_router.include_router(map_router)
api_router.include_router(alerts_router)
api_router.include_router(reports_router)
api_router.include_router(admin_router)
api_router.include_router(search_router)
api_router.include_router(network_router)
api_router.include_router(voice_router)


