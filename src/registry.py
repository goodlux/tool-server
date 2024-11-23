from typing import Callable, Dict, List, Literal, Any, Type
from dataclasses import dataclass
import inspect
from .core_tools.base_tool import BaseTool

@dataclass
class ToolInfo:
    name: str
    description: str
    parameters: List[Dict[str, Any]]
    returns: str

class ToolRegistry:
    _tools: Dict[str, Type[BaseTool]] = {}
    _tool_info: Dict[str, ToolInfo] = {}

    @classmethod
    def register_tool(cls, tool_class: Type[BaseTool]) -> None:
        """Register a tool class"""
        tool = tool_class()
        cls._tools[tool.name] = tool_class
        cls._tool_info[tool.name] = ToolInfo(
            name=tool.name,
            description=tool.description,
            parameters=[],  # You might want to add parameter inspection here
            returns="Any"
        )

    @classmethod
    def convert_type_to_gpt(cls, type_str: str) -> str:
        """Convert Python types to JSON Schema types"""
        type_mapping = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object"
        }
        return type_mapping.get(type_str, "string")

    @classmethod
    def convert_type_to_anthropic(cls, type_str: str) -> str:
        """Convert Python types to Anthropic format types"""
        return type_str

    @classmethod
    async def execute_tool(cls, name: str, **kwargs: Any) -> Any:
        """Execute a registered tool"""
        if name not in cls._tools:
            raise ValueError(f"Tool {name} not found")
        tool = cls._tools[name]()
        return await tool.execute(**kwargs)

    @classmethod
    def list_tools(cls, format_type: Literal["gpt", "anthropic"] = "gpt") -> List[Dict[str, Any]]:
        """List available tools in specified format"""
        if format_type == "gpt":
            return [{
                "name": info.name,
                "description": info.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param["name"]: {
                            "type": cls.convert_type_to_gpt(param["type"]),
                            "description": param["description"]
                        } for param in info.parameters
                    },
                    "required": [p["name"] for p in info.parameters if p["required"]]
                }
            } for info in cls._tool_info.values()]
        else:
            return [{
                "name": info.name,
                "description": info.description,
                "parameters": [
                    {
                        "name": param["name"],
                        "type": cls.convert_type_to_anthropic(param["type"]),
                        "description": param["description"],
                        "required": param["required"]
                    } for param in info.parameters
                ]
            } for info in cls._tool_info.values()]
