from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog

from app.repositories.audit_repository import (
    AuditRepository,
)



class AuditService:


    def __init__(self):

        self.repository = AuditRepository()



    async def log(

        self,

        session: AsyncSession,

        user: str,

        event,

        resource: str,

        details: dict

    ):


        audit = AuditLog(

            user=user,

            event=event,

            resource=resource,

            details=details,

        )


        session.add(
            audit
        )


        await session.flush()


        await session.refresh(
            audit
        )


        return audit