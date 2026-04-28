# Epic Management Methods Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and expose `create_epic`, `link_to_epic`, and `get_epic_progress` methods in the Tuleap MCP Server.

**Architecture:** Extend the `agile.py` module with new functions. Refactor tracker ID lookup into helpers. Expose new functions as FastMCP tools in `server.py`.

**Tech Stack:** Python, `mcp` (FastMCP), `pytest`, `pytest-asyncio`

---

### Task 1: Refactor and Implement `create_epic`

**Files:**
- Modify: `src/tuleap_mcp/tools/agile.py`
- Modify: `tests/test_agile.py`

- [ ] **Step 1: Write the failing test for `create_epic`**
  Add a test to `tests/test_agile.py`.

```python
# add to tests/test_agile.py

@pytest.mark.asyncio
async def test_create_epic():
    client_mock = AsyncMock()
    # Mock finding the tracker ID
    client_mock.get.return_value = [{"id": 15, "name": "Epics"}]
    # Mock creating the artifact
    client_mock.post.return_value = {"id": 101, "title": "Big Feature"}
    
    values = [{"field_id": 1, "value": "Big Feature"}]
    result = await agile.create_epic(client_mock, project_id=1, values=values)
    
    client_mock.get.assert_called_once_with("/projects/1/trackers")
    client_mock.post.assert_called_once_with(
        "/trackers/15/artifacts", 
        json={"values": values}
    )
    assert result == {"id": 101, "title": "Big Feature"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_agile.py::test_create_epic -v`
Expected: FAIL with AttributeError

- [ ] **Step 3: Refactor and implement in `agile.py`**
  Extract `_get_epic_tracker_id` and add `create_epic`.

```python
# add to src/tuleap_mcp/tools/agile.py

async def _get_epic_tracker_id(client: TuleapClient, project_id: int) -> int:
    """Helper to find the Epic tracker ID for a project."""
    tracker_id = await _get_tracker_id_by_name(client, project_id, "epic")
    if not tracker_id:
        raise Exception(f"Could not find an 'Epic' tracker in project {project_id}")
    return tracker_id

async def create_epic(
    client: TuleapClient, project_id: int, values: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a new epic artifact in a project."""
    tracker_id = await _get_epic_tracker_id(client, project_id)
    payload = {"values": values}
    return await client.post(f"/trackers/{tracker_id}/artifacts", json=payload)
```

- [ ] **Step 4: Update `get_epics` to use the new helper**

```python
# update in src/tuleap_mcp/tools/agile.py

async def get_epics(client: TuleapClient, project_id: int) -> List[Dict[str, Any]]:
    """Get epics for a project. Returns the artifacts from the Epic tracker."""
    tracker_id = await _get_epic_tracker_id(client, project_id)
    return await client.get(f"/trackers/{tracker_id}/artifacts")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `PYTHONPATH=src pytest tests/test_agile.py -v`
Expected: ALL PASS

- [ ] **Step 6: Commit**

```bash
git add src/tuleap_mcp/tools/agile.py tests/test_agile.py
git commit -m "feat: implement create_epic and refactor epic tracker lookup"
```

### Task 2: Implement `link_to_epic`

**Files:**
- Modify: `src/tuleap_mcp/tools/agile.py`
- Modify: `tests/test_agile.py`

- [ ] **Step 1: Write the failing test for `link_to_epic`**

```python
# add to tests/test_agile.py

@pytest.mark.asyncio
async def test_link_to_epic():
    client_mock = AsyncMock()
    client_mock.put.return_value = {"id": 200, "parent_id": 101}
    
    result = await agile.link_to_epic(client_mock, epic_id=101, child_artifact_id=200)
    
    expected_payload = {
        "values": [{"field_id": "parent_id", "value": 101}],
        "comment": {"body": "Linked to Epic #101 via MCP Server"}
    }
    client_mock.put.assert_called_once_with("/artifacts/200", json=expected_payload)
    assert result == {"id": 200, "parent_id": 101}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_agile.py::test_link_to_epic -v`
Expected: FAIL

- [ ] **Step 3: Implement `link_to_epic` in `agile.py`**

```python
# add to src/tuleap_mcp/tools/agile.py

async def link_to_epic(
    client: TuleapClient, epic_id: int, child_artifact_id: int
) -> Dict[str, Any]:
    """Link a child artifact to a parent epic."""
    payload = {
        "values": [{"field_id": "parent_id", "value": epic_id}],
        "comment": {"body": f"Linked to Epic #{epic_id} via MCP Server"}
    }
    return await client.put(f"/artifacts/{child_artifact_id}", json=payload)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_agile.py::test_link_to_epic -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/agile.py tests/test_agile.py
git commit -m "feat: implement link_to_epic"
```

### Task 3: Implement `get_epic_progress`

**Files:**
- Modify: `src/tuleap_mcp/tools/agile.py`
- Modify: `tests/test_agile.py`

- [ ] **Step 1: Write the failing test for `get_epic_progress`**

```python
# add to tests/test_agile.py

@pytest.mark.asyncio
async def test_get_epic_progress():
    client_mock = AsyncMock()
    client_mock.get.return_value = {
        "id": 101,
        "values": [
            {"label": "Status", "value": "Open"},
            {"label": "Progress", "value": 45},
            {"label": "Remaining Effort", "value": 10},
            {"label": "Total Effort", "value": 22}
        ]
    }
    
    result = await agile.get_epic_progress(client_mock, epic_id=101)
    
    assert result["id"] == 101
    assert result["Status"] == "Open"
    assert result["Progress"] == 45
    assert result["Remaining Effort"] == 10
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_agile.py::test_get_epic_progress -v`
Expected: FAIL

- [ ] **Step 3: Implement `get_epic_progress` in `agile.py`**

```python
# add to src/tuleap_mcp/tools/agile.py

async def get_epic_progress(client: TuleapClient, epic_id: int) -> Dict[str, Any]:
    """Get summarized progress information for an epic."""
    artifact = await client.get(f"/artifacts/{epic_id}")
    summary = {"id": artifact.get("id")}
    
    # Extract relevant fields from values array
    for v in artifact.get("values", []):
        label = v.get("label")
        if label in ["Status", "Progress", "Remaining Effort", "Total Effort"]:
            summary[label] = v.get("value")
            
    return summary
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_agile.py::test_get_epic_progress -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tuleap_mcp/tools/agile.py tests/test_agile.py
git commit -m "feat: implement get_epic_progress summary"
```

### Task 4: Expose tools in `server.py`

**Files:**
- Modify: `src/tuleap_mcp/server.py`

- [ ] **Step 1: Add new tool wrappers to `server.py`**

```python
# add to src/tuleap_mcp/server.py

@mcp.tool()
async def create_epic(project_id: int, values: list) -> str:
    """Create a new epic artifact in a project."""
    client = get_client()
    return str(await agile.create_epic(client, project_id, values))


@mcp.tool()
async def link_to_epic(epic_id: int, child_artifact_id: int) -> str:
    """Link a child artifact (e.g. User Story) to a parent epic."""
    client = get_client()
    return str(await agile.link_to_epic(client, epic_id, child_artifact_id))


@mcp.tool()
async def get_epic_progress(epic_id: int) -> str:
    """Get summarized progress information for an epic (Status, Progress, Effort)."""
    client = get_client()
    return str(await agile.get_epic_progress(client, epic_id))
```

- [ ] **Step 2: Run all tests**

Run: `PYTHONPATH=src .venv/bin/pytest tests/`
Expected: ALL PASS

- [ ] **Step 3: Commit**

```bash
git add src/tuleap_mcp/server.py
git commit -m "feat: expose new epic management tools in MCP server"
```
