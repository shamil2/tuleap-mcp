# Tuleap MCP Server: Epic Management Methods Design

## Goal
Expand the Agile domain of the Tuleap MCP Server by adding methods for comprehensive Epic management: creating epics, linking artifacts to epics, and retrieving epic progress.

## Scope
- **Create Epic**: A new tool to create Epic artifacts within a specified project.
- **Link Epic**: A new tool to link an existing child artifact (like a User Story) to a parent Epic.
- **Epic Progress**: A new tool to retrieve a summarized view of an Epic's status and progress.

## Architecture

**Framework**: `mcp` SDK with `FastMCP`
**HTTP Client**: Injected `TuleapClient`
**Module**: `src/tuleap_mcp/tools/agile.py` (for creation and progress) and `server.py` (for MCP routing).

### Tool Definitions

1.  **`create_epic(project_id: int, values: list)`**
    *   **Logic**: Use the existing `_get_tracker_id_by_name` helper to locate the "Epic" tracker for the `project_id`. Then, make a `POST /trackers/{tracker_id}/artifacts` request with the provided `values`.
    *   **Module**: `agile.py`

2.  **`link_to_epic(epic_id: int, child_artifact_id: int)`**
    *   **Logic**: In Tuleap, linking is typically done by setting the `parent_id` field on the child artifact. We will make a `PUT /artifacts/{child_artifact_id}` request, updating the artifact's values to set its parent to `epic_id`. We will also add a comment indicating the link was made via the MCP server.
    *   **Module**: `agile.py`

3.  **`get_epic_progress(epic_id: int)`**
    *   **Logic**: Make a `GET /artifacts/{epic_id}` request. Instead of returning the raw artifact, this function will parse the `values` array and return a summarized dictionary containing key progress indicators (e.g., Status, Progress, Remaining Effort, Total Effort).
    *   **Module**: `agile.py`

## Error Handling
- Use the existing error handling mechanisms.
- If the "Epic" tracker cannot be found in a project, raise an exception indicating this so the LLM knows why the operation failed.

## Testing Strategy
- Unit tests in `tests/test_agile.py` using `pytest` and `unittest.mock.AsyncMock`.
- Mock the `TuleapClient` to ensure no live API calls are made during the test suite.
- Verify that the correct endpoint URIs and JSON payloads are constructed.
