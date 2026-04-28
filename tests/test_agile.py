import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.agile import search_projects, get_epics, get_user_stories


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

    async def mock_get(endpoint, **kwargs):
        if "trackers" in endpoint and "projects" in endpoint:
            return [{"id": 15, "name": "Epics"}]
        return [{"id": 200, "title": "Epic 1"}]

    mock_client.get.side_effect = mock_get

    result = await get_epics(mock_client, project_id=1)

    assert result == [{"id": 200, "title": "Epic 1"}]


@pytest.mark.asyncio
async def test_get_user_stories():
    mock_client = AsyncMock()

    async def mock_get(endpoint, **kwargs):
        if "trackers" in endpoint and "projects" in endpoint:
            return [{"id": 20, "name": "User Stories"}]
        return [{"id": 300, "title": "Story 1"}]

    mock_client.get.side_effect = mock_get

    result = await get_user_stories(mock_client, project_id=1, epic_id=200)

    assert result == [{"id": 300, "title": "Story 1"}]


@pytest.mark.asyncio
async def test_create_user_story():
    client_mock = AsyncMock()
    # Mock finding the tracker ID
    client_mock.get.return_value = [{"id": 42, "item_name": "User Story"}]
    # Mock creating the artifact
    client_mock.post.return_value = {"id": 99, "title": "New Story"}
    
    values = [{"field_id": 1, "value": "New Story"}]
    # Note: agile module will be imported, but we'll import create_user_story directly or use agile.create_user_story
    from tuleap_mcp.tools import agile
    result = await agile.create_user_story(client_mock, project_id=1, values=values)
    
    client_mock.get.assert_called_once_with("/projects/1/trackers")
    client_mock.post.assert_called_once_with(
        "/trackers/42/artifacts", 
        json={"values": values}
    )
    assert result == {"id": 99, "title": "New Story"}
