"""Remove category from recipe tool - removes a category tag from a recipe."""

from typing import Any

from mcp.types import TextContent

from ..utils import clear_categories_cache, get_categories, get_remote, translate_category_uids


async def remove_category_tool(args: dict[str, Any]) -> list[TextContent]:
    """Remove a category from a recipe by category name."""
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

    category_uid = name_to_uid.get(category_name.lower())
    if not category_uid:
        # Show what categories this recipe currently has
        current_names = translate_category_uids(
            recipe.categories or [], remote.bearer_token
        )
        return [
            TextContent(
                type="text",
                text=f"Error: Category '{category_name}' not found.\n\nRecipe's current categories: {current_names or 'none'}",
            )
        ]

    # Check if the recipe actually has this category
    current_categories = recipe.categories or []
    if category_uid not in current_categories:
        current_names = translate_category_uids(current_categories, remote.bearer_token)
        return [
            TextContent(
                type="text",
                text=f"Recipe '{recipe.name}' does not have category '{category_name}'.\n\nCurrent categories: {current_names or 'none'}",
            )
        ]

    # Remove the category
    current_categories.remove(category_uid)
    recipe.categories = current_categories

    # Upload the updated recipe
    try:
        remote.upload_recipe(recipe)
        clear_categories_cache()
        remaining_names = translate_category_uids(recipe.categories, remote.bearer_token)
        return [
            TextContent(
                type="text",
                text=f"Successfully removed category '{category_name}' from recipe '{recipe.name}' (ID: {recipe_id})\n\nRemaining categories: {remaining_names or 'none'}",
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
    "name": "remove_category",
    "description": (
        "Remove a category tag from a recipe. "
        "Use read_recipe to see the recipe's current categories first. "
        "This is a DANGEROUS operation that modifies the recipe."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "recipe_id": {
                "type": "string",
                "description": "Recipe UID to remove the category from",
            },
            "category_name": {
                "type": "string",
                "description": "Name of the category to remove (case-insensitive)",
            },
        },
        "required": ["recipe_id", "category_name"],
    },
}
