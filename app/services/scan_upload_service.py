from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.scan_upload import ScanUpload
from app.models.enums import ScanStatus

from app.repositories.scan_upload_repository import (
    ScanUploadRepository,
)


class ScanUploadService:

    def __init__(self):

        self.repository = ScanUploadRepository()

    async def create_scan_upload(
        self,
        session: AsyncSession,
        filename: str,
        scanner: str,
        uploaded_by: str,
    ) -> ScanUpload:

        scan_upload = ScanUpload(
            filename=filename,
            scanner=scanner,
            uploaded_by=uploaded_by,
            status=ScanStatus.PENDING,
        )

        return await self.repository.create(
            session,
            scan_upload,
        )

    async def get_scan(
        self,
        session: AsyncSession,
        scan_id: UUID,
    ) -> ScanUpload | None:

        return await self.repository.get_by_id(
            session,
            scan_id,
        )

    async def mark_processing(
        self,
        session: AsyncSession,
        scan_upload: ScanUpload,
    ) -> ScanUpload:

        scan_upload.status = ScanStatus.PROCESSING

        return await self.repository.update(
            session,
            scan_upload,
        )

    async def complete_scan_upload(
        self,
        session: AsyncSession,
        scan_upload: ScanUpload,
        total_records: int,
        inserted_records: int,
        duplicate_records: int,
        failed_records: int = 0,
    ) -> ScanUpload:

        scan_upload.status = ScanStatus.COMPLETED

        scan_upload.total_records = total_records
        scan_upload.inserted_records = inserted_records
        scan_upload.duplicate_records = duplicate_records
        scan_upload.failed_records = failed_records

        return await self.repository.update(
            session,
            scan_upload,
        )

    async def fail_scan_upload(
        self,
        session: AsyncSession,
        scan_upload: ScanUpload,
        error_message: str | None = None,
    ) -> ScanUpload:

        scan_upload.status = ScanStatus.FAILED

        if error_message:
            scan_upload.error_message = error_message

        return await self.repository.update(
            session,
            scan_upload,
        )

    async def get_scan_history(
        self,
        session: AsyncSession,
        page: int,
        page_size: int,
    ) -> dict:


        offset = (
            page - 1
        ) * page_size


        scans = await self.repository.get_all_paginated(
            session,
            offset,
            page_size,
        )


        total = await self.repository.count(
            session
        )


        return {

            "page": page,

            "page_size": page_size,

            "total": total,

            "scans": scans,

        }