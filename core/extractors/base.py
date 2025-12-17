from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def supports(self, filename: str) -> bool:
        pass

    @abstractmethod
    def extract(self, file) -> str:
        pass
