"""Recipe text parser.

Parses plain-text recipe blocks (like those exported from recipe-manager
apps) into structured dicts with name, ingredients, directions, and notes.

Recognised section headers (case-insensitive):
  Ingredients:, Directions:, Notes:, Nutrition:, Source:

Everything before "Ingredients:" is treated as title/meta. The first
non-empty line becomes the recipe name.
Between "Ingredients:" and "Directions:" is the ingredients block.
Between "Directions:" and the next recognised header (or EOF) is the
directions block.
A "Notes:" section is captured as a separate notes field.
Nutrition and source lines are dropped.
"""

import re


# Section headers we recognise (order matters – first match wins)
SECTION_HEADERS = ["ingredients", "directions", "notes", "nutrition", "source"]


def _find_section(text: str, header: str) -> tuple[int, int] | None:
    """Return (start, end) line indices for *header*, or None.

    *start* is the line *after* the header.
    *end* is the line of the next recognised header (exclusive), or the
    last line of the text.
    """
    lines = text.splitlines()
    lower_header = header.lower()

    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == lower_header + ":":
            start = i + 1
            break

    if start is None:
        return None

    # Find the next section header after *start*
    end = len(lines)
    for j in range(start, len(lines)):
        for h in SECTION_HEADERS:
            if lines[j].strip().lower() == h + ":":
                end = j
                break
        if j < len(lines) and lines[j].strip().lower() in {h + ":" for h in SECTION_HEADERS}:
            break

    return start, end


def parse_recipe_text(text: str) -> dict:
    """Parse a plain-text recipe block into a structured dict.

    Returns a dict with keys: name, ingredients, directions.
    Optionally includes 'notes' if a Notes section is present.
    """
    lines = text.splitlines()

    # --- Name: first non-empty line before "Ingredients:" ---
    name = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower() == "ingredients:":
            break
        name = stripped
        break

    # --- Ingredients ---
    ingredients = ""
    rng = _find_section(text, "ingredients")
    if rng:
        start, end = rng
        ingredients = "\n".join(lines[start:end]).strip()

    # --- Directions ---
    directions = ""
    rng = _find_section(text, "directions")
    if rng:
        start, end = rng
        directions = "\n".join(lines[start:end]).strip()

    # --- Notes (optional) ---
    notes = ""
    rng = _find_section(text, "notes")
    if rng:
        start, end = rng
        notes = "\n".join(lines[start:end]).strip()

    result = {
        "name": name,
        "ingredients": ingredients,
        "directions": directions,
    }
    if notes:
        result["notes"] = notes

    return result
