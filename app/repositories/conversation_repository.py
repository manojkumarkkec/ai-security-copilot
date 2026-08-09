from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:


    async def create(

        self,

        session: AsyncSession,

        conversation: Conversation,

    ) -> Conversation:

        session.add(conversation)

        await session.flush()

        await session.refresh(conversation)

        return conversation



    async def get_recent(

        self,

        session: AsyncSession,

        user_id,

        limit: int = 5,

    ) -> list[Conversation]:

        statement = (

            select(Conversation)

            .where(

                Conversation.user_id == user_id

            )

            .order_by(

                Conversation.created_at.desc()

            )

            .limit(limit)

        )

        result = await session.execute(statement)

        return list(result.scalars().all())