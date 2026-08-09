import logging
import json
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):


    def format(self, record):

        log_data = {

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "level": record.levelname,

            "event": getattr(
                record,
                "event",
                "APPLICATION_EVENT"
            ),

            "message": record.getMessage(),

        }


        if hasattr(record, "context"):

            log_data["context"] = getattr(
                record,
                "context",
                {},
            )


        return json.dumps(log_data)



logger = logging.getLogger(
    "ai_security_copilot"
)


handler = logging.StreamHandler()


handler.setFormatter(
    StructuredFormatter()
)


logger.addHandler(
    handler
)


logger.setLevel(
    logging.INFO
)