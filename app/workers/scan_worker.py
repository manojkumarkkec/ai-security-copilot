from uuid import UUID

from app.database.session import (
    AsyncSessionLocal,
)

from app.services.scan_ingestion_service import (
    ScanIngestionService,
)

from app.core.logging import logger

from app.core.events import SecurityEvent

class ScanWorker:


    def __init__(self):

        self.service = ScanIngestionService()



    async def process_scan(

        self,

        scan_id: UUID,

        filename: str,

        content: bytes,

        uploaded_by: str,

    ):


        async with AsyncSessionLocal() as session:


            try:


                logger.info(

                    "Background scan started | scan_id=%s",

                    scan_id,

                )


                await self.service.process_scan(

                    session=session,

                    scan_id=scan_id,

                    filename=filename,

                    content=content,

                    uploaded_by=uploaded_by,

                )



                await session.commit()



                logger.info(

                    "Background scan completed",

                    extra={

                        "event": SecurityEvent.SCAN_PROCESS_COMPLETED.value,

                        "context": {

                            "scan_id": str(scan_id),

                        }

                    }

                )



            except Exception as exc:


                await session.rollback()


                logger.exception(

                    "Background scan failed",

                    extra={

                        "event": SecurityEvent.SCAN_PROCESS_FAILED.value,

                        "context": {

                            "scan_id": str(scan_id),

                        }

                    }

                )


                raise exc