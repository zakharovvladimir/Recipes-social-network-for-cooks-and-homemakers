"""Admin.py."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import CharFilter

from .models import (Cart, Favorite, IngredientInRecipe, Ingredients, Recipe,
                     Tag)


class IngredientsAdmin(admin.ModelAdmin):
    """Ingredients model in admin."""

    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', ('name', CharFilter(lookup_expr='istartswith')))
    search_fields = ('name',)
    empty_value_display = _('-empty-')


class TagsAdmin(admin.ModelAdmin):
    """Tags model in admin."""

    list_display = ('name', 'color',)
    list_filter = ('id', 'name')
    list_editable = ('color',)
    search_fields = ('name',)
    empty_value_display = _('-empty-')


class RecipeAdmin(admin.ModelAdmin):
    """Recipe model in admin."""

    list_display = (
        'name',
        'text',
        'author',
        'cooking_time',
        'image',
    )
    list_editable = ('text', 'author', 'cooking_time', 'image',)
    search_fields = ('name', 'text', 'author',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = _('-empty-')


class CartAdmin(admin.ModelAdmin):
    """Cart model in Admin."""

    list_display = ('user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    """Favorite model in admin."""

    list_display = ('user', 'recipe',)


class IngredientInRecipeAdmin(admin.ModelAdmin):
    """IngredientInRecipe model in admin."""

    list_display = ('recipe', 'ingredient', 'amount',)


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
