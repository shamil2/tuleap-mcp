import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.users import get_users

@pytest.mark.asyncio
async def test_get_users():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 1, "username": "jdoe"}]
    
    result = await get_users(mock_client, query="jdoe")
    
    mock_client.get.assert_called_once_with("/users", params={"query": "jdoe"})
    assert result == [{"id": 1, "username": "jdoe"}]
