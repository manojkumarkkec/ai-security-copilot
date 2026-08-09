from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.redis import redis_client
from app.core.langsmith import setup_langsmith

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    global_exception_handler,
)
from app.middleware.requestid_middleware import (
    RequestLoggingMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services
    yield
    # Cleanup
    await redis_client.close()


def create_application() -> FastAPI:

    setup_langsmith()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        lifespan=lifespan,
        description="AI powered vulnerability analysis assistant",
    )

    app.add_middleware(
            RequestLoggingMiddleware,
    )

    # Register global exception handlers
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        global_exception_handler,
    )

    # Register API routes
    app.include_router(
        api_router,
        prefix="/api/v1",
    )

    

    return app


app = create_application()
