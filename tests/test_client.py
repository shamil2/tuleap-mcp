import pytest
import respx
import httpx
from tuleap_mcp.client import TuleapClient, TuleapAPIError


@pytest.mark.asyncio
async def test_client_get_request():
    with respx.mock:
        respx.get("https://tuleap.example.com/api/v1/users/1").mock(
            return_value=httpx.Response(200, json={"id": 1})
        )
        client = TuleapClient("https://tuleap.example.com", "fake-token")
        response = await client.get("/users/1")
        assert response == {"id": 1}


@pytest.mark.asyncio
async def test_client_error_handling():
    with respx.mock:
        respx.get("https://tuleap.example.com/api/v1/notfound").mock(
            return_value=httpx.Response(404, json={"error": "Not Found"})
        )
        client = TuleapClient("https://tuleap.example.com", "fake-token")
        with pytest.raises(TuleapAPIError) as exc:
            await client.get("/notfound")
        assert "404" in str(exc.value)
