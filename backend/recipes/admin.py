from django.contrib import admin

from .models import (
    AmountOfIngredient, FavouriteRecipe, Ingredient, Recipe, ShoppingCart, Tag,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name')
    list_filter = ('measurement_unit')
    empty_value_display = ('-пусто-')


@admin.register(AmountOfIngredient)
class AmountOfIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name')
    empty_value_display = ('-пусто-')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'name', 'text', 'cooking_time')
    readonly_fields = ('favourites')
    list_filter = ('pub_date', 'cooking_time')
    search_fields = ('author', 'name', 'text')
    empty_value_display = ('-пусто-')

    def favourites(self, obj):
        return obj.favourite_recipe.count()


@admin.register(FavouriteRecipe)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_filter = ('user')
    search_fields = ('recipe')
    empty_value_display = ('-пусто-')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_filter = ('user')
    search_fields = ('recipe')
    empty_value_display = ('-пусто-')
