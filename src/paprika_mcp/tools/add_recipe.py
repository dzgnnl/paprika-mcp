"""Add recipe tool - creates a new recipe in Paprika."""

from typing import Any

from mcp.types import TextContent
from paprika_recipes.remote import RemoteRecipe

from ..utils import get_categories, get_remote

# Free-text recipe fields that can be set when creating a recipe
TEXT_FIELDS = [
    "ingredients",
    "directions",
    "description",
    "notes",
    "servings",
    "prep_time",
    "cook_time",
    "total_time",
    "difficulty",
    "source",
    "source_url",
    "image_url",
    "nutritional_info",
]


async def add_recipe_tool(args: dict[str, Any]) -> list[TextContent]:
    """Create a new recipe."""
    name = args["name"].strip()
    category_names = args.get("categories", [])
    rating = args.get("rating", 0)
    allow_duplicate = args.get("allow_duplicate", False)

    if not name:
        return [TextContent(type="text", text="Error: Recipe name cannot be empty")]

    if not isinstance(rating, int) or not 0 <= rating <= 5:
        return [
            TextContent(
                type="text", text="Error: Rating must be a whole number from 0 to 5"
            )
        ]

    # Get the remote
    remote = get_remote()

    # Refuse to create a second recipe with the same name unless asked to
    if not allow_duplicate:
        for r in remote.recipes:
            if not r.in_trash and r.name.strip().lower() == name.lower():
                return [
                    TextContent(
                        type="text",
                        text=f"Error: A recipe named '{r.name}' already exists (ID: {r.uid}). No recipe was created. Use update_recipe to change it, or set allow_duplicate=true to create another one.",
                    )
                ]

    # Resolve category names to UUIDs before saving anything
    category_uids = []
    if category_names:
        categories_data = get_categories(remote.bearer_token)
        name_to_uid = categories_data["name_to_uid"]

        missing = [c for c in category_names if c.strip().lower() not in name_to_uid]
        if missing:
            available = ", ".join(sorted(categories_data["uid_to_name"].values()))
            return [
                TextContent(
                    type="text",
                    text=f"Error: Category not found: {', '.join(missing)}. No recipe was created.\n\nAvailable categories:\n{available}",
                )
            ]

        for c in category_names:
            uid = name_to_uid[c.strip().lower()]
            if uid not in category_uids:
                category_uids.append(uid)

    recipe = RemoteRecipe(
        name=name,
        categories=category_uids,
        rating=rating,
        **{field: args[field] for field in TEXT_FIELDS if args.get(field)},
    )

    try:
        remote.add_recipe(recipe)
    except Exception as e:
        return [
            TextContent(type="text", text=f"Error creating recipe '{name}': {str(e)}")
        ]

    category_text = ", ".join(category_names) if category_names else "none"
    return [
        TextContent(
            type="text",
            text=f"Successfully created recipe '{name}' (ID: {recipe.uid})\n\nCategories: {category_text}",
        )
    ]


# Tool definition
TOOL_DEFINITION = {
    "name": "add_recipe",
    "description": (
        "Create a new recipe in Paprika. Only the name is required. "
        "Use list_categories first to find valid category names. "
        "Refuses to create a recipe whose name matches an existing recipe "
        "unless allow_duplicate is true. "
        "This operation modifies the user's recipe library; confirm the "
        "recipe contents with the user before creating it."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Recipe title"},
            "ingredients": {
                "type": "string",
                "description": "Ingredients, one per line",
            },
            "directions": {
                "type": "string",
                "description": "Directions, one step per line or paragraph",
            },
            "description": {
                "type": "string",
                "description": "Short description or summary",
            },
            "notes": {"type": "string", "description": "Additional notes"},
            "servings": {
                "type": "string",
                "description": "Servings or yield, e.g. '4' or '12 cookies'",
            },
            "prep_time": {"type": "string", "description": "e.g. '15 min'"},
            "cook_time": {"type": "string", "description": "e.g. '1 hr'"},
            "total_time": {"type": "string", "description": "e.g. '1 hr 15 min'"},
            "difficulty": {"type": "string", "description": "e.g. 'Easy'"},
            "source": {
                "type": "string",
                "description": "Recipe source, e.g. cookbook or website name",
            },
            "source_url": {"type": "string", "description": "URL of the original"},
            "image_url": {
                "type": "string",
                "description": "URL of an image for the recipe",
            },
            "nutritional_info": {
                "type": "string",
                "description": "Nutritional information",
            },
            "categories": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Category NAMES (not UUIDs) to assign. Must already exist in Paprika (case-insensitive).",
            },
            "rating": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Star rating from 0 (unrated) to 5",
            },
            "allow_duplicate": {
                "type": "boolean",
                "description": "Create the recipe even if one with the same name exists (default: false)",
            },
        },
        "required": ["name"],
    },
}
