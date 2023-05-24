"""Serializers.py."""
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import IngredientInRecipe, Ingredients, Recipe, Tag
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        ReadOnlyField)
from users.models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """User Create model seralizer."""

    class Meta:
        """CustomUserCreate Serializer Meta."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """User model serializer."""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        """CustomUserSerializer Meta."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Is subscribed func."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class RecipeShortenedSerializer(ModelSerializer):
    """Recipe model shortened serializer."""

    image = Base64ImageField()

    class Meta:
        """RecipeShortenedSerializer Meta."""

        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(ModelSerializer):
    """Follow model subscribe serialization."""

    id = ReadOnlyField()
    email = ReadOnlyField()
    username = ReadOnlyField()
    first_name = ReadOnlyField()
    last_name = ReadOnlyField()
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField(method_name='get_recipes')
    recipes_count = SerializerMethodField(method_name='get_recipes_count')
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'author'
        )

    def validate(self, data):
        """Start validation pass."""
        author = self.instance
        user = self.context.get('request').user
        if Follow.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail=_("You've already a follower"),
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail=_("You cannot subscribe to yourself"),
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        """Recipes number of items."""
        return obj.recipes.count()

    def get_recipes(self, instance):
        """Retrieve a specified number of recipe instances."""
        limit = self.context['request'].GET.get('recipes_limit')
        query_set = instance.recipes.all()[
            :int(limit)] if limit else instance.recipes.all()
        context = {'request': self.context['request']}
        serialized_data = RecipeShortenedSerializer(
            query_set,
            many=True,
            context=context)
        return serialized_data.data

    def get_is_subscribed(self, obj):
        """Check of user subscription."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated or not hasattr(
            obj, 'author'
                ):
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.author
            ).exists()


class IngredientsSerializer(ModelSerializer):
    """Ingredients model serialization."""

    class Meta:
        """IngredientsSerializer Meta."""

        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

        ordering = ['name']


class RevealIngredientsInRecipeSerializer(ModelSerializer):
    """IngredientsInRecipe model serialization."""

    id = ReadOnlyField()
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        """RevealIngredientsInRecipeSerializer Meta."""

        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    ordering = ['name']


class TagsSerializer(ModelSerializer):
    """Tag model serialization."""

    class Meta:
        """TagsSerializer Meta."""

        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class RecipeReadSerializer(ModelSerializer):
    """Recipe model Read serialization."""

    tags = TagsSerializer(read_only=True, many=True)
    ingredients = SerializerMethodField(method_name='get_ingredients')
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    author = CustomUserSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        """Init."""
        self.request = kwargs['context']['request']
        super().__init__(*args, **kwargs)

    class Meta:
        """RecipeReadSerializer Meta."""

        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        """Get ingredients."""
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return RevealIngredientsInRecipeSerializer(
            ingredients,
            many=True).data

    def get_is_favorited(self, obj):
        """Get favorited recipe."""
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Get recipe in shopping cart."""
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class IngredientInRecipeWriteSerializer(ModelSerializer):
    """IngredientInRecipe Write serialization."""

    id = IntegerField(write_only=True)

    class Meta:
        """IngredientInRecipeWriteSerializer Meta."""

        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(ModelSerializer):
    """Recipe model Read serialization."""

    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                  many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        """RecipeWriteSerializer Meta."""

        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'author',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_ingredients(self, ingredients):
        """Validate a list of ingredients."""
        ids_seen = set()
        for i in ingredients:
            if not i.get('id'):
                raise ValidationError('No ingredient ID found')
            if i['id'] in ids_seen:
                raise ValidationError('Ingredients cannot be repeated')
            ids_seen.add(i['id'])
            if not i.get('amount'):
                raise ValidationError('No ingredient quantity found')
            if not isinstance(i['amount'], (int, float)) or i['amount'] <= 1:
                raise ValidationError('Qty value should be a nmb more than 0')
        return ingredients

    def validate_tags(self, value):
        """Check value tags."""
        tags = value
        if not tags:
            raise ValidationError(_('No tags found'))
        if len(set(tags)) != len(tags):
            raise ValidationError(_('Tag is not unique'))
        return value

    def validate_cooking_time(value):
        """Check value cooking_time."""
        if value <= 0:
            raise ValidationError(
                'Cooking time should be more than 0'
            )
        return value

    @transaction.atomic
    def ingredients_amounts(self, ingredients, recipe):
        """Create ingredients amount."""
        IngredientInRecipe.objects.bulk_create(
            [IngredientInRecipe(
                ingredient=Ingredients.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        """Recipe creation."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingredients_amounts(recipe=recipe,
                                 ingredients=ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Recipe update."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.ingredients_amounts(recipe=instance,
                                 ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Return a serialized representation using RecipeReadSerializer."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance,
                                    context=context).data
