from openai import AsyncAzureOpenAI

from app.core.config import settings



class EmbeddingClient:


    def __init__(self):

        self.client = AsyncAzureOpenAI(

            api_key=settings.AZURE_OPENAI_API_KEY,

            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,

            api_version=settings.AZURE_OPENAI_API_VERSION,

        )



    async def create_embedding(

        self,

        text: str,

    ):


        response = await self.client.embeddings.create(

            model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,

            input=text,

        )


        return response.data[0].embedding