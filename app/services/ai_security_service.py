from app.ai_security.prompt_guard import (
    PromptGuard,
)

from app.ai_security.pii_detector import (
    PIIDetector,
)

from app.ai_security.output_filter import (
    OutputFilter,
)



class AISecurityService:


    def __init__(self):

        self.prompt_guard = PromptGuard()

        self.pii_detector = PIIDetector()

        self.output_filter = OutputFilter()



    def validate_input(

        self,

        prompt: str,

    ) -> str:


        prompt = self.prompt_guard.check(

            prompt

        )


        return self.pii_detector.mask(

            prompt

        )



    def validate_output(

        self,

        response: str,

    ) -> str:


        return self.output_filter.validate(

            response

        )