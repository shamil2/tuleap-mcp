from typing import List, Dict, Any, Optional
from ..client import TuleapClient


async def search_projects(
    client: TuleapClient, query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for projects in Tuleap."""
    params = {}
    if query:
        params["query"] = query
    return await client.get("/projects", params=params)


async def _get_tracker_id_by_name(
    client: TuleapClient, project_id: int, tracker_name: str
) -> Optional[int]:
    """Helper to find a tracker ID by its name within a project."""
    trackers = await client.get(f"/projects/{project_id}/trackers")
    for t in trackers:
        # Match names like "Epic", "Epics", "User Story", "User Stories"
        if (
            tracker_name.lower() in t.get("item_name", "").lower()
            or tracker_name.lower() in t.get("name", "").lower()
            or t.get("shortname", "").lower() == tracker_name.lower()
        ):
            return t.get("id")
    return None


async def _get_epic_tracker_id(client: TuleapClient, project_id: int) -> int:
    """Helper to find the Epic tracker ID for a project."""
    tracker_id = await _get_tracker_id_by_name(client, project_id, "epic")
    if not tracker_id:
        raise Exception(f"Could not find an 'Epic' tracker in project {project_id}")
    return tracker_id

async def get_epics(client: TuleapClient, project_id: int) -> List[Dict[str, Any]]:
    """Get epics for a project. Returns the artifacts from the Epic tracker."""
    tracker_id = await _get_epic_tracker_id(client, project_id)
    return await client.get(f"/trackers/{tracker_id}/artifacts")

async def create_epic(
    client: TuleapClient, project_id: int, values: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a new epic artifact in a project."""
    tracker_id = await _get_epic_tracker_id(client, project_id)
    payload = {"values": values}
    return await client.post(f"/trackers/{tracker_id}/artifacts", json=payload)


async def _get_user_story_tracker_id(client: TuleapClient, project_id: int) -> int:
    tracker_id = await _get_tracker_id_by_name(client, project_id, "user stor")
    if not tracker_id:
        tracker_id = await _get_tracker_id_by_name(client, project_id, "story")
    if not tracker_id:
        raise Exception(
            f"Could not find a 'User Story' tracker in project {project_id}"
        )
    return tracker_id


async def get_user_stories(
    client: TuleapClient, project_id: int, epic_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get user stories for a project, optionally filtered by Epic parent."""
    tracker_id = await _get_user_story_tracker_id(client, project_id)

    # If epic_id is provided, we can use TQL to filter (query=parent_id=...)
    params = {}
    if epic_id:
        params["query"] = f"parent_id={epic_id}"

    return await client.get(f"/trackers/{tracker_id}/artifacts", params=params)


async def create_user_story(
    client: TuleapClient, project_id: int, values: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a new user story artifact in a project."""
    tracker_id = await _get_user_story_tracker_id(client, project_id)

    payload = {"values": values}
    return await client.post(f"/trackers/{tracker_id}/artifacts", json=payload)
