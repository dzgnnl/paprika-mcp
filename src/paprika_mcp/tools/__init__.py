"""Tools module - exports all MCP tool implementations."""

from .add_category import TOOL_DEFINITION as ADD_CATEGORY_DEF
from .add_category import add_category_tool
from .delete_recipe import TOOL_DEFINITION as DELETE_RECIPE_DEF
from .delete_recipe import delete_recipe_tool
from .format_fraction import TOOL_DEFINITION as FORMAT_FRACTION_DEF
from .format_fraction import format_fraction_tool
from .list_categories import TOOL_DEFINITION as LIST_CATEGORIES_DEF
from .list_categories import list_categories_tool
from .read_recipe import TOOL_DEFINITION as READ_RECIPE_DEF
from .read_recipe import read_recipe_tool
from .remove_category import TOOL_DEFINITION as REMOVE_CATEGORY_DEF
from .remove_category import remove_category_tool
from .search_recipes import TOOL_DEFINITION as SEARCH_RECIPES_DEF
from .search_recipes import search_recipes_tool
from .update_recipe import TOOL_DEFINITION as UPDATE_RECIPE_DEF
from .update_recipe import update_recipe_tool

# Export all tools and their definitions
TOOLS = {
    "add_category": {
        "definition": ADD_CATEGORY_DEF,
        "handler": add_category_tool,
    },
    "remove_category": {
        "definition": REMOVE_CATEGORY_DEF,
        "handler": remove_category_tool,
    },
    "delete_recipe": {
        "definition": DELETE_RECIPE_DEF,
        "handler": delete_recipe_tool,
    },
    "search_recipes": {
        "definition": SEARCH_RECIPES_DEF,
        "handler": search_recipes_tool,
    },
    "read_recipe": {
        "definition": READ_RECIPE_DEF,
        "handler": read_recipe_tool,
    },
    "update_recipe": {
        "definition": UPDATE_RECIPE_DEF,
        "handler": update_recipe_tool,
    },
    "list_categories": {
        "definition": LIST_CATEGORIES_DEF,
        "handler": list_categories_tool,
    },
    "format_fraction": {
        "definition": FORMAT_FRACTION_DEF,
        "handler": format_fraction_tool,
    },
}

__all__ = [
    "TOOLS",
    "add_category_tool",
    "remove_category_tool",
    "delete_recipe_tool",
    "search_recipes_tool",
    "read_recipe_tool",
    "update_recipe_tool",
    "list_categories_tool",
    "format_fraction_tool",
]
