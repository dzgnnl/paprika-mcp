"""Add category to recipe tool - assigns a category tag to a recipe."""

from typing import Any

from mcp.types import TextContent

from ..utils import (
    clear_categories_cache,
    get_categories,
    get_remote,
    translate_category_uids,
)


async def add_category_tool(args: dict[str, Any]) -> list[TextContent]:
    """Add a category to a recipe by category name."""
    recipe_id = args["recipe_id"]
    category_name = args["category_name"]

    # Get the remote
    remote = get_remote()

    # Fetch the recipe
    recipe = None
    for r in remote.recipes:
        if r.uid == recipe_id:
            recipe = r
            break

    if not recipe:
        return [
            TextContent(
                type="text",
                text=f"Error: No recipe found with ID '{recipe_id}'",
            )
        ]

    # Resolve category name to UID
    categories_data = get_categories(remote.bearer_token)
    name_to_uid = categories_data["name_to_uid"]
    uid_to_name = categories_data["uid_to_name"]

    category_uid = name_to_uid.get(category_name.lower())
    if not category_uid:
        available = ", ".join(sorted(uid_to_name.values()))
        return [
            TextContent(
                type="text",
                text=f"Error: Category '{category_name}' not found.\n\nAvailable categories:\n{available}",
            )
        ]

    # Check if already assigned
    current_categories = recipe.categories or []
    if category_uid in current_categories:
        return [
            TextContent(
                type="text",
                text=f"Recipe '{recipe.name}' already has category '{category_name}'.",
            )
        ]

    # Add the category
    current_categories.append(category_uid)
    recipe.categories = current_categories

    # Upload the updated recipe
    try:
        remote.upload_recipe(recipe)
        clear_categories_cache()
        new_category_names = translate_category_uids(recipe.categories, remote.bearer_token)
        return [
            TextContent(
                type="text",
                text=f"Successfully added category '{category_name}' to recipe '{recipe.name}' (ID: {recipe_id})\n\nCurrent categories: {new_category_names}",
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error updating recipe '{recipe.name}': {str(e)}",
            )
        ]


# Tool definition
TOOL_DEFINITION = {
    "name": "add_category",
    "description": (
        "Add a category tag to a recipe. "
        "Use list_categories first to find available category names. "
        "This is a DANGEROUS operation that modifies the recipe."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "recipe_id": {
                "type": "string",
                "description": "Recipe UID to add the category to",
            },
            "category_name": {
                "type": "string",
                "description": "Name of the category to add (case-insensitive)",
            },
        },
        "required": ["recipe_id", "category_name"],
    },
}
