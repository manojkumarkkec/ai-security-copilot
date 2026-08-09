from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Duration, Limiter, Rate

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.core.dependencies import (
    get_scan_upload_service,
    get_vulnerability_service,
)

from app.core.permissions import require_roles

from app.models.user import User
from app.models.enums import (
    UserRole,
    VulnerabilitySeverity,
    VulnerabilityStatus,
)

from app.schemas.update_status_request import (
    UpdateStatusRequest,
)

from app.schemas.vulnerability_schema import (
    VulnerabilityResponse,
)

from app.services.scan_upload_service import (
    ScanUploadService,
)

from app.services.vulnerability_service import (
    VulnerabilityService,
)

from app.workers.scan_worker import (
    ScanWorker,
)


router = APIRouter(
    prefix="/vulnerabilities",
    tags=["Vulnerabilities"],
)


MAX_FILE_SIZE = 10 * 1024 * 1024


# =====================================================
# Rate Limiting
# =====================================================

upload_limiter = Limiter(
    Rate(
        10,
        Duration.MINUTE,
    )
)


# =====================================================
# 1. Upload Scan
# =====================================================

@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[
        Depends(
            RateLimiter(
                limiter=upload_limiter,
            )
        )
    ],
)
async def upload_scan(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    scan_service: ScanUploadService = Depends(
        get_scan_upload_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    filename = file.filename.lower()

    if not filename.endswith(
        (
            ".csv",
            ".json",
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and JSON files are supported.",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum file size is 10 MB.",
        )

    scan_upload = await scan_service.create_scan_upload(
        session=db,
        filename=file.filename,
        scanner="UNKNOWN",
        uploaded_by=current_user.username,
    )

    await db.commit()

    await db.refresh(
        scan_upload
    )

    worker = ScanWorker()

    background_tasks.add_task(
        worker.process_scan,
        scan_upload.id,
        file.filename,
        content,
        current_user.username,
    )

    return {
        "message": "Scan accepted.",
        "scan_id": scan_upload.id,
        "status": scan_upload.status,
        "filename": scan_upload.filename,
    }


# =====================================================
# 2. Get Scan Status
# =====================================================

@router.get(
    "/scans/{scan_id}",
)
async def get_scan_status(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    scan_service: ScanUploadService = Depends(
        get_scan_upload_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    scan = await scan_service.get_scan(
        session=db,
        scan_id=scan_id,
    )

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found.",
        )

    return {
        "scan_id": scan.id,
        "filename": scan.filename,
        "scanner": scan.scanner,
        "status": scan.status,
        "uploaded_by": scan.uploaded_by,
        "total_records": scan.total_records,
        "inserted_records": scan.inserted_records,
        "duplicate_records": scan.duplicate_records,
        "failed_records": scan.failed_records,
        "created_at": scan.uploaded_at,
    }


# =====================================================
# 3. Scan History
# =====================================================

@router.get(
    "/scans",
)
async def get_scan_history(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
    scan_service: ScanUploadService = Depends(
        get_scan_upload_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must start from 1.",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be greater than 0.",
        )

    if page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum page size is 100.",
        )

    return await scan_service.get_scan_history(
        session=db,
        page=page,
        page_size=page_size,
    )


# =====================================================
# 4. Vulnerability Listing
# =====================================================

@router.get(
    "",
)
async def get_vulnerabilities(
    page: int = 1,
    page_size: int = 20,
    severity: VulnerabilitySeverity | None = None,
    vulnerability_status: VulnerabilityStatus | None = None,
    db: AsyncSession = Depends(get_db),
    service: VulnerabilityService = Depends(
        get_vulnerability_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must start from 1.",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be greater than 0.",
        )

    if page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum page size is 100.",
        )

    result = await service.get_paginated(
        session=db,
        page=page,
        page_size=page_size,
        severity=severity,
        status=vulnerability_status,
    )

    return {
        "page": result["page"],
        "page_size": result["page_size"],
        "total": result["total"],
        "vulnerabilities": [
            VulnerabilityResponse.model_validate(item)
            for item in result["vulnerabilities"]
        ],
    }


# =====================================================
# 5. Vulnerability Detail
# =====================================================

@router.get(
    "/{vulnerability_id}",
)
async def get_vulnerability(
    vulnerability_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: VulnerabilityService = Depends(
        get_vulnerability_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    vulnerability = await service.get_by_id(
        session=db,
        vulnerability_id=vulnerability_id,
    )

    if vulnerability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability not found.",
        )

    return VulnerabilityResponse.model_validate(
        vulnerability
    )


# =====================================================
# 6. Update Vulnerability Status
# =====================================================

@router.patch(
    "/{vulnerability_id}/status",
)
async def update_status(
    vulnerability_id: UUID,
    request: UpdateStatusRequest,
    db: AsyncSession = Depends(get_db),
    service: VulnerabilityService = Depends(
        get_vulnerability_service,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SECURITY_ENGINEER,
        )
    ),
):
    vulnerability = await service.update_status(
        session=db,
        vulnerability_id=vulnerability_id,
        status=request.status,
    )

    if vulnerability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability not found.",
        )

    return {
        "message": "Status updated successfully.",
        "vulnerability_id": vulnerability.id,
        "status": vulnerability.status,
    }