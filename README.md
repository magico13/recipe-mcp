# Recipe Manager MCP Server

A FastMCP server built with FastAPI that serves a recipe editing web page and exposes recipe data via MCP tools. Designed for voice-assistant interaction — fractions like `1/2` and `1¼` are automatically normalized to `"a half"` and `"one and a quarter"` so they read naturally aloud.

## Features

- **Web UI** — Clean, responsive form with Edit and Import tabs at `/`
- **Recipe Import** — Paste plain-text recipe blocks and auto-parse into structured fields
- **Fraction Normalization** — `1/2`, `1¼`, `½` → `"a half"`, `"one and a quarter"`, `"a half"` on save
- **Notes Field** — Optional notes section for tips, substitutions, and comments
- **REST API** — `GET /api/get-recipe`, `POST /api/save-recipe`, `POST /api/import-recipe`
- **MCP Tools** — `get_recipe`, `save_recipe`, and `import_recipe` exposed at `/mcp/`
- **Persistent storage** — Recipes saved to `recipes.json` in a Docker named volume

## Quick Start

### Running with Docker (recommended)

```bash
bash run.sh
```

This rebuilds the image and starts the container on port **8002** with a named volume (`recipe-data`) for persistent storage and `--restart unless-stopped` for auto-recovery.

### Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

## Web UI

Open `http://localhost:8002` in your browser.

### Edit Tab

Four fields: **Recipe Name**, **Ingredients**, **Directions**, and **Notes**. Edit any field and click **Save Recipe** to persist changes. Fractions are normalized on save so voice assistants read them naturally.

![Edit Tab](docs/screenshots/edit-tab.jpg)

### Import Tab

Paste a plain-text recipe block and click **Parse & Save**. The parser extracts the title, ingredients, directions, and notes, then switches to the Edit tab so you can review before saving.

![Import Tab](docs/screenshots/import-tab.jpg)

**Expected format:**

```
Recipe Name Here

Ingredients:
1 1/2 cups flour
1/4 tsp salt
2 eggs

Directions:
Mix ingredients together.
Bake at 350°F for 25 minutes.

Notes:
Add vanilla extract for extra flavor.
```

The first line becomes the recipe title. Sections are identified by `Ingredients:`, `Directions:`, and `Notes:` headers (case-insensitive). Nutrition facts and source URLs are ignored.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI for editing and importing recipes |
| `/api/get-recipe` | GET | Get the current recipe as JSON |
| `/api/save-recipe` | POST | Save a recipe (JSON body with `name`, `ingredients`, `directions`, `notes`) |
| `/api/import-recipe` | POST | Import a plain-text recipe (JSON body with `text`) |
| `/mcp/` | POST | MCP Streamable HTTP transport endpoint |

## MCP Tools

- **`get_recipe`** — Retrieve the current recipe
- **`save_recipe`** — Save or update a recipe (params: `name`, `ingredients`, `directions`, `notes`)
- **`import_recipe`** — Parse and save a plain-text recipe block (param: `text`)

### Import via MCP example

```
import_recipe(text="Classic Pancakes\n\nIngredients:\n1 1/2 cups flour\n1/4 tsp salt\n\nDirections:\nMix and cook on a griddle.\n\nNotes:\nServe with maple syrup.")
```

## Fraction Normalization

On save, fractions in ingredients, directions, and notes are converted to voice-friendly words:

| Input | Output |
|-------|--------|
| `1/2 cup` | `a half cup` |
| `1 1/2 cups` | `one and a half cups` |
| `3/4 tsp` | `three quarters tsp` |
| `1¼ cups` | `one and a quarter cups` |
| `½ tsp` | `a half tsp` |
| `80/20 ground beef` | `80/20 ground beef` (unchanged) |

This ensures voice assistants read measurements naturally instead of saying "one slash two."

## Project Structure

```
recipe-mcp/
├── Dockerfile            # Container build definition
├── .dockerignore         # Docker build context exclusions
├── .gitignore            # Git exclusion rules
├── README.md             # This file
├── data.py               # Recipe I/O, Pydantic model, and import helper
├── mcp_server.py         # FastMCP tools definition
├── parser.py             # Plain-text recipe parser and fraction normalizer
├── requirements.txt      # Python dependencies
├── run.sh                # One-command rebuild + restart (port 8002)
├── sample_1.txt          # Sample recipe for testing import
├── sample_2.txt          # Sample recipe for testing import
├── server.py             # FastAPI app, routes, and entry point
└── templates/
    └── web_page.html     # Web UI template with Edit/Import tabs
```

Recipe data is persisted in a Docker named volume (`recipe-data`) and is not tracked by git.
