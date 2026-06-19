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
    notes: str = ""

# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_recipe() -> dict:
    """Load the current recipe from disk."""
    if RECIPE_FILE.exists():
        return json.loads(RECIPE_FILE.read_text())
    return {}


def save_recipe(data: dict) -> dict:
    """Persist recipe data to disk and return the saved recipe.

    Normalizes fractions (e.g. "1/2" → "a half") in ingredients and directions
    so voice assistants read them naturally.
    """
    from parser import normalize_fractions

    # Normalize fractions in text fields before saving
    if "ingredients" in data and data["ingredients"]:
        data["ingredients"] = normalize_fractions(data["ingredients"])
    if "directions" in data and data["directions"]:
        data["directions"] = normalize_fractions(data["directions"])
    if "notes" in data and data["notes"]:
        data["notes"] = normalize_fractions(data["notes"])

    RECIPE_FILE.parent.mkdir(parents=True, exist_ok=True)
    RECIPE_FILE.write_text(json.dumps(data, indent=2))
    return load_recipe()


def import_recipe(text: str) -> dict:
    """Parse a plain-text recipe block and save it to disk."""
    from parser import parse_recipe_text
    parsed = parse_recipe_text(text)
    return save_recipe(parsed)
