from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document

from app.parsers.pdf_parser import (
    PDFParser,
)

from app.services.chunking_service import (
    ChunkingService,
)

from app.shared.ai.embedding_client import (
    EmbeddingClient,
)

from app.repositories.document_repository import (
    DocumentRepository,
)


class DocumentIngestionService:


    def __init__(self):

        self.parser = PDFParser()

        self.chunker = ChunkingService()

        self.embedding_client = EmbeddingClient()

        self.repository = DocumentRepository()



    async def ingest(

        self,

        session: AsyncSession,

        filename: str,

        content: bytes,

        category: str = "Security",

    ) -> dict:


        # ---------------------------------------
        # Extract text from PDF
        # ---------------------------------------

        text = self.parser.parse(

            content

        )


        if not text.strip():

            raise ValueError(

                "Document contains no readable text."

            )


        # ---------------------------------------
        # Split into chunks
        # ---------------------------------------

        chunks = self.chunker.split(

            text

        )


        documents: list[Document] = []


        # ---------------------------------------
        # Generate embeddings and build documents
        # ---------------------------------------

        for index, chunk in enumerate(chunks):


            embedding = await self.embedding_client.create_embedding(

                chunk

            )


            document = Document(

                content=chunk,

                source=filename,

                embedding=embedding,

                category=category,

                document_type="PDF",

                chunk_index=index,

                page_number=None,

            )


            documents.append(

                document

            )


        # ---------------------------------------
        # Store in PostgreSQL
        # ---------------------------------------

        await self.repository.bulk_create(

            session=session,

            documents=documents,

        )


        await session.commit()


        return {

            "message": "Document indexed successfully.",

            "document_count": len(documents),

            "chunks_created": len(chunks),

            "source": filename,

        }