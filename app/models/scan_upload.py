import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.enums import ScanStatus


class ScanUpload(Base):

    __tablename__ = "scan_uploads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    scanner: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    uploaded_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[ScanStatus] = mapped_column(
        Enum(ScanStatus),
        default=ScanStatus.PROCESSING,
        nullable=False,
    )

    total_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    inserted_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    duplicate_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    failed_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )

    error_message: Mapped[str | None] = mapped_column(
        String(255),    
        nullable=True,   
    ) 
