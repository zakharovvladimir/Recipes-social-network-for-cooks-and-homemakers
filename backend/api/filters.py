"""Filters.py."""
from django.contrib.auth import get_user_model
from django_filters.rest_framework import BooleanFilter, FilterSet, filters
from recipes.models import Ingredients, Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    """Filters instances of the Recipe model based on criterias."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        """Defines the model to be filtered."""

        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        """Define a method 'filter_is_favorited'."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Define a method 'filter_is_in_shopping_cart'."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset


class IngredientFilter(FilterSet):
    """Defines a filter that filters instances of the Ingredients model."""

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    ordering = filters.OrderingFilter(fields=('name',))

    class Meta:
        """Defines the model to be filtered."""

        model = Ingredients
        fields = ['name']
