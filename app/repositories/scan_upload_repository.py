from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from app.models.scan_upload import ScanUpload


class ScanUploadRepository:


    async def create(
        self,
        session: AsyncSession,
        scan_upload: ScanUpload,
    ) -> ScanUpload:

        session.add(scan_upload)
        await session.flush()

        await session.refresh(scan_upload)

        return scan_upload


    async def update(
        self,
        session: AsyncSession,
        scan_upload: ScanUpload,
    ) -> ScanUpload:

        await session.commit()

        await session.refresh(scan_upload)

        return scan_upload

    async def get_by_id(
        self,
        session: AsyncSession,
        scan_id: UUID,
    ) -> ScanUpload | None:

        return await session.get(
        ScanUpload,
        scan_id,
        )

    async def get_all_paginated(
        self,
        session: AsyncSession,
        offset: int,
        limit: int,
    ) -> list[ScanUpload]:


        query = (
            select(ScanUpload)
            .offset(offset)
            .limit(limit)
            .order_by(
                ScanUpload.uploaded_at.desc()
            )
        )


        result = await session.execute(
            query
        )


        return list(
            result.scalars().all()
        )



    async def count(
        self,
        session: AsyncSession,
    ) -> int:


        query = select(
            func.count()
        ).select_from(
            ScanUpload
        )


        result = await session.execute(
            query
        )


        return result.scalar_one()