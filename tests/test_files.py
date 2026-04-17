import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.files import get_git_repositories


@pytest.mark.asyncio
async def test_get_git_repositories():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 10, "name": "backend"}]

    result = await get_git_repositories(mock_client, project_id=1)

    mock_client.get.assert_called_once_with("/projects/1/git")
    assert result == [{"id": 10, "name": "backend"}]
