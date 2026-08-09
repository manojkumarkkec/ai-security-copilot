from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    OAuth2PasswordBearer,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


from app.core.security import (
    decode_access_token,
)

from app.core.events import (
    SecurityEvent,
)

from app.database.session import (
    get_db,
)

from app.repositories.user_repository import (
    UserRepository,
)

from app.models.user import (
    User,
)

from app.services.audit_service import (
    AuditService,
)



oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="/api/v1/auth/login"

)



user_repository = UserRepository()

audit_service = AuditService()



async def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: AsyncSession = Depends(get_db),

) -> User:



    payload = decode_access_token(
        token
    )



    # ---------------------------------
    # Invalid JWT
    # ---------------------------------

    if payload is None:


        await audit_service.log(

            session=db,

            user="UNKNOWN",

            event=SecurityEvent.TOKEN_VALIDATION_FAILED,

            resource="JWT",

            details={

                "reason": "Invalid or expired token",

            },

        )


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token",

        )



    user_id = payload.get(
        "sub"
    )



    # ---------------------------------
    # Missing subject
    # ---------------------------------

    if user_id is None:


        await audit_service.log(

            session=db,

            user="UNKNOWN",

            event=SecurityEvent.TOKEN_VALIDATION_FAILED,

            resource="JWT",

            details={

                "reason": "Missing subject claim",

            },

        )


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token payload",

        )



    # ---------------------------------
    # Load User
    # ---------------------------------

    user = await user_repository.get_by_id(

        db,

        user_id,

    )



    if user is None:


        await audit_service.log(

            session=db,

            user=str(user_id),

            event=SecurityEvent.TOKEN_VALIDATION_FAILED,

            resource="JWT",

            details={

                "reason": "User does not exist",

            },

        )


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="User not found",

        )



    return user