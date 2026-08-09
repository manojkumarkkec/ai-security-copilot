import time
import uuid

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger



class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):


    async def dispatch(

        self,

        request: Request,

        call_next,

    ) -> Response:


        request_id = str(
            uuid.uuid4()
        )


        start_time = time.perf_counter()



        # Attach request id
        request.state.request_id = request_id



        logger.info(

            "Incoming request",

            extra={

                "event": "API_REQUEST_STARTED",

                "context": {

                    "request_id": request_id,

                    "method": request.method,

                    "path": request.url.path,

                    "client_ip": (

                        request.client.host

                        if request.client

                        else None

                    ),

                },

            },

        )



        try:


            response = await call_next(
                request
            )



            duration_ms = (

                time.perf_counter()

                - start_time

            ) * 1000



            logger.info(

                "Request completed",

                extra={

                    "event": "API_REQUEST_COMPLETED",

                    "context": {

                        "request_id": request_id,

                        "method": request.method,

                        "path": request.url.path,

                        "status_code": response.status_code,

                        "duration_ms": round(

                            duration_ms,

                            2,

                        ),

                    },

                },

            )



            response.headers[

                "X-Request-ID"

            ] = request_id



            return response



        except Exception as exc:


            duration_ms = (

                time.perf_counter()

                - start_time

            ) * 1000



            logger.exception(

                "Request failed",

                extra={

                    "event": "API_REQUEST_FAILED",

                    "context": {

                        "request_id": request_id,

                        "method": request.method,

                        "path": request.url.path,

                        "duration_ms": round(

                            duration_ms,

                            2,

                        ),

                        "error": str(exc),

                    },

                },

            )


            raise