from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class TransformContext:
    language: str
    intensity: str  # "light", "medium", "aggressive"
    changes: list[str] = field(default_factory=list)


class BaseTransformer(ABC):
    @abstractmethod
    async def transform(self, text: str, context: TransformContext) -> str:
        ...
