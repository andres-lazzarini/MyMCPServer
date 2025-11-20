from typing import Dict, Any
import time

from fastmcp import FastMCP

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

if __name__ == "__main__":
    mcp.run()