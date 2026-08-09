import logging


logger = logging.getLogger(

    "llm_monitor"

)



class LLMLogger:


    def log_request(

        self,

        model: str,

        latency: float,

        tokens,

    ):


        logger.info(

            "LLM Request | model=%s latency=%s tokens=%s",

            model,

            latency,

            tokens,

        )