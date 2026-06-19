"""Data layer for recipe storage.

Handles reading/writing recipes to a JSON file and provides
the Pydantic model used by the REST endpoints.
"""

import json
from pathlib import Path

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
RECIPE_FILE = Path("/data/recipes.json")

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class RecipeInput(BaseModel):
    name: str
    ingredients: str
    directions: str

# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_recipe() -> dict:
    """Load the current recipe from disk."""
    if RECIPE_FILE.exists():
        return json.loads(RECIPE_FILE.read_text())
    return {}


def save_recipe(data: dict) -> dict:
    """Persist recipe data to disk and return the saved recipe."""
    RECIPE_FILE.parent.mkdir(parents=True, exist_ok=True)
    RECIPE_FILE.write_text(json.dumps(data, indent=2))
    return load_recipe()
