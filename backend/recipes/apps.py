"""Apps.py."""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Recipe app activation."""

    name = 'recipes'
    verbose_name = 'Recipes App'
