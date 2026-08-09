from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.responses import StreamingResponse

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
)


from app.services.chat_service import (
    ChatService,
)


from app.models.user import User


from app.core.auth import (
    get_current_user,
)


from app.core.chat_dependencies import (
    get_chat_service,
)



router = APIRouter(

    prefix="/chat",

    tags=["AI Chat"],

)



@router.post(

    "",

    response_model=ChatResponse,

    status_code=status.HTTP_200_OK,

)
async def chat(

    request: ChatRequest,

    current_user: User = Depends(
        get_current_user
    ),

    chat_service: ChatService = Depends(
        get_chat_service
    ),

):


    try:


        response = await chat_service.chat(

            question=request.question,

            user=current_user,

        )


        return ChatResponse(

            **response

        )



    except ValueError as exc:


        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(exc),

        )



    except Exception:


        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="AI processing failed",

        )

@router.post(
    "/stream"
)
async def stream_chat(

    request: ChatRequest,

    current_user: User = Depends(
        get_current_user
    ),

    chat_service: ChatService = Depends(
        get_chat_service
    ),

):


    return StreamingResponse(

        chat_service.stream_chat(

            question=request.question,

            user=current_user,

        ),

        media_type="text/event-stream",

    )