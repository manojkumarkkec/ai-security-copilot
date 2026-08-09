from langsmith import Client

from app.core.config import settings



def setup_langsmith():


    if not settings.LANGCHAIN_API_KEY:

        return None



    client = Client(

        api_key=settings.LANGCHAIN_API_KEY

    )


    return client