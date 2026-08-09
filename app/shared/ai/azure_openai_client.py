from typing import AsyncGenerator

from openai import AsyncAzureOpenAI

from app.core.config import settings



class AzureOpenAIClient:


    def __init__(self):

        self.client = AsyncAzureOpenAI(

            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,

            api_key=settings.AZURE_OPENAI_API_KEY,

            api_version=settings.AZURE_OPENAI_API_VERSION,

        )


        self.deployment = (
            settings.AZURE_OPENAI_DEPLOYMENT_NAME
        )



    async def chat_completion(

        self,

        messages: list[dict],

    ):


        response = await self.client.chat.completions.create(

            model=self.deployment,

            messages=messages,

            temperature=0.2,

        )


        # Return complete response
        # Required for token usage tracking

        return response




    async def stream_chat_completion(

        self,

        messages: list[dict],

    ) -> AsyncGenerator[str, None]:


        response = await self.client.chat.completions.create(

            model=self.deployment,

            messages=messages,

            temperature=0.2,

            stream=True,

        )


        async for chunk in response:


            if not chunk.choices:

                continue


            token = chunk.choices[0].delta.content


            if token:

                yield token