from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Duration, Limiter, Rate

from app.database.session import get_db


from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
)


from app.services.auth_service import (
    AuthService,
)


from app.core.auth import (
    get_current_user,
)


from app.models.user import User



router = APIRouter(

    prefix="/auth",

    tags=["Authentication"],

)



auth_service = AuthService()

login_limiter = Limiter(
    Rate(
        5,
        Duration.MINUTE,
    )
)

@router.post(

    "/register",

    status_code=status.HTTP_201_CREATED,

)

async def register_user(

    request: UserRegisterRequest,

    db: AsyncSession = Depends(get_db),

):


    try:


        user = await auth_service.register(

            db,

            request,

        )


        return {


            "message": "User created successfully",


            "user_id": str(user.id),


        }



    except ValueError as error:


        raise HTTPException(

            status_code=400,

            detail=str(error),

        )





@router.post(

    "/login",

    response_model=TokenResponse,
    dependencies=[
        Depends(
            RateLimiter(
                limiter=login_limiter
            )
        )
    ]

)

async def login_user(

    request: UserLoginRequest,

    db: AsyncSession = Depends(get_db),

):


    try:


        tokens = await auth_service.login(

            db,

            request,

        )


        return TokenResponse(

            **tokens

        )



    except ValueError as error:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail=str(error),

        )





@router.post(

    "/refresh",

    response_model=TokenResponse,

)

async def refresh_token(

    request: RefreshTokenRequest,

    db: AsyncSession = Depends(get_db),

):


    try:


        tokens = await auth_service.refresh_access_token(

            db,

            request.refresh_token,

        )


        return TokenResponse(

            **tokens

        )



    except ValueError as error:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail=str(error),

        )





@router.post(

    "/logout",

    status_code=status.HTTP_200_OK,

)

async def logout_user(

    request: LogoutRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(get_current_user),

):


    try:


        await auth_service.logout(

            session=db,

            refresh_token=request.refresh_token,

            username=current_user.username,

        )


        return {


            "message": "Logged out successfully"


        }



    except ValueError as error:


        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(error),

        )