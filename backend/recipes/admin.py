from django.contrib import admin

from .models import (
    AmountOfIngredient, FavouriteRecipe, Ingredient, Recipe, ShoppingCart, Tag,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Панель администратора ингридиентов."""

    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    empty_value_display = ('-пусто-')


@admin.register(AmountOfIngredient)
class AmountOfIngredientAdmin(admin.ModelAdmin):
    """Панель администратора количества ингридиентов."""

    list_display = ('ingredient_recipe', 'amount')
    list_filter = ('ingredient_recipe', 'amount')
    empty_value_display = ('-пусто-')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Панель администратора тэгов."""

    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color')
    search_fields = ('name', 'color', 'slug')
    empty_value_display = ('-пусто-')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Панель администратора рецепта."""

    list_display = (
        'pub_date', 'author', 'name', 'text', 'cooking_time',
    )
    list_filter = (
        'pub_date', 'author', 'name', 'text', 'cooking_time',
    )
    search_fields = ('author', 'name', 'text')
    empty_value_display = ('-пусто-')


@admin.register(FavouriteRecipe)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    """Панель администратора любимых рецептов."""

    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = ('-пусто-')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Панель администратора списка покупок."""

    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = ('-пусто-')
