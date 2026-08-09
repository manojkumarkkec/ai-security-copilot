from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document

from app.shared.ai.embedding_client import (
    EmbeddingClient,
)


class RetrieverService:


    def __init__(

        self,

        session: AsyncSession,

    ):

        self.session = session

        self.embedding_client = EmbeddingClient()



    async def search(

        self,

        query: str,

        top_k: int = 5,

        category: str | None = None,

    ) -> list[Document]:


        query_embedding = await self.embedding_client.create_embedding(

            query

        )


        similarity = Document.embedding.cosine_distance(

            query_embedding

        )


        statement = select(

            Document

        )


        if category:

            statement = statement.where(

                Document.category == category

            )


        statement = (

            statement

            .order_by(similarity)

            .limit(top_k)

        )


        result = await self.session.execute(

            statement

        )


        documents = list(

            result.scalars().all()

        )


        return documents