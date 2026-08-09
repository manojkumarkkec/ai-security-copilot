from app.services.audit_service import AuditService
from app.services.scan_ingestion_service import ScanIngestionService
from app.services.scan_upload_service import ScanUploadService
from app.services.vulnerability_service import VulnerabilityService


def get_vulnerability_service() -> VulnerabilityService:

    return VulnerabilityService()


def get_scan_upload_service() -> ScanUploadService:

    return ScanUploadService()


def get_scan_ingestion_service() -> ScanIngestionService:

    return ScanIngestionService()


def get_audit_service() -> AuditService:

    return AuditService()