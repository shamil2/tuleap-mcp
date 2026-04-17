from typing import List, Dict, Any, Optional
from ..client import TuleapClient


async def get_artifact_details(
    client: TuleapClient, artifact_id: int
) -> Dict[str, Any]:
    """Get details of a specific artifact."""
    return await client.get(f"/artifacts/{artifact_id}")


async def search_artifacts(
    client: TuleapClient, tracker_id: int, query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for artifacts in a tracker."""
    params = {"tracker_id": tracker_id}
    if query:
        params["query"] = query
    return await client.get("/artifacts", params=params)


async def update_artifact(
    client: TuleapClient,
    artifact_id: int,
    values: List[Dict[str, Any]],
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an artifact's fields or add a comment."""
    payload = {"values": values}
    if comment:
        payload["comment"] = {"body": comment}
    return await client.put(f"/artifacts/{artifact_id}", json=payload)
