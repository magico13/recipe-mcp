"""Recipe Manager MCP Server.

A FastMCP server with FastAPI that serves a recipe editing web page
and exposes recipe data via MCP tools. Recipes are stored in recipes.json.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastmcp.utilities.lifespan import combine_lifespans

from data import RECIPE_FILE, RecipeInput, load_recipe, save_recipe
from mcp_server import mcp

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Ensure the data directory exists on startup
    RECIPE_FILE.parent.mkdir(parents=True, exist_ok=True)
    yield


# Create MCP ASGI app (path="/" since we mount at /mcp)
mcp_app = mcp.http_app(path="/")

app = FastAPI(
    title="Recipe Manager",
    lifespan=combine_lifespans(app_lifespan, mcp_app.lifespan),
)

# Mount MCP at /mcp
app.mount("/mcp", mcp_app)


# ---------------------------------------------------------------------------
# REST endpoints (used by the web UI)
# ---------------------------------------------------------------------------
@app.get("/api/get-recipe")
async def api_get_recipe():
    return load_recipe()


@app.post("/api/save-recipe")
async def api_save_recipe(recipe: RecipeInput):
    return save_recipe(recipe.model_dump())


# ---------------------------------------------------------------------------
# Web UI
# ---------------------------------------------------------------------------
WEB_PAGE_TEMPLATE = Path(__file__).parent / "templates" / "web_page.html"


@app.get("/", response_class=HTMLResponse)
async def web_ui():
    return WEB_PAGE_TEMPLATE.read_text()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
