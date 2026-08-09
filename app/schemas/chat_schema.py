from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    question: str = Field(

        ...,

        min_length=3,

        max_length=5000,

        description="User question",

    )



class ChatResponse(BaseModel):

    answer: str

    metadata: dict

    sources: list