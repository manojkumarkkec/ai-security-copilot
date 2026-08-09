from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
async def get_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value
    }