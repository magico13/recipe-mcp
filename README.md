# Recipe Manager MCP Server

A FastMCP server built with FastAPI that serves a recipe editing web page and exposes recipe data via MCP tools. Recipes are stored in a JSON file.

## Features

- **Web UI** — Clean, responsive form for editing recipes at `/`
- **REST API** — `GET /api/get-recipe` and `POST /api/save-recipe`
- **MCP Tools** — `get_recipe` and `save_recipe` exposed at `/mcp/`
- **Persistent storage** — Recipes saved to `recipes.json`

## Quick Start

### Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

### Running with Docker

```bash
docker build -t recipe-mcp .
docker run -d --name recipe-mcp-server -p 8000:8000 --rm recipe-mcp
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI for editing recipes |
| `/api/get-recipe` | GET | Get the current recipe as JSON |
| `/api/save-recipe` | POST | Save a recipe (JSON body with `name`, `ingredients`, `directions`) |
| `/mcp/` | POST | MCP Streamable HTTP transport endpoint |

## MCP Tools

- **`get_recipe`** — Retrieve the current recipe
- **`save_recipe`** — Save or update a recipe (params: `name`, `ingredients`, `directions`)

## Project Structure

```
recipe-mcp/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── data.py             # Recipe I/O and Pydantic model
├── mcp_server.py       # FastMCP tools definition
├── requirements.txt    # Python dependencies
├── run.sh              # One-command rebuild + restart
├── server.py           # FastAPI app, routes, and entry point
└── templates/
    └── web_page.html   # Web UI template
```

Recipe data is persisted in a Docker named volume (`recipe-data`) and is not tracked by git.
