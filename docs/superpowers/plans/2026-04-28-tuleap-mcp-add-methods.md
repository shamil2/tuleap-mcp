# Tuleap MCP Server: Methods Addition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and expose `update_artifact` and `create_user_story` methods in the Tuleap MCP Server.

**Architecture:** Extend existing modular tool structure. `update_artifact` is already implemented in `trackers.py` but needs exposing in `server.py`. `create_user_story` needs implementation in `agile.py` leveraging existing tracker ID lookup logic, and then exposing in `server.py`. Tests will be added for both.

**Tech Stack:** Python, `mcp` (FastMCP), `pytest`, `pytest-asyncio`

---

### Task 1: Expose `update_artifact` tool

**Files:**
- Modify: `src/tuleap_mcp/server.py`
- Modify: `tests/test_trackers.py`

- [ ] **Step 1: Write the failing test for `update_artifact`**
  Add a test to `tests/test_trackers.py` to ensure `trackers.update_artifact` works as expected. We need to mock the HTTP call.

```python
# add to tests/test_trackers.py
import pytest
from unittest.mock import AsyncMock, patch
from tuleap_mcp.tools import trackers
from tuleap_mcp.client import TuleapClient

@pytest.mark.asyncio
async def test_update_artifact():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = {"id": 123, "status": "updated"}
    
    values = [{"field_id": 1, "value": "New Title"}]
    comment = "Doing some work"
    
    result = await trackers.update_artifact(client_mock, 123, values, comment)
    
    client_mock.put.assert_called_once_with(
        "/artifacts/123", 
        json={"values": values, "comment": {"body": comment}}
    )
    assert result == {"id": 123, "status": "updated"}
```

- [ ] **Step 2: Run test to verify it passes (implementation already exists)**

Run: `pytest tests/test_trackers.py::test_update_artifact -v`
Expected: PASS (because the method is already in `src/tuleap_mcp/tools/trackers.py`)

- [ ] **Step 3: Write minimal implementation in server**
  Add the FastMCP tool wrapper in `src/tuleap_mcp/server.py` around the existing function.

```python
# add to src/tuleap_mcp/server.py, after get_artifact

@mcp.tool()
async def update_artifact(artifact_id: int, values: list = None, comment: str = None) -> str:
    """Update an artifact's fields or add a comment. Values should be a list of dictionaries with field updates. At least one of values or comment is required."""
    client = get_client()
    if not values and not comment:
        return "Error: Must provide either values or comment to update."
    if values is None:
        values = []
    return str(await trackers.update_artifact(client, artifact_id, values, comment))
```

- [ ] **Step 4: Commit**

```bash
git add tests/test_trackers.py src/tuleap_mcp/server.py
git commit -m "feat: expose update_artifact mcp tool"
```

### Task 2: Implement `create_user_story` tool

**Files:**
- Modify: `src/tuleap_mcp/tools/agile.py`
- Modify: `src/tuleap_mcp/server.py`
- Modify: `tests/test_agile.py`

- [ ] **Step 1: Write the failing test for `create_user_story`**
  Add a test to `tests/test_agile.py`.

```python
# add to tests/test_agile.py
import pytest
from unittest.mock import AsyncMock, patch
from tuleap_mcp.tools import agile
from tuleap_mcp.client import TuleapClient

@pytest.mark.asyncio
async def test_create_user_story():
    client_mock = AsyncMock(spec=TuleapClient)
    # Mock finding the tracker ID
    client_mock.get.return_value = [{"id": 42, "item_name": "User Story"}]
    # Mock creating the artifact
    client_mock.post.return_value = {"id": 99, "title": "New Story"}
    
    values = [{"field_id": 1, "value": "New Story"}]
    result = await agile.create_user_story(client_mock, project_id=1, values=values)
    
    client_mock.get.assert_called_once_with("/projects/1/trackers")
    client_mock.post.assert_called_once_with(
        "/trackers/42/artifacts", 
        json={"values": values}
    )
    assert result == {"id": 99, "title": "New Story"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_agile.py::test_create_user_story -v`
Expected: FAIL with AttributeError or similar since `create_user_story` isn't defined yet.

- [ ] **Step 3: Write minimal implementation in `agile.py`**
  Add the function to `src/tuleap_mcp/tools/agile.py`.

```python
# add to src/tuleap_mcp/tools/agile.py

async def create_user_story(
    client: TuleapClient, project_id: int, values: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a new user story artifact in a project."""
    tracker_id = await _get_tracker_id_by_name(client, project_id, "user stor")
    if not tracker_id:
        tracker_id = await _get_tracker_id_by_name(client, project_id, "story")
    if not tracker_id:
        raise Exception(
            f"Could not find a 'User Story' tracker in project {project_id}"
        )
        
    payload = {"values": values}
    return await client.post(f"/trackers/{tracker_id}/artifacts", json=payload)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_agile.py::test_create_user_story -v`
Expected: PASS

- [ ] **Step 5: Write minimal implementation in `server.py`**
  Expose the new function as an MCP tool.

```python
# add to src/tuleap_mcp/server.py, after get_project_user_stories

@mcp.tool()
async def create_user_story(project_id: int, values: list) -> str:
    """Create a new user story artifact in a project. Values should be a list of dictionaries defining the story fields."""
    client = get_client()
    return str(await agile.create_user_story(client, project_id, values))
```

- [ ] **Step 6: Commit**

```bash
git add src/tuleap_mcp/tools/agile.py src/tuleap_mcp/server.py tests/test_agile.py
git commit -m "feat: implement and expose create_user_story mcp tool"
```
