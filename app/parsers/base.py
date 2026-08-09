from abc import ABC, abstractmethod

from app.models.vulnerability_model import VulnerabilityModel


class FileParser(ABC):


    @abstractmethod
    def parse(
        self,
        content: bytes,
    ) -> list[dict]:
        pass