from fastapi import HTTPException


BLOCKED_PATTERNS = [

    "ignore previous instructions",

    "system prompt",

    "reveal your instructions",

    "developer message",

    "jailbreak",

]


class InputFilter:


    def validate(

        self,

        text: str,

    ) -> str:


        normalized = text.lower()



        for pattern in BLOCKED_PATTERNS:


            if pattern in normalized:


                raise HTTPException(

                    status_code=400,

                    detail="Potential prompt injection detected.",

                )


        return text