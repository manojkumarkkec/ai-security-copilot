import uuid

from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base



class AuditLog(Base):

    __tablename__ = "audit_logs"


    id: Mapped[uuid.UUID] = mapped_column(

        primary_key=True,

        default=uuid.uuid4,

    )


    user: Mapped[str] = mapped_column(

        String(100),

        nullable=False,

    )


    event: Mapped[str] = mapped_column(

        String,

        nullable=False,

    )


    resource: Mapped[str] = mapped_column(

        String(100),

        nullable=False,

    )


    details: Mapped[str | None] = mapped_column(

        Text,

        nullable=True,

    )


    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

    )