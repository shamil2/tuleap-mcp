import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.agile import search_projects, get_epics

@pytest.mark.asyncio
async def test_search_projects():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 1, "shortname": "demo"}]
    
    result = await search_projects(mock_client, query="demo")
    
    mock_client.get.assert_called_once_with("/projects", params={"query": "demo"})
    assert result == [{"id": 1, "shortname": "demo"}]

@pytest.mark.asyncio
async def test_get_epics():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 200, "title": "Epic 1"}]
    
    result = await get_epics(mock_client, project_id=1)
    
    mock_client.get.assert_called_once_with("/projects/1/agile/epics")
    assert result == [{"id": 200, "title": "Epic 1"}]
