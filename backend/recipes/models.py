from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Класс ингредиента."""

    name = models.CharField(
        'Ингредиент', max_length=200, blank=False,
        help_text='Наименование, например яйцо.',
    )
    measurement_unit = models.CharField(
        'Единица измерения', max_length=200, blank=False,
        help_text='Единица измерения, например штука/шт.',
    )

    def __str__(self):
        return self.name


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


class Recipe(models.Model):
    """Класс рецепта."""

    pub_date = models.DateField(
        auto_now_add=True, db_index=True, blank=False,
        help_text='Дата создания рецепта',
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='recipes',
        help_text='Автор рецепта',
    )
    name = models.CharField(
        max_length=200, blank=False, help_text='Название рецепта',
    )
    text = models.TextField(
        blank=False, help_text='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, blank=False, related_name='recipes',
    )
    image = models.ImageField(
        upload_to='recipe_images', blank=False, help_text='Фото рецепта',
    )
    tags = models.ManyToManyField(
        Tag, blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False, default=1, help_text='Время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'Минимальное время приготовления 1 мин.')
        ],
    )
