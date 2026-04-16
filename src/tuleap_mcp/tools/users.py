from typing import List, Dict, Any, Optional
from ..client import TuleapClient

async def get_users(client: TuleapClient, query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for users in Tuleap.
    
    Args:
        client: The TuleapClient instance
        query: Optional search term (username, email, real name)
    """
    params = {}
    if query:
        params["query"] = query
    return await client.get("/users", params=params)
