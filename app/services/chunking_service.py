class ChunkingService:


    def __init__(

        self,

        chunk_size: int = 1000,

        overlap: int = 200,

    ):

        self.chunk_size = chunk_size

        self.overlap = overlap



    def split(

        self,

        text: str,

    ) -> list[str]:


        chunks = []


        start = 0


        while start < len(text):


            end = start + self.chunk_size


            chunks.append(

                text[start:end]

            )


            start = end - self.overlap



        return chunks