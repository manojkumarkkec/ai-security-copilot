import csv
import io
import json


class RawFileParser:


    def parse(
        self,
        filename: str,
        content: bytes,
    ) -> list[dict]:


        filename = filename.lower()


        if filename.endswith(".csv"):

            return self._parse_csv(
                content
            )


        if filename.endswith(".json"):

            return self._parse_json(
                content
            )


        raise ValueError(
            "Unsupported file format."
        )



    def _parse_csv(
        self,
        content: bytes,
    ) -> list[dict]:


        text = content.decode(
            "utf-8"
        )


        reader = csv.DictReader(
            io.StringIO(text)
        )


        return list(reader)



    def _parse_json(
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


        return data