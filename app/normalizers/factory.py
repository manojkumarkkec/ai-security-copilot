from app.models.enums import ScannerType

from app.normalizers.wiz_normalizer import (
    WizNormalizer,
)

from app.normalizers.tenable_normalizer import (
    TenableNormalizer,
)

class NormalizerFactory:
     
    @staticmethod
    def get_normalizer(
            scanner: str
    ):

            if scanner == "WIZ":
                return WizNormalizer()

            if scanner == "TENABLE":
                return TenableNormalizer()

            raise ValueError(
                "Unsupported scanner"
            )