from collections.abc import Callable

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    get_current_user,
)

from app.core.events import (
    SecurityEvent,
)

from app.database.session import (
    get_db,
)

from app.models.enums import (
    UserRole,
)

from app.models.user import (
    User,
)

from app.services.audit_service import (
    AuditService,
)



audit_service = AuditService()



def require_roles(

    *allowed_roles: UserRole,

) -> Callable:



    async def role_checker(

        current_user: User = Depends(get_current_user),

        session: AsyncSession = Depends(get_db),

    ) -> User:



        if current_user.role not in allowed_roles:



            await audit_service.log(

                session=session,

                user=current_user.username,

                event=SecurityEvent.ROLE_ACCESS_DENIED,

                resource="RBAC",

                details={

                    "user_role": current_user.role.value,

                    "required_roles": [

                        role.value

                        for role in allowed_roles

                    ],

                },

            )



            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail=(

                    "You do not have permission "

                    "to perform this action."

                ),

            )



        return current_user



    return role_checker