import re


class PromptInjectionDetector:

    PATTERNS = [

        r"ignore previous",

        r"ignore all instructions",

        r"forget everything",

        r"system prompt",

        r"developer message",

        r"reveal prompt",

        r"bypass",

        r"override",

        r"disable safety",

        r"act as root",

        r"jailbreak",

    ]


    def validate(

        self,

        prompt: str,

    ):


        lower = prompt.lower()


        for pattern in self.PATTERNS:

            if re.search(pattern, lower):

                raise ValueError(

                    "Prompt injection detected."

                )


        return prompt