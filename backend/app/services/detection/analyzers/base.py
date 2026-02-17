from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AnalyzerResult:
    score: float  # 0-1, where 1 = more AI-like
    confidence: float  # 0-1
    details: dict = field(default_factory=dict)


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str, language: str) -> AnalyzerResult:
        ...
