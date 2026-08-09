from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.core.events import SecurityEvent

from app.models.enums import ScanStatus

from app.parsers.csv_parser import CSVParser
from app.parsers.json_parser import JSONParser

from app.scanners.detector import ScannerDetector

from app.normalizers.factory import NormalizerFactory

from app.services.vulnerability_service import (
    VulnerabilityService,
)

from app.services.scan_upload_service import (
    ScanUploadService,
)

from app.services.audit_service import (
    AuditService,
)



class ScanIngestionService:


    def __init__(self):

        self.vulnerability_service = VulnerabilityService()

        self.scan_service = ScanUploadService()

        self.scanner_detector = ScannerDetector()

        self.audit_service = AuditService()



    async def process_scan(

        self,

        session: AsyncSession,

        scan_id: UUID,

        filename: str,

        content: bytes,

        uploaded_by: str,

    ) -> dict:


        logger.info(

            "Scan processing started",

            extra={

                "event": SecurityEvent.SCAN_UPLOAD_STARTED.value,

                "context": {

                    "scan_id": str(scan_id),

                    "filename": filename,

                },

            },

        )


        scan_upload = await self.scan_service.get_scan(

            session=session,

            scan_id=scan_id,

        )


        if scan_upload is None:

            raise ValueError(
                "Scan upload record not found."
            )



        try:


            # -----------------------------
            # Select Parser
            # -----------------------------

            if filename.lower().endswith(".csv"):

                parser = CSVParser()


            elif filename.lower().endswith(".json"):

                parser = JSONParser()


            else:

                raise ValueError(
                    "Unsupported file format."
                )



            # -----------------------------
            # Parse
            # -----------------------------

            raw_data = parser.parse(
                content
            )


            if not raw_data:

                raise ValueError(
                    "No records found."
                )



            # -----------------------------
            # Detect Scanner
            # -----------------------------

            scanner = self.scanner_detector.detect(

                raw_data

            )


            scan_upload.scanner = scanner



            # -----------------------------
            # Normalize
            # -----------------------------

            normalizer = NormalizerFactory.get_normalizer(

                scanner

            )


            vulnerabilities = [

                normalizer.normalize(item)

                for item in raw_data

            ]



            # -----------------------------
            # Import vulnerabilities
            # -----------------------------

            result = await self.vulnerability_service.bulk_import(

                session=session,

                vulnerabilities=vulnerabilities,

            )



            # -----------------------------
            # Complete Scan
            # -----------------------------

            await self.scan_service.complete_scan_upload(

                session=session,

                scan_upload=scan_upload,

                total_records=result["total_records"],

                inserted_records=result["inserted_records"],

                duplicate_records=result["duplicate_records"],

                failed_records=result["failed_records"],

            )



            # -----------------------------
            # Audit Success
            # -----------------------------

            await self.audit_service.log(

                session=session,

                user=uploaded_by,

                event=SecurityEvent.SCAN_PROCESS_COMPLETED,

                resource=str(scan_id),

                details={

                    "filename": filename,

                    "scanner": scanner,

                    "records": result,

                },

            )



            logger.info(

                "Scan processing completed",

                extra={

                    "event": SecurityEvent.SCAN_PROCESS_COMPLETED.value,

                    "context": {

                        "scan_id": str(scan_id),

                    },

                },

            )



            return {


                "scan_id": scan_id,


                "scanner": scanner,


                "records_processed": result,


                "status": ScanStatus.COMPLETED,


            }



        except Exception as exc:


            logger.exception(

                "Scan processing failed",

                extra={

                    "event": SecurityEvent.SCAN_PROCESS_FAILED.value,

                    "context": {

                        "scan_id": str(scan_id),

                        "error": str(exc),

                    },

                },

            )


            await self.scan_service.fail_scan_upload(

                session=session,

                scan_upload=scan_upload,

            )



            await self.audit_service.log(

                session=session,

                user=uploaded_by,

                event=SecurityEvent.SCAN_PROCESS_FAILED,

                resource=str(scan_id),

                details={

                    "filename": filename,

                    "error": str(exc),

                },

            )


            raise