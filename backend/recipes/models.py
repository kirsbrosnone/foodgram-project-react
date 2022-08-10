from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, blank=False,
    )
    color = models.CharField(
        max_length=7, unique=True, default='#D3D3D3', blank=False,
    )
    slug = models.SlugField(
        max_length=200, unique=True, blank=False,
    )


class Ingredient(models.Model):
    """Класс ингредиентов."""

    name = models.CharField(
        verbose_name='Ингредиент', max_length=200, blank=False,
        help_text='Наименование, например яйцо.',
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=200, blank=False,
        help_text='Единица измерения, например штука/шт',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецепта."""

    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes',
    )
