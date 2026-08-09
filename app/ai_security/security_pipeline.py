from app.ai_security.input_filter import InputFilter

from app.ai_security.prompt_injection_detector import (
    PromptInjectionDetector,
)

from app.ai_security.pii_detector import (
    PIIDetector,
)

from app.ai_security.output_filter import (
    OutputFilter,
)


class SecurityPipeline:


    def __init__(self):

        self.input_filter = InputFilter()

        self.injection = PromptInjectionDetector()

        self.pii = PIIDetector()

        self.output = OutputFilter()


    def secure_input(

        self,

        prompt: str,

    ):


        prompt = self.input_filter.validate(

            prompt

        )


        prompt = self.injection.validate(

            prompt

        )


        prompt = self.pii.sanitize(

            prompt

        )


        return prompt


    def secure_output(

        self,

        answer: str,

    ):


        return self.output.validate(

            answer

        )