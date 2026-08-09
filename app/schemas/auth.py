from pydantic import BaseModel, EmailStr



class UserRegisterRequest(BaseModel):

    username: str

    email: EmailStr

    password: str



class UserLoginRequest(BaseModel):

    email: EmailStr

    password: str



class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"



class RefreshTokenRequest(BaseModel):

    refresh_token: str



class LogoutRequest(BaseModel):

    refresh_token: str