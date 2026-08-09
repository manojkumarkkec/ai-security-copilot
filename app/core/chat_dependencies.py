from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.database.session import get_db


from app.services.chat_service import ChatService


from app.services.retriever_service import (
    RetrieverService,
)



async def get_chat_service(

    db: AsyncSession = Depends(get_db),

):


    retriever = RetrieverService(

        session=db

    )


    return ChatService(

        session=db,

        retriever_service=retriever,

    )