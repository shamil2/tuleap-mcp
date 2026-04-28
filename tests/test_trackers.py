import pytest
from unittest.mock import AsyncMock, patch
from tuleap_mcp.tools.trackers import get_artifact_details, search_artifacts, update_artifact
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_get_artifact_details():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 100, "title": "Bug"}

    result = await get_artifact_details(mock_client, artifact_id=100)

    mock_client.get.assert_called_once_with("/artifacts/100")
    assert result == {"id": 100, "title": "Bug"}


@pytest.mark.asyncio
async def test_search_artifacts():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 100}]

    result = await search_artifacts(mock_client, tracker_id=5, query="auth")

    mock_client.get.assert_called_once_with(
        "/artifacts", params={"tracker_id": 5, "query": "auth"}
    )
    assert result == [{"id": 100}]


@pytest.mark.asyncio
async def test_update_artifact():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = {"id": 123, "status": "updated"}

    values = [{"field_id": 1, "value": "New Title"}]
    comment = "Doing some work"

    result = await update_artifact(client_mock, 123, values, comment)

    client_mock.put.assert_called_once_with(
        "/artifacts/123", json={"values": values, "comment": {"body": comment}}
    )
    assert result == {"id": 123, "status": "updated"}
