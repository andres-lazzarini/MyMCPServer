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

@mcp.resource("resource://server/user/{user_id}")
def user_info(user_id: str) -> Dict[str, Any]:
    """
    Dynamic resource template.

    Any URI that matches:
      resource://server/user/<ANY_VALUE>

    will trigger this function with user_id injected.
    """
    return {
        "requested_user": user_id,
        "status": "ok",
        "generated_at": int(time.time()),
        "data": {
            "name": f"User {user_id}",
            "role": "tester",
            "active": True
        }
    }

if __name__ == "__main__":
    mcp.run()