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

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class AmountOfIngredient(models.Model):
    """Количество ингридиентов."""

    ingredient_recipe = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, blank=True,
        verbose_name='Ингредиент', help_text='Выберите ингридиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество', blank=False, default=1,
        validators=[
            MinValueValidator(1, 'Минимальное количество ингридиента')
        ]
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return (f'{self.amount}{self.ingredient_recipe.measurement_unit}'
                f'{self.ingredient_recipe.name}')


class Tag(models.Model):
    """Класс тэга."""

    name = models.CharField(
        'Тэг', max_length=200, unique=True, blank=False,
        help_text='Имя тэга',
    )
    color = models.CharField(
        'Цвет', max_length=7, unique=True, blank=False, null=True,
        default='#D3D3D3', help_text='Цвет в формате HEX #D3D3D3',
    )
    slug = models.SlugField(
        'Слаг', max_length=200, unique=True, blank=False, null=True,
        help_text='Уникальный слаг',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецепта."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        'Название рецепта', max_length=200, blank=False,
    )
    text = models.TextField(
        'Описание рецепта', blank=False,
    )
    ingredients = models.ManyToManyField(
        AmountOfIngredient, blank=False, related_name='recipes',
        verbose_name='Ингредиенты',
    )
    image = models.ImageField(
        'Изображение рецепта', upload_to='recipe_images', blank=False,
    )
    tags = models.ManyToManyField(
        Tag, blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', blank=False, default=1,
        help_text='В минутах',
        validators=[
            MinValueValidator(1, 'Минимальное время приготовления 1 мин.')
        ],
    )
    pub_date = models.DateField(
        'Дата публикации', auto_now_add=True, db_index=True, blank=False,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavouriteRecipe(models.Model):
    """Список избранного у пользователя."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favourite_recipe',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favourite_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favourite_recipe_user'
            )
        ]

    def __str__(self) -> str:
        return (f'Пользователь {self.user.username} добавил рецепт: '
                f'{self.recipe.name} в избранное')


class ShoppingCart(models.Model):
    """Список покупок у пользователя."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopcart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopcart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='shopcart_user'
            )
        ]

    def __str__(self) -> str:
        return (f'Пользователь {self.user.username} добавил рецепт: '
                f'{self.recipe.name} в список покупок')
