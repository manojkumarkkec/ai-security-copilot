from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
)

from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from datetime import datetime,timezone
import uuid

from app.database.base import Base



class Document(Base):


    __tablename__ = "documents"


    id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4,

    )


    content = Column(

        Text,

        nullable=False,

    )


    source = Column(

        String(255),

        nullable=False,

    )


    metadata_json = Column(

        Text,

        nullable=True,

    )


    embedding = Column(

        Vector(1536),

        nullable=False,

    )


    created_at = Column(

        DateTime,

        default=datetime.now(timezone.utc),

    )

    category = Column(
    String(100),
    nullable=True,
    )

    document_type = Column(
        String(50),
        nullable=True,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    page_number = Column(
        Integer,
        nullable=True,
    )