from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.enums import UserRole

from app.repositories.user_repository import (
    UserRepository,
)

from app.services.audit_service import (
    AuditService,
)

from app.services.refresh_token_service import (
    RefreshTokenService,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.events import (
    SecurityEvent,
)

from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
)



class AuthService:


    def __init__(self):

        self.user_repository = UserRepository()

        self.audit_service = AuditService()

        self.refresh_service = RefreshTokenService()



    async def register(

        self,

        session: AsyncSession,

        request: UserRegisterRequest,

    ) -> User:


        existing_user = await self.user_repository.get_by_email(

            session,

            request.email,

        )


        if existing_user:

            raise ValueError(

                "Email already registered"

            )



        user = User(

            username=request.username,

            email=request.email,

            password_hash=hash_password(

                request.password

            ),

            role=UserRole.DEVELOPER,

        )



        return await self.user_repository.create(

            session,

            user,

        )



    async def login(

        self,

        session: AsyncSession,

        request: UserLoginRequest,

    ) -> dict:



        user = await self.user_repository.get_by_email(

            session,

            request.email,

        )



        if not user:


            await self.audit_service.log(

                session=session,

                user="UNKNOWN",

                action="LOGIN_FAILED",

                resource="AUTH",

                details={

                    "reason": "User not found",

                    "email": request.email,

                },

            )


            raise ValueError(

                "Invalid credentials"

            )



        if not verify_password(

            request.password,

            user.password_hash,

        ):



            await self.audit_service.log(

                session=session,

                user=user.username,

                action="LOGIN_FAILED",

                resource="AUTH",

                details={

                    "reason": "Invalid password",

                },

            )


            raise ValueError(

                "Invalid credentials"

            )



        access_token = create_access_token(

            {

                "sub": str(user.id),

                "role": user.role.value,

            }

        )



        refresh_token = await self.refresh_service.create_token(

            session=session,

            user_id=str(user.id),

            username=user.username,

        )



        await self.audit_service.log(

            session=session,

            user=user.username,

            action="LOGIN_SUCCESS",

            resource="AUTH",

            details={},

        )



        return {


            "access_token": access_token,


            "refresh_token": refresh_token,


            "token_type": "bearer",


        }



    async def refresh_access_token(

        self,

        session: AsyncSession,

        refresh_token: str,

    ) -> dict:



        stored_token = await self.refresh_service.validate_token(

            session,

            refresh_token,

        )



        user = await self.user_repository.get_by_id(

            session,

            stored_token.user_id,

        )



        if user is None:

            raise ValueError(

                "User not found"

            )



        new_access_token = create_access_token(

            {

                "sub": str(user.id),

                "role": user.role.value,

            }

        )



        await self.audit_service.log(

            session=session,

            user=user.username,

            action="REFRESH_TOKEN_USED",

            resource="AUTH",

            details={},

        )



        return {


            "access_token": new_access_token,


            "refresh_token": refresh_token,


            "token_type": "bearer",


        }



    async def logout(

        self,

        session: AsyncSession,

        refresh_token: str,

        username: str,

    ) -> None:



        await self.refresh_service.revoke_token(

            session,

            refresh_token,

            username,

        )



        await self.audit_service.log(

            session=session,

            user=username,

            action="LOGOUT_SUCCESS",

            resource="AUTH",

            details={},

        )