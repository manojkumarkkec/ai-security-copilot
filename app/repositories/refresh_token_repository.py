from datetime import datetime, timezone

from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken



class RefreshTokenRepository:



    async def create(

        self,

        session: AsyncSession,

        refresh_token: RefreshToken,

    ) -> RefreshToken:



        session.add(

            refresh_token

        )


        await session.flush()


        await session.refresh(

            refresh_token

        )


        return refresh_token





    async def get_by_token(

        self,

        session: AsyncSession,

        token: str,

    ) -> RefreshToken | None:



        query = select(

            RefreshToken

        ).where(

            RefreshToken.token == token

        )



        result = await session.execute(

            query

        )


        return result.scalar_one_or_none()





    async def revoke(

        self,

        session: AsyncSession,

        refresh_token: RefreshToken,

    ) -> RefreshToken:



        refresh_token.revoked = True


        session.add(

            refresh_token

        )


        await session.flush()


        await session.refresh(

            refresh_token

        )


        return refresh_token





    async def delete_expired(

        self,

        session: AsyncSession,

    ) -> None:



        now = datetime.now(

            timezone.utc

        )


        query = (

            update(RefreshToken)

            .where(

                RefreshToken.expires_at < now

            )

            .values(

                revoked=True

            )

        )


        await session.execute(

            query

        )