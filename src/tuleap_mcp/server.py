import os
import sys
from mcp.server.fastmcp import FastMCP
from .client import TuleapClient
from .tools import users, trackers, agile, files

def get_client() -> TuleapClient:
    tuleap_url = os.getenv("TULEAP_URL")
    tuleap_api_key = os.getenv("TULEAP_API_KEY")
    
    if not tuleap_url or not tuleap_api_key:
        print("Error: TULEAP_URL and TULEAP_API_KEY environment variables must be set.", file=sys.stderr)
        sys.exit(1)
        
    return TuleapClient(tuleap_url, tuleap_api_key)

mcp = FastMCP("Tuleap MCP Server")

@mcp.tool()
async def search_users(query: str = None) -> str:
    """Search for users in Tuleap."""
    client = get_client()
    return str(await users.get_users(client, query))

@mcp.tool()
async def get_artifact(artifact_id: int) -> str:
    """Get details of a specific artifact."""
    client = get_client()
    return str(await trackers.get_artifact_details(client, artifact_id))

@mcp.tool()
async def search_artifacts(tracker_id: int, query: str = None) -> str:
    """Search for artifacts in a specific tracker."""
    client = get_client()
    return str(await trackers.search_artifacts(client, tracker_id, query))

@mcp.tool()
async def search_projects(query: str = None) -> str:
    """Search for projects."""
    client = get_client()
    return str(await agile.search_projects(client, query))

@mcp.tool()
async def get_project_epics(project_id: int) -> str:
    """Get epics for a project."""
    client = get_client()
    return str(await agile.get_epics(client, project_id))

@mcp.tool()
async def get_git_repos(project_id: int) -> str:
    """Get git repositories for a project."""
    client = get_client()
    return str(await files.get_git_repositories(client, project_id))

def main():
    mcp.run()

if __name__ == "__main__":
    main()
