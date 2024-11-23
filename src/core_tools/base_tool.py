from abc import ABC, abstractmethod
from typing import Any,  Dict

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass

    @abstractmethod
    async def execute(self, **kwargs: Dict[str, Any]) -> Any:
        """Execute the tool"""
        pass
