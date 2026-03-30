"""Delete recipe tool - soft-deletes a recipe by moving it to trash."""

from typing import Any

from mcp.types import TextContent

from ..utils import get_remote


async def delete_recipe_tool(args: dict[str, Any]) -> list[TextContent]:
    """Soft-delete a recipe by setting in_trash to True."""
    recipe_id = args["recipe_id"]

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

    # Check if already trashed
    if recipe.in_trash:
        return [
            TextContent(
                type="text",
                text=f"Recipe '{recipe.name}' is already in the trash.",
            )
        ]

    # Soft-delete by moving to trash
    recipe.in_trash = True

    try:
        remote.upload_recipe(recipe)
        return [
            TextContent(
                type="text",
                text=f"Successfully moved recipe '{recipe.name}' (ID: {recipe_id}) to trash.\n\nThe recipe can be restored from the Paprika app's trash.",
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error deleting recipe '{recipe.name}': {str(e)}",
            )
        ]


# Tool definition
TOOL_DEFINITION = {
    "name": "delete_recipe",
    "description": (
        "Soft-delete a recipe by moving it to the trash. "
        "The recipe can still be restored from trash in the Paprika app. "
        "This is a DANGEROUS operation. Use read_recipe first to confirm "
        "you have the correct recipe."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "recipe_id": {
                "type": "string",
                "description": "Recipe UID to delete",
            },
        },
        "required": ["recipe_id"],
    },
}
