import os
import sys
from mcp.server.fastmcp import FastMCP
from .client import TuleapClient
from .tools import users, trackers, agile, files


def get_client() -> TuleapClient:
    tuleap_url = os.getenv("TULEAP_URL")
    tuleap_api_key = os.getenv("TULEAP_API_KEY")

    if not tuleap_url or not tuleap_api_key:
        print(
            "Error: TULEAP_URL and TULEAP_API_KEY environment variables must be set.",
            file=sys.stderr,
        )
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
    """Get details of a specific artifact. This includes the fields and values like status, start_date, end_date."""
    client = get_client()
    return str(await trackers.get_artifact_details(client, artifact_id))


@mcp.tool()
async def update_artifact(
    artifact_id: int, values: list = None, comment: str = None
) -> str:
    """Update an artifact's fields or add a comment. Values should be a list of dictionaries with field updates. At least one of values or comment is required."""
    client = get_client()
    if not values and not comment:
        return "Error: Must provide either values or comment to update."
    if values is None:
        values = []
    return str(await trackers.update_artifact(client, artifact_id, values, comment))


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
    """Get epics for a project. To see details like start/end dates, you might need to use get_artifact on the returned IDs."""
    client = get_client()
    return str(await agile.get_epics(client, project_id))


@mcp.tool()
async def get_project_user_stories(project_id: int, epic_id: int = None) -> str:
    """Get user stories for a project, optionally filtered by an Epic ID."""
    client = get_client()
    return str(await agile.get_user_stories(client, project_id, epic_id))


@mcp.tool()
async def create_user_story(project_id: int, values: list) -> str:
    """Create a new user story artifact in a project. Values should be a list of dictionaries defining the story fields."""
    client = get_client()
    return str(await agile.create_user_story(client, project_id, values))


@mcp.tool()
async def get_git_repos(project_id: int) -> str:
    """Get git repositories for a project."""
    client = get_client()
    return str(await files.get_git_repositories(client, project_id))


def main():
    mcp.run()


if __name__ == "__main__":
    main()
