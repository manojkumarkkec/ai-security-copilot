from pydantic import BaseModel

from app.models.enums import (
    VulnerabilityStatus,
)


class UpdateStatusRequest(BaseModel):

    status: VulnerabilityStatus