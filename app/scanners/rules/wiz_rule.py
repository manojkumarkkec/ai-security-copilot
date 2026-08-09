from app.models.enums import ScannerType

from app.scanners.rules.base import ScannerRule


class WizRule(ScannerRule):


    REQUIRED_FIELDS = {
        "issue_name",
        "risk",
        "asset"
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

        return ScannerType.WIZ