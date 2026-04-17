from typing import List, Dict, Any
from ..client import TuleapClient


async def get_git_repositories(
    client: TuleapClient, project_id: int
) -> List[Dict[str, Any]]:
    """List Git repositories in a project."""
    return await client.get(f"/projects/{project_id}/git")
