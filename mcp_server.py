"""MCP server definition.

Exposes get_recipe and save_recipe as MCP tools.
"""

from fastmcp import FastMCP

from data import load_recipe, save_recipe, import_recipe

# ---------------------------------------------------------------------------
# FastMCP instance
# ---------------------------------------------------------------------------
mcp = FastMCP("Recipe Manager")


@mcp.tool
def get_recipe() -> dict:
    """Retrieve the current recipe with name, ingredients, and directions."""
    return load_recipe()


@mcp.tool(name="save_recipe")
def save_recipe_mcp(name: str, ingredients: str, directions: str, notes: str = "") -> dict:
    """Save or update the recipe with the given name, ingredients, and directions."""
    return save_recipe({"name": name, "ingredients": ingredients, "directions": directions, "notes": notes})


@mcp.tool
def import_recipe_tool(text: str) -> dict:
    """Parse a plain-text recipe block and save it. The first line should be the recipe title. Accepts recipe text with Ingredients:, Directions:, and optional Notes: sections."""
    return import_recipe(text)
