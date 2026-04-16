# Tuleap MCP Server

A Model Context Protocol (MCP) server for interacting with [Tuleap](https://tuleap.net/), enabling AI assistants to read and manage Agile projects, artifacts, Git repositories, and users.

## Features

Exposes various Tuleap domains to your AI assistant:
- **Agile & Projects**: Search projects, retrieve Epics, and list User Stories.
- **Trackers & Artifacts**: Search for specific artifacts and get rich details (fields, status, dates).
- **Files & Repositories**: List Git repositories linked to a project.
- **Users**: Search for Tuleap users by name or email.

## Prerequisites

- Python 3.10 or higher
- A Tuleap instance URL
- A Tuleap Personal Access Token (API Key)

## Installation

1. Clone the repository (or navigate to this directory):
   ```bash
   cd tuleap_mcp
   ```
2. Create a virtual environment and install the package:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

## Configuration

The server requires the following environment variables to authenticate with your Tuleap instance:

- `TULEAP_URL`: The base URL of your Tuleap instance (e.g., `https://tuleap.example.com`)
- `TULEAP_API_KEY`: Your Tuleap Personal Access Token.

## Usage with Claude Desktop

To use this MCP server with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "tuleap": {
      "command": "/path/to/tuleap_mcp/.venv/bin/tuleap-mcp",
      "env": {
        "TULEAP_URL": "https://your-tuleap-instance.com",
        "TULEAP_API_KEY": "your-tuleap-api-key"
      }
    }
  }
}
```
*Note: Replace `/path/to/tuleap_mcp` with the absolute path to your local repository.*

## Available Tools

- `search_projects(query)`: Search for projects.
- `get_project_epics(project_id)`: Retrieve epics for a specific project.
- `get_project_user_stories(project_id, epic_id)`: Retrieve user stories for a project, optionally filtered by an Epic.
- `search_artifacts(tracker_id, query)`: Search for artifacts within a specific tracker.
- `get_artifact(artifact_id)`: Get detailed information about a specific artifact.
- `search_users(query)`: Search for Tuleap users.
- `get_git_repos(project_id)`: Get git repositories for a project.

## Development

To set up the development environment and run tests:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```
