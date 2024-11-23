from datetime import datetime
from .base_tool import BaseTool
from typing import Any, Dict

class NowTool(BaseTool):
    @property
    def name(self) -> str:
        return "now"

    @property
    def description(self) -> str:
        return "Returns current server time"

    async def execute(self, **kwargs: Dict[str, Any]) -> str:
        return datetime.now().isoformat()
