from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth_endpoint import router as auth_router
from app.api.v1.users_endpoint import router as users_router

from app.api.v1.vulnerabilities_endpoint import (
    router as vulnerabilities_router,
)

from app.api.v1.chat_endpoint import (
    router as chat_router,
)

from app.api.v1.document_endpoint import (
    router as document_router,
)

from app.api.v1.evaluation_endpoint import (
    router as evaluation_router,
)


api_router = APIRouter()


api_router.include_router(
    health_router,
    tags=["Health"],
)


api_router.include_router(
    auth_router,
)


api_router.include_router(
    users_router,
)


api_router.include_router(
    vulnerabilities_router,
)


api_router.include_router(
    chat_router,
)


api_router.include_router(
    document_router,
)


api_router.include_router(
    evaluation_router,
)