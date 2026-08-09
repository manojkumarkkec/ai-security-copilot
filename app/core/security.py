from datetime import (
    datetime,
    timedelta,
    timezone,
)

from typing import Any

from jose import (
    JWTError,
    jwt,
)

from pwdlib import PasswordHash

from app.core.config import settings



password_hash = PasswordHash.recommended()



# ------------------------------------
# Password
# ------------------------------------

def hash_password(

    password: str,

) -> str:

    return password_hash.hash(

        password

    )



def verify_password(

    plain_password: str,

    hashed_password: str,

) -> bool:

    return password_hash.verify(

        plain_password,

        hashed_password,

    )



# ------------------------------------
# Access Token
# ------------------------------------

def create_access_token(

    data: dict[str, Any],

    expires_delta: timedelta | None = None,

) -> str:


    payload = data.copy()



    if expires_delta:


        expire = (

            datetime.now(timezone.utc)

            + expires_delta

        )


    else:


        expire = (

            datetime.now(timezone.utc)

            + timedelta(

                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES

            )

        )



    payload.update(

        {

            "exp": expire,

            "type": "access",

        }

    )



    return jwt.encode(

        payload,

        settings.JWT_SECRET,

        algorithm=settings.JWT_ALGORITHM,

    )





def decode_access_token(

    token: str,

) -> dict[str, Any] | None:


    try:


        payload = jwt.decode(

            token,

            settings.JWT_SECRET,

            algorithms=[

                settings.JWT_ALGORITHM

            ],

        )


        if payload.get("type") != "access":

            return None



        return payload



    except JWTError:


        return None



# ------------------------------------
# Refresh Token
# ------------------------------------

def create_refresh_token(

    data: dict[str, Any],

) -> str:


    payload = data.copy()



    expire = (

        datetime.now(timezone.utc)

        + timedelta(

            days=settings.REFRESH_TOKEN_EXPIRE_DAYS

        )

    )



    payload.update(

        {

            "exp": expire,

            "type": "refresh",

        }

    )



    return jwt.encode(

        payload,

        settings.JWT_SECRET,

        algorithm=settings.JWT_ALGORITHM,

    )





def decode_refresh_token(

    token: str,

) -> dict[str, Any] | None:


    try:


        payload = jwt.decode(

            token,

            settings.JWT_SECRET,

            algorithms=[

                settings.JWT_ALGORITHM

            ],

        )



        if payload.get("type") != "refresh":

            return None



        return payload



    except JWTError:


        return None