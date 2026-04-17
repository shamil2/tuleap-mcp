import httpx
from typing import Any, Dict, Optional


class TuleapAPIError(Exception):
    pass


class TuleapClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v1"
        self.headers = {
            "X-Auth-AccessKey": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.api_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, **kwargs)
            try:
                response.raise_for_status()
                # 204 No Content has no JSON body
                if response.status_code == 204:
                    return None
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.text
                try:
                    error_detail = e.response.json()
                except ValueError:
                    pass
                raise TuleapAPIError(
                    f"Tuleap API Error {e.response.status_code}: {error_detail}"
                )

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return await self._request("POST", endpoint, json=json)

    async def put(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return await self._request("PUT", endpoint, json=json)
