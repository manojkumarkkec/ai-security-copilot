import json

from app.parsers.base import FileParser

class JSONParser(FileParser):


    def parse(
        self,
        content: bytes,
    ) -> list[dict]:


        data = json.loads(
            content.decode("utf-8")
        )


        if not isinstance(data, list):

            raise ValueError(
                "JSON root must be an array."
            )


        records = []


        for item in data:

            if not isinstance(item, dict):

                raise ValueError(
                    "Each JSON item must be an object."
                )


            records.append(
                item
            )


        return records