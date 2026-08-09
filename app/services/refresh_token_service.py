from datetime import (
    datetime,
    timezone,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken

from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)

from app.core.security import (
    create_refresh_token,
    decode_refresh_token,
)

from app.services.audit_service import (
    AuditService,
)

from app.core.events import (
    SecurityEvent,
)



class RefreshTokenService:


    def __init__(self):

        self.repository = RefreshTokenRepository()

        self.audit_service = AuditService()



    async def create_token(

        self,

        session: AsyncSession,

        user_id: str,

        username: str,

    ) -> str:


        token = create_refresh_token(

            {

                "sub": user_id,

            }

        )



        expires_at = datetime.fromtimestamp(

            self._get_expiry(token),

            tz=timezone.utc,

        )



        refresh_token = RefreshToken(

            user_id=user_id,

            token=token,

            expires_at=expires_at,

        )



        await self.repository.create(

            session,

            refresh_token,

        )



        await self.audit_service.log(

            session=session,

            user=username,

            action="REFRESH_TOKEN_CREATED",

            resource="AUTH",

            details={

                "user_id": user_id,

            },

        )


        return token



    async def validate_token(

        self,

        session: AsyncSession,

        token: str,

    ) -> RefreshToken:



        payload = decode_refresh_token(

            token

        )



        if payload is None:

            raise ValueError(

                "Invalid refresh token"

            )



        stored_token = await self.repository.get_by_token(

            session,

            token,

        )



        if stored_token is None:

            raise ValueError(

                "Refresh token not found"

            )



        if stored_token.revoked:

            raise ValueError(

                "Refresh token revoked"

            )



        if stored_token.expires_at < datetime.now(timezone.utc):

            raise ValueError(

                "Refresh token expired"

            )



        return stored_token



    async def revoke_token(

        self,

        session: AsyncSession,

        token: str,

        username: str,

    ) -> None:



        refresh_token = await self.repository.get_by_token(

            session,

            token,

        )



        if refresh_token:


            await self.repository.revoke(

                session,

                refresh_token,

            )



            await self.audit_service.log(

                session=session,

                user=username,

                action="REFRESH_TOKEN_REVOKED",

                resource="AUTH",

                details={

                    "token_id": str(refresh_token.id),

                },

            )



    def _get_expiry(

        self,

        token: str,

    ) -> int:


        payload = decode_refresh_token(

            token

        )


        if payload is None:

            raise ValueError(

                "Unable to decode token"

            )


        return payload["exp"]