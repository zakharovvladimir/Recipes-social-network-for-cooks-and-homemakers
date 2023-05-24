"""API views.py."""
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Favorite, IngredientInRecipe, Ingredients,
                            Recipe, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, RecipeReadSerializer,
                          RecipeShortenedSerializer, RecipeWriteSerializer,
                          TagsSerializer)

User = get_user_model()


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Ingredients ViewSet with read only endpoints."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagsViewSet(ReadOnlyModelViewSet):
    """Tags ViewSet with read only endpoints."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Recipe ViewSet with read only endpoints."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """Save data submitted by serializer."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Check request method."""
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Start custom favorite action."""
        if request.method == 'POST':
            if not Favorite.objects.filter(
                user=request.user, recipe__id=pk
                    ).exists():
                return self.add_to(Favorite, request.user, pk)
            return self.delete_from(Favorite, request.user, pk)
        return self.delete_from(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Start function of shopping cart."""
        if request.method == 'POST':
            return self.add_to(Cart, request.user, pk)
        return self.delete_from(Cart, request.user, pk)

    def add_to(self, model, user, pk):
        """Add object method."""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortenedSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        """Delete object method."""
        recipe_query = model.objects.filter(user=user, recipe__id=pk)
        if recipe_query.exists():
            recipe_query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Recipe has already been deleted!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Download shopping cart as HTML."""
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
            'recipe__name'
        ).annotate(amount=Sum('amount'))
        ingredients_list = sorted(ingredients, key=lambda x: x['recipe__name'])
        shopping_list = [
            f'{ingredient["recipe__name"]}\n'
            f'<li>{ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}) '
            f'- {ingredient["amount"]}</li><br>'
            for ingredient in ingredients_list
        ]
        html = ''.join(shopping_list)
        response = HttpResponse(content_type='text/html')
        response.write(html)
        filename = 'shoppinglist.html'
        disposition = f'attachment; filename="{filename}"'
        response['Content-Disposition'] = disposition
        return response
