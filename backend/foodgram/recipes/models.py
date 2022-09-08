from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.TextField(verbose_name='Название ингредиента')
    measurement_unit = models.TextField(
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент',
        on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиента',
        default=0,
        validators=[MinValueValidator(0)]
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_for_recipe',
            ),
        ]

    def __str__(self):
        return (f'для {self.recipe} требуется {self.ingredient.name},'
                f' {self.amount} {self.ingredient.measurement_unit}')


class Tag(models.Model):
    name = models.TextField(
        verbose_name='Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=7,
        unique=True
    )
    slug = models.TextField(
        verbose_name='SLUG',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег рецепта',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег для рецепта'
        verbose_name_plural = 'Теги для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_for_recipe',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} содержит тег {self.tag}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.TextField(verbose_name='Название рецепта',)
    text = models.TextField(verbose_name='Описание',)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images/'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through=RecipeIngredient,
        default=0,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        through=RecipeTag
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'рецепт {self.name} от {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец избранного',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт добавленный в избранное',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='single_favorite',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Автор списка покупок',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты добавленные в список покупок',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_list',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
