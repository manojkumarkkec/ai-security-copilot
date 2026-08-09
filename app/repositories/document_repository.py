from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document



class DocumentRepository:


    async def bulk_create(

        self,

        session: AsyncSession,

        documents: list[Document],

    ):


        session.add_all(

            documents

        )


        await session.flush()


        return documents