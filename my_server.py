from typing import Dict, Any
import time

from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent


mcp = FastMCP("My MCP Server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name"""
    return f"Hello, {name} from My MCP Server!"

@mcp.resource("resource://server/status")
def server_status() -> Dict[str, Any]:
    """
    Return basic server status information as a resource.
    Clients can fetch it via readResource.
    """
    return {
        "server": "mcpserver2",
        "uptime_seconds": int(time.time()),
        "status": "running",
        "version": "1.0.0"
    }

@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> dict:
    """Provides weather information for a specific city."""
    # In a real implementation, this would call a weather API
    # Here we're using simplified logic for example purposes
    return {
        "city": city.capitalize(),
        "temperature": 22,
        "condition": "Sunny",
        "unit": "celsius"
    }

@mcp.resource("repo://{owner}/{path*}/template.py")
def get_template_file(owner: str, path: str) -> dict:
    """Retrieves a file from a specific repository and path, but
    only if the resource ends with `template.py`"""
    # Can match repo://jlowin/fastmcp/src/resources/template.py
    return {
        "owner": owner,
        "path": path + "/template.py",
        "content": f"File at {path}/template.py in {owner}'s repository"
    }

@mcp.resource("data://{id}{?format}")
def get_data(id: str, format: str = "json") -> str:
    """Retrieve data in specified format."""
    if format == "xml":
        return f"<data id='{id}' />"
    return f'{{"id": "{id}"}}'

@mcp.resource("image://logo.png", mime_type="image/png")
def get_logo() -> bytes:
    """Provides the server's logo image."""
    with open("logo.png", "rb") as f:
        return f.read()

@mcp.prompt()
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

if __name__ == "__main__":
    mcp.run()