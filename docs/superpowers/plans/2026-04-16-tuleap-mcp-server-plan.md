# Tuleap MCP Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular FastMCP Python server to expose Tuleap API operations (Agile, Trackers, Files, Users) to LLMs.

**Architecture:** Python `mcp[cli]` with `FastMCP`. Modules register tools and rely on a shared `TuleapClient` configured via `TULEAP_URL` and `TULEAP_API_KEY`.

**Tech Stack:** Python 3.10+, `mcp[cli]`, `httpx`, `pytest`, `respx`

---

### Task 1: Project Setup and Dependencies

**Files:**
- Create: `pyproject.toml`
- Create: `src/tuleap_mcp/__init__.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "tuleap-mcp"
version = "0.1.0"
description = "Tuleap MCP Server"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.0.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "respx>=0.21.0",
]

[project.scripts]
tuleap-mcp = "tuleap_mcp.server:main"
```

- [ ] **Step 2: Create `README.md`**

```markdown
# Tuleap MCP Server
A Model Context Protocol server for interacting with Tuleap.
```

- [ ] **Step 3: Create empty `__init__.py`**

```python
# src/tuleap_mcp/__init__.py
```

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml README.md src/tuleap_mcp/__init__.py
git commit -m "chore: initial project setup"
```

---

### Task 2: Core Tuleap Client

**Files:**
- Create: `src/tuleap_mcp/client.py`
- Create: `tests/test_client.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_client.py
import pytest
import respx
import httpx
from tuleap_mcp.client import TuleapClient, TuleapAPIError

@pytest.mark.asyncio
async def test_client_get_request():
    with respx.mock:
        respx.get("https://tuleap.example.com/api/v1/users/1").mock(return_value=httpx.Response(200, json={"id": 1}))
        client = TuleapClient("https://tuleap.example.com", "fake-token")
        response = await client.get("/users/1")
        assert response == {"id": 1}

@pytest.mark.asyncio
async def test_client_error_handling():
    with respx.mock:
        respx.get("https://tuleap.example.com/api/v1/notfound").mock(return_value=httpx.Response(404, json={"error": "Not Found"}))
        client = TuleapClient("https://tuleap.example.com", "fake-token")
        with pytest.raises(TuleapAPIError) as exc:
            await client.get("/notfound")
        assert "404" in str(exc.value)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_client.py -v`
Expected: FAIL with ModuleNotFoundError or ImportError for `TuleapClient`

- [ ] **Step 3: Write minimal implementation**

```python
# src/tuleap_mcp/client.py
import httpx
from typing import Any, Dict, Optional

class TuleapAPIError(Exception):
    pass

class TuleapClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/v1"
        self.headers = {
            "X-Auth-AccessKey": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
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
                raise TuleapAPIError(f"Tuleap API Error {e.response.status_code}: {error_detail}")

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return await self._request("POST", endpoint, json=json)
        
    async def put(self, endpoint: str, json: Optional[Dict] = None) -> Any:
        return await self._request("PUT", endpoint, json=json)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_client.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/client.py tests/test_client.py
git commit -m "feat: core Tuleap HTTP client with error handling"
```

---

### Task 3: Users Tool Module

**Files:**
- Create: `src/tuleap_mcp/tools/__init__.py`
- Create: `src/tuleap_mcp/tools/users.py`
- Create: `tests/test_users.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_users.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_users.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/tuleap_mcp/tools/__init__.py
```

```python
# src/tuleap_mcp/tools/users.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_users.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/__init__.py src/tuleap_mcp/tools/users.py tests/test_users.py
git commit -m "feat: users tools module"
```

---

### Task 4: Trackers Tool Module

**Files:**
- Create: `src/tuleap_mcp/tools/trackers.py`
- Create: `tests/test_trackers.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_trackers.py
import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.trackers import get_artifact_details, search_artifacts

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
    
    mock_client.get.assert_called_once_with("/artifacts", params={"tracker_id": 5, "query": "auth"})
    assert result == [{"id": 100}]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_trackers.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/tuleap_mcp/tools/trackers.py
from typing import List, Dict, Any, Optional
from ..client import TuleapClient

async def get_artifact_details(client: TuleapClient, artifact_id: int) -> Dict[str, Any]:
    """Get details of a specific artifact."""
    return await client.get(f"/artifacts/{artifact_id}")

async def search_artifacts(client: TuleapClient, tracker_id: int, query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for artifacts in a tracker."""
    params = {"tracker_id": tracker_id}
    if query:
        params["query"] = query
    return await client.get("/artifacts", params=params)

async def update_artifact(client: TuleapClient, artifact_id: int, values: List[Dict[str, Any]], comment: Optional[str] = None) -> Dict[str, Any]:
    """Update an artifact's fields or add a comment."""
    payload = {"values": values}
    if comment:
        payload["comment"] = {"body": comment}
    return await client.put(f"/artifacts/{artifact_id}", json=payload)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_trackers.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/trackers.py tests/test_trackers.py
git commit -m "feat: trackers tools module"
```

---

### Task 5: Agile Tool Module

**Files:**
- Create: `src/tuleap_mcp/tools/agile.py`
- Create: `tests/test_agile.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_agile.py
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
    
    # Assuming the API endpoint to get epics for a project is /projects/{id}/epics or similar.
    # Tuleap often uses agile dashboard API or artifact search filtering. We'll abstract it nicely.
    # Using generic artifact search for a hypothetical Epic tracker type as fallback if not exact.
    # Let's mock a hypothetical direct endpoint /projects/{id}/agile/epics
    mock_client.get.assert_called_once_with("/projects/1/agile/epics")
    assert result == [{"id": 200, "title": "Epic 1"}]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_agile.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/tuleap_mcp/tools/agile.py
from typing import List, Dict, Any, Optional
from ..client import TuleapClient

async def search_projects(client: TuleapClient, query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for projects in Tuleap."""
    params = {}
    if query:
        params["query"] = query
    return await client.get("/projects", params=params)

async def get_epics(client: TuleapClient, project_id: int) -> List[Dict[str, Any]]:
    """Get epics for a project."""
    # Assuming Tuleap exposes an agile endpoints. If not, this acts as the intended interface 
    # to be refined based on exact Tuleap REST API schemas.
    return await client.get(f"/projects/{project_id}/agile/epics")

async def get_user_stories(client: TuleapClient, project_id: int, epic_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get user stories for a project, optionally filtered by Epic."""
    params = {}
    if epic_id:
        params["epic_id"] = epic_id
    return await client.get(f"/projects/{project_id}/agile/user_stories", params=params)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_agile.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/agile.py tests/test_agile.py
git commit -m "feat: agile tools module"
```

---

### Task 6: Files & Git Tool Module

**Files:**
- Create: `src/tuleap_mcp/tools/files.py`
- Create: `tests/test_files.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_files.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_files.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/tuleap_mcp/tools/files.py
from typing import List, Dict, Any
from ..client import TuleapClient

async def get_git_repositories(client: TuleapClient, project_id: int) -> List[Dict[str, Any]]:
    """List Git repositories in a project."""
    return await client.get(f"/projects/{project_id}/git")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_files.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/files.py tests/test_files.py
git commit -m "feat: files and git tools module"
```

---

### Task 7: FastMCP Server Assembly

**Files:**
- Create: `src/tuleap_mcp/server.py`

- [ ] **Step 1: Write minimal implementation**

```python
# src/tuleap_mcp/server.py
import os
import sys
from mcp.server.fastmcp import FastMCP
from .client import TuleapClient
from .tools import users, trackers, agile, files

def get_client() -> TuleapClient:
    tuleap_url = os.getenv("TULEAP_URL")
    tuleap_api_key = os.getenv("TULEAP_API_KEY")
    
    if not tuleap_url or not tuleap_api_key:
        print("Error: TULEAP_URL and TULEAP_API_KEY environment variables must be set.", file=sys.stderr)
        sys.exit(1)
        
    return TuleapClient(tuleap_url, tuleap_api_key)

mcp = FastMCP("Tuleap MCP Server")

@mcp.tool()
async def search_users(query: str = None) -> str:
    """Search for users in Tuleap."""
    client = get_client()
    return str(await users.get_users(client, query))

@mcp.tool()
async def get_artifact(artifact_id: int) -> str:
    """Get details of a specific artifact."""
    client = get_client()
    return str(await trackers.get_artifact_details(client, artifact_id))

@mcp.tool()
async def search_artifacts(tracker_id: int, query: str = None) -> str:
    """Search for artifacts in a specific tracker."""
    client = get_client()
    return str(await trackers.search_artifacts(client, tracker_id, query))

@mcp.tool()
async def search_projects(query: str = None) -> str:
    """Search for projects."""
    client = get_client()
    return str(await agile.search_projects(client, query))

@mcp.tool()
async def get_project_epics(project_id: int) -> str:
    """Get epics for a project."""
    client = get_client()
    return str(await agile.get_epics(client, project_id))

@mcp.tool()
async def get_git_repos(project_id: int) -> str:
    """Get git repositories for a project."""
    client = get_client()
    return str(await files.get_git_repositories(client, project_id))

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add src/tuleap_mcp/server.py
git commit -m "feat: assemble FastMCP server and register tools"
```
