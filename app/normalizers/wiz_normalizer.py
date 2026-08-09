from app.models.enums import (
    VulnerabilitySeverity,
    VulnerabilityStatus,
)
from app.models.vulnerability_model import VulnerabilityModel


class WizNormalizer:

    def normalize(
        self,
        item: dict,
    ) -> VulnerabilityModel:

        return VulnerabilityModel(
            external_id=item["id"],
            title=item["issue_name"],
            description=item.get("description", ""),
            severity=VulnerabilitySeverity(
                item["risk"].upper()
            ),
            status=VulnerabilityStatus.OPEN,
            asset_name=item["asset"],
            source="WIZ",
            remediation=item.get("fix", ""),
        )