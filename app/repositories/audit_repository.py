from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog



class AuditRepository:


    async def create(

        self,

        session: AsyncSession,

        audit: AuditLog,

    ):


        session.add(
            audit
        )


        await session.flush()


        return audit