from app.models.enums import (
    VulnerabilitySeverity,
    VulnerabilityStatus,
)
from app.models.vulnerability_model import VulnerabilityModel


class TenableNormalizer:

    def normalize(
        self,
        item: dict,
    ) -> VulnerabilityModel:

        return VulnerabilityModel(
            external_id=str(item["plugin_id"]),
            title=item["plugin_name"],
            description=item.get("description", ""),
            severity=VulnerabilitySeverity(
                item["severity"].upper()
            ),
            status=VulnerabilityStatus.OPEN,
            asset_name=item["host"],
            source="TENABLE",
            remediation=item.get("solution", ""),
        )