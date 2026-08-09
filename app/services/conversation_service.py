from sqlalchemy.ext.asyncio import AsyncSession


from app.models.conversation import Conversation


from app.repositories.conversation_repository import (
    ConversationRepository,
)



class ConversationService:


    def __init__(self):

        self.repository = ConversationRepository()



    async def save(

        self,

        session: AsyncSession,

        user_id,

        question: str,

        answer: str,

    ):


        conversation = Conversation(

            user_id=user_id,

            question=question,

            answer=answer,

        )


        return await self.repository.create(

            session,

            conversation,

        )



    async def get_history(

        self,

        session: AsyncSession,

        user_id,

    ):


        conversations = await self.repository.get_recent(

            session,

            user_id,

            limit=5,

        )


        history = []


        for item in reversed(conversations):


            history.append(

                {

                    "role": "user",

                    "content": item.question,

                }

            )


            history.append(

                {

                    "role": "assistant",

                    "content": item.answer,

                }

            )


        return history