from fastapi import FastAPI, Request
from typing import Dict, List, Literal, Any
from .registry import ToolRegistry
from .core_tools.now_tool import NowTool

app = FastAPI()

# Register tools
ToolRegistry.register_tool(NowTool)

@app.post("/execute")
async def execute_tool(request: Request) -> Dict[str, Any]:
    data = await request.json()

    if "name" in data and "arguments" in data:
        tool_name = data["name"]
        arguments = data["arguments"]
    elif "type" in data and data["type"] == "tool_call":
        tool_name = data["tool_name"]
        arguments = data["parameters"]
    else:
        return {"error": "Unsupported tool call format"}

    try:
        result = await ToolRegistry.execute_tool(tool_name, **arguments)
        return {
            "status": "success",
            "tool_name": tool_name,
            "output": result
        }
    except Exception as e:
        return {
            "status": "error",
            "tool_name": tool_name,
            "error": str(e)
        }

@app.get("/list-tools/{format_type}")
async def list_tools(format_type: Literal["gpt", "anthropic"] = "gpt") -> List[Dict[str, Any]]:
    return ToolRegistry.list_tools(format_type=format_type)
