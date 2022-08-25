from django_filters import AllValuesMultipleFilter, ModelMultipleChoiceFilter
from django_filters.rest_framework import BooleanFilter, FilterSet

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтрация рецептов."""

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name='tags__slug',
        to_field_name='slug', label='Тэг'
    )
    author = AllValuesMultipleFilter(
        field_name='author__username', label='Автор'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart', method='filter',
        label='В списке покупок',
    )
    is_favorited = BooleanFilter(
        field_name='is_favorited', method='filter', label='В избранном',
    )

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(shopping_cart__user=self.request.user)
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite_recipes__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
