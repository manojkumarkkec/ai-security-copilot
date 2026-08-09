from app.models.enums import ScannerType

from app.scanners.rules.base import ScannerRule


class TenableRule(ScannerRule):


    REQUIRED_FIELDS = {
        "plugin_id",
        "plugin_name",
        "severity"
    }


    def matches(
        self,
        data: list[dict],
    ) -> bool:


        if not data:
            return False


        fields = set(
            data[0].keys()
        )


        return self.REQUIRED_FIELDS.issubset(
            fields
        )


    def scanner_type(
        self,
    ) -> ScannerType:

        return ScannerType.TENABLE