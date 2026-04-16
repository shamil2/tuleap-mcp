from typing import List, Dict, Any, Optional
from ..client import TuleapClient

async def search_projects(client: TuleapClient, query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for projects in Tuleap."""
    params = {}
    if query:
        params["query"] = query
    return await client.get("/projects", params=params)

async def get_epics(client: TuleapClient, project_id: int) -> List[Dict[str, Any]]:
    """Get epics for a project."""
    # Assuming Tuleap exposes an agile endpoints. If not, this acts as the intended interface 
    # to be refined based on exact Tuleap REST API schemas.
    return await client.get(f"/projects/{project_id}/agile/epics")

async def get_user_stories(client: TuleapClient, project_id: int, epic_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get user stories for a project, optionally filtered by Epic."""
    params = {}
    if epic_id:
        params["epic_id"] = epic_id
    return await client.get(f"/projects/{project_id}/agile/user_stories", params=params)
