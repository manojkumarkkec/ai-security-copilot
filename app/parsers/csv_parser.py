import csv
import io

from app.parsers.base import FileParser


class CSVParser(FileParser):


    def parse(
        self,
        content: bytes,
    ) -> list[dict]:

        text = content.decode(
            "utf-8"
        )


        reader = csv.DictReader(
            io.StringIO(text)
        )


        records = []


        for row in reader:

            records.append(
                dict(row)
            )


        return records