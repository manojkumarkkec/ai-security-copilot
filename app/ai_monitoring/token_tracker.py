from dataclasses import dataclass



@dataclass
class TokenUsage:

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0



class TokenTracker:


    def calculate(

        self,

        response,

    ) -> TokenUsage:


        usage = getattr(

            response,

            "usage",

            None,

        )


        if usage is None:

            return TokenUsage()



        return TokenUsage(

            prompt_tokens=usage.prompt_tokens,

            completion_tokens=usage.completion_tokens,

            total_tokens=usage.total_tokens,

        )