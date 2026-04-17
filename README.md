# Tuleap MCP Server

[![CI](https://github.com/shamilghaseeta/tuleap_mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/shamilghaseeta/tuleap_mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A secure, fully-tested **Model Context Protocol (MCP)** server for interacting with [Tuleap](https://tuleap.net/). This allows your favorite AI assistants (Claude, OpenCode, Cursor, Gemini, etc.) to safely read and manage your Agile projects, track artifacts, list Git repositories, and query users directly from your IDE or chat interface.

---

## 🌟 Features

Exposes the following Tuleap domains to your AI assistant:
- **Agile & Projects**: Search projects, retrieve Epics, and list User Stories.
- **Trackers & Artifacts**: Search for specific artifacts and get rich details (status, assigned to, dates, custom fields).
- **Files & Repositories**: List Git repositories linked to a project.
- **Users**: Search for Tuleap users by name or email.

## 🔐 Security & Best Practices

- **Zero Hardcoded Secrets**: Tokens are passed strictly via your local environment variables.
- **No Personal Data Logging**: The server acts purely as a conduit and does not cache or log your Tuleap data.
- **Automated Security Scans**: CI pipelines run `bandit` to ensure no common vulnerabilities are introduced.
- **Test-Driven**: Comprehensive tests with `pytest` and `respx` ensure data is mocked accurately without hitting live environments.

## 📦 Prerequisites & Installation

1. **Prerequisites**:
   - Python 3.10 or higher.
   - A Tuleap instance URL.
   - A Tuleap Personal Access Token (API Key) generated via the Tuleap user settings.

2. **Clone & Setup**:
   ```bash
   git clone https://github.com/your-username/tuleap_mcp.git
   cd tuleap_mcp
   
   # Create a virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install the package
   pip install -e .
   ```

3. **Verify Executable Path**:
   Once installed, the MCP binary will be located at:
   `/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp`

---

## 🚀 Configuration & Usage

Configure your AI assistant by pointing it to the virtual environment's executable.

### Using with Claude Desktop

Add this to your `claude_desktop_config.json` file (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "tuleap": {
      "command": "/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp",
      "env": {
        "TULEAP_URL": "https://your-tuleap-instance.com",
        "TULEAP_API_KEY": "your-tuleap-api-key"
      }
    }
  }
}
```

### Using with OpenCode

Add the server under the `mcp` block in your `~/.config/opencode/opencode.json`. Note that OpenCode uses `environment` instead of `env`, requires `type: local`, and uses a list for the `command`:

```json
{
  "mcp": {
    "tuleap": {
      "type": "local",
      "command": [
        "/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp"
      ],
      "environment": {
        "TULEAP_URL": "https://your-tuleap-instance.com",
        "TULEAP_API_KEY": "your-tuleap-api-key"
      },
      "enabled": true
    }
  }
}
```

### Using with OpenAI / ChatGPT
Currently, ChatGPT does not support running local MCP servers natively. However, you can use frameworks like [LangChain](https://github.com/hwchase17/langchain) or [LlamaIndex](https://github.com/jerryjliu/llama_index) to bridge this server to an OpenAI model in a custom Python script.

### Using with Gemini / Cursor / Zed
Most modern AI IDEs that support the official MCP spec configure servers similarly to Claude Desktop. Point their MCP settings menu to the full path of `.venv/bin/tuleap-mcp` and inject the `TULEAP_URL` and `TULEAP_API_KEY` environment variables.

---

## 🛠️ Available MCP Tools

Once connected, your AI assistant can use the following tools natively:
- `search_projects(query)`: Find Tuleap projects.
- `get_project_epics(project_id)`: Retrieve epics for a project via the Epic tracker.
- `get_project_user_stories(project_id, epic_id)`: Retrieve user stories for a project, optionally filtering by parent Epic.
- `search_artifacts(tracker_id, query)`: Search for generic artifacts using TQL queries or keywords.
- `get_artifact(artifact_id)`: Get deep metadata and fields for a specific artifact.
- `search_users(query)`: Search for Tuleap users.
- `get_git_repos(project_id)`: Fetch a list of git repositories linked to a project.

---

## 👨‍💻 Development & Contributing

We welcome contributions! To set up the development environment, run tests, and format code:

```bash
# Activate your venv
source .venv/bin/activate

# Install dev dependencies (pytest, ruff, bandit, etc.)
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=src/tuleap_mcp tests/

# Run linter and formatter
ruff check .
ruff format .

# Run security checks
bandit -r src/
```

### CI/CD Pipeline
Every Pull Request runs a GitHub Actions workflow (`.github/workflows/ci.yml`) ensuring:
1. All unit tests pass.
2. Code follows the Ruff formatting rules.
3. Bandit flags no common security issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
