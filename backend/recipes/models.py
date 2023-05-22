"""Recipe models."""
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredients(models.Model):
    """Ingredients models."""

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name=_('Name'),
        )
    measurement_unit = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_('Measurement unit'),
        )

    @classmethod
    def create(cls, **kwargs):
        """Create ingredient."""
        ingredient = cls(**kwargs)
        ingredient.save()
        return ingredient

    class Meta():
        """Ingredients Meta."""

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='items_unique'),
        )
        ordering = ('-id',)
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        """Str."""
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('Name'),
        )
    color = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message=_('Enter the value in the correct format')
            )
        ],
        verbose_name=_('HEX'),
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('Tag slug'),
        )

    class Meta():
        """Tag Meta."""

        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        """Str."""
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name=_('Name'),
        )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name=_('Description'),
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('Author'),
    )
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
        blank=False,
        null=False,
        help_text=_('Load Image'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_('Time'),
        )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name=_('Ingredients'),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=_('Tags'),
    )

    class Meta():
        """Recipe Meta."""

        ordering = ['-id']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        """Str."""
        return self.name


class IngredientInRecipe(models.Model):
    """Recipe ingredients model."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name=_('Recipe'),
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name=_('Ingredient'),
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('Qty'),
    )

    class Meta:
        """IngredientInRecipe Meta."""

        verbose_name = _("Recipe's ingredients")
        verbose_name_plural = _("Recipes' ingredients")

    def __str__(self):
        """Str."""
        return (
            f'{self.ingredient.name} '
            f'- {self.amount} {self.ingredient.measurement_unit}'
        )


class Cart(models.Model):
    """Shopping cart model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name=_('User'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name=_('Recipe'),
    )

    class Meta:
        """Cart Meta."""

        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_cart')
        ]

    def __str__(self):
        """Str."""
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    """Favorite model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('User'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Recipe'),
    )

    class Meta:
        """Favorite Meta."""

        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_fav')
        ]

    def __str__(self):
        """Str."""
        return f'{self.user} {self.recipe}'
