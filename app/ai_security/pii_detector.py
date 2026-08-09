import re


class PIIDetector:


    EMAIL = re.compile(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    )


    PHONE = re.compile(

        r"\b\d{10}\b"

    )


    def sanitize(

        self,

        text: str,

    ):


        text = self.EMAIL.sub(

            "[EMAIL]",

            text,

        )


        text = self.PHONE.sub(

            "[PHONE]",

            text,

        )


        return text