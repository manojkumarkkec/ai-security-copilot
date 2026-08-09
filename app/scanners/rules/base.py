from abc import ABC, abstractmethod

from app.models.enums import ScannerType


class ScannerRule(ABC):


    @abstractmethod
    def matches(
        self,
        data: list[dict],
    ) -> bool:
        pass


    @abstractmethod
    def scanner_type(
        self,
    ) -> ScannerType:
        pass