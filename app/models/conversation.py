import uuid
from datetime import datetime,timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )