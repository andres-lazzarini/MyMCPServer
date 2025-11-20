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

@mcp.resource("api://{endpoint}{?limit,offset,sort}")
def get_users_with_pagination(endpoint: str, limit: int = 10, offset: int = 0, sort: str = "name") -> dict:
    """Gets users with pagination and sorting query parameters.
    Example: api://users?limit=5&offset=10&sort=email
    Example: api://users?limit=20
    """
    # Simulate user data based on pagination
    total_users = 100
    users = []
    
    for i in range(offset, min(offset + limit, total_users)):
        users.append({
            "id": i + 1,
            "name": f"User {i + 1}",
            "email": f"user{i + 1}@example.com",
            "created_at": "2024-01-01T00:00:00Z"
        })
    
    return {
        "endpoint": endpoint,
        "users": users,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": total_users,
            "has_next": offset + limit < total_users
        },
        "sort": sort
    }

if __name__ == "__main__":
    mcp.run()