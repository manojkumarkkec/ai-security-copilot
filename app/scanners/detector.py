from app.models.enums import ScannerType

from app.scanners.rules.wiz_rule import WizRule
from app.scanners.rules.tenable_rule import TenableRule



class ScannerDetector:


    def __init__(self):

        self.rules = [
            WizRule(),
            TenableRule(),
        ]



    def detect(
        self,
        data: list[dict],
    ) -> ScannerType:


        for rule in self.rules:

            if rule.matches(data):

                return rule.scanner_type()


        return ScannerType.UNKNOWN