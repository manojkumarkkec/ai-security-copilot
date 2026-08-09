from app.parsers.csv_parser import CSVParser
from app.parsers.json_parser import JSONParser



class ParserFactory:


    def get(
        self,
        filename: str,
    ):


        filename = filename.lower()


        if filename.endswith(".csv"):

            return CSVParser()


        if filename.endswith(".json"):

            return JSONParser()


        raise ValueError(
            "Unsupported file format."
        )