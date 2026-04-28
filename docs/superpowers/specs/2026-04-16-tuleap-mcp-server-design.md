# Tuleap MCP Server Design

## Goal
Build a Model Context Protocol (MCP) server for Tuleap to allow AI assistants to interact with Tuleap workspaces.

## Scope
The user has specified the following key domains to expose:
- Trackers & Artifacts
- Files & Repositories
- Users & Groups
- Agile & Planning (Specifically: Project Management, Epics Management, User Stories Management)

## Architecture
**Language & Framework**: Python using the official `mcp` SDK with `FastMCP` for a modular, decorator-based routing system.
**HTTP Client**: `httpx` for making asynchronous REST API calls to the Tuleap instance.
**Authentication**: Personal Access Token (PAT) passed via environment variables, specifically `TULEAP_URL` and `TULEAP_API_KEY`.

## Project Structure
```text
tuleap-mcp/
├── pyproject.toml
├── src/
│   └── tuleap_mcp/
│       ├── __init__.py
│       ├── server.py        # FastMCP instance and entry point
│       ├── client.py        # TuleapClient encapsulating httpx calls and auth
│       └── tools/           # Modularized tool definitions
│           ├── __init__.py
│           ├── trackers.py  # Generic artifact and tracker operations
│           ├── agile.py     # Agile-specific operations (Projects, Epics, Stories)
│           ├── files.py     # Git repos, SVN, and documents
│           └── users.py     # Users and groups
```

## Data Flow
1. The MCP client (e.g. Claude Desktop) calls an MCP tool (e.g., `get_epic_details`).
2. The `FastMCP` router in `server.py` dispatches the call to the appropriate function in `tools/agile.py`.
3. The tool function uses the injected `TuleapClient` to make an HTTP request to `https://<TULEAP_URL>/api/v1/...` with the `X-Auth-AccessKey` header.
4. The client parses the JSON response and handles API errors (401, 404, 500).
5. The tool function formats the response back to the MCP client as a string or structured data.

## Tool Definitions

### Agile & Project Management (`agile.py`)
- `search_projects`: Find projects by name or ID.
- `get_epics`: List epics within a project (filtering artifacts by Epic tracker).
- `get_user_stories`: List user stories linked to a specific epic or project.
- `create_user_story`: Create a new user story artifact.

### Trackers & Artifacts (`trackers.py`)
- `search_artifacts`: Search for generic artifacts across trackers.
- `get_artifact_details`: Get full details of an artifact (comments, changes, fields).
- `update_artifact`: Update fields or add a comment to an artifact.

### Files & Repositories (`files.py`)
- `get_git_repositories`: List Git repositories in a project.

### Users & Groups (`users.py`)
- `get_users`: Search for users by username or email.

## Testing Strategy
- Unit tests for the `TuleapClient` using `pytest` and `respx` to mock HTTP responses.
- Integration test script that uses the MCP SDK to connect to the local server via standard I/O and verify tool execution.

## Error Handling
- `TuleapClient` will raise domain-specific exceptions (e.g., `TuleapAuthError`, `TuleapNotFoundError`).
- These exceptions will be caught by the FastMCP tool handlers and returned as readable error messages to the LLM to allow it to recover or inform the user.
