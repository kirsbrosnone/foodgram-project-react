from io import StringIO

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import AdminAuthorOrReadOnly, IsAuthor
from api.serializers import (
    FavouriteRecipeSerializer, FollowUserSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, ShoppingCartSerializer,
    TagSerializer,
)
from recipes.models import (
    AmountOfIngredient, FavouriteRecipe, Ingredient, Recipe, ShoppingCart, Tag,
)
from users.models import CustomUser, Follow


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление тегов. /tags/"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = [SearchFilter, ]
    search_fields = ['^name', '^slug', ]
    throttle_scope = 'tags'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингредиенты. /ingredients/"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter, ]
    search_fields = ['^name', ]
    throttle_scope = 'ingredients'


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты. /recipes/"""

    queryset = Recipe.objects.all()
    permission_classes = [AdminAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    filterset_class = RecipeFilter
    search_fields = ['name', 'text', ]
    throttle_scope = 'recipes'

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=['POST', 'DELETE'], detail=True, url_path='favorite',
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            recipe_favorite, created = FavouriteRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created:
                serializer = FavouriteRecipeSerializer()
                return Response(
                    serializer.to_representation(instance=recipe_favorite),
                    status=status.HTTP_201_CREATED,
                )
            fav = FavouriteRecipe.objects.filter(user=user, recipe=recipe)
            if fav.exists():
                return Response(
                    'Рецепт уже есть в списке избранного',
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            fav = FavouriteRecipe.objects.filter(user=user, recipe=recipe)
            if fav.exists():
                fav.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                'Отсутствует рецепт для удаления из списка избранного',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', 'POST', 'DELETE'], detail=True,
            url_path='shopping_cart', permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if self.request.method in ['GET', 'POST']:
            recipe_shop, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe_shop),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                'Рецепт уже в корзине покупок',
                status=status.HTTP_400_BAD_REQUEST
            )
        elif self.request.method == 'DELETE':
            shop = ShoppingCart.objects.filter(user=user, recipe=recipe)
            if shop.exists():
                shop.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                'Отсутствует рецепт для удаления из списка покупок',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):
        cart_file = StringIO()
        ingredients = AmountOfIngredient.objects.filter(
            recipes__shopcart__user=request.user
        ).values(
            'ingredient_recipe__name', 'ingredient_recipe__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount')).values_list(
            'ingredient_recipe__name', 'ingredient_recipe__measurement_unit',
            'amount'
        )
        cart_file.write('Нужно купить: ')
        for ingredient in ingredients:
            cart_file.write(
                f'{ingredient[0]} {ingredient[2]} {ingredient[1]}, '
            )
        response = HttpResponse(cart_file.getvalue(), content_type='text',)
        response['Content-Disposition'] = (
            'attachment; filename="%s"' % 'cart_file.txt'
        )
        return response


class FollowUserViewSet(UserViewSet):
    """Подписки. /subscriptions/ /subscribe/."""

    throttle_scope = 'follows'

    @action(methods=['GET'], detail=False, url_path='subscriptions',
            permission_classes=[IsAuthor, ])
    def subscriptions(self, request):
        user = request.user
        user_follows = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(user_follows)
        serializer = FollowUserSerializer(
            pages, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=True, url_path='subscribe',
            permission_classes=[IsAuthenticated, ])
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            user = request.user
            author = get_object_or_404(CustomUser, id=id)
            if user == author:
                return Response(
                    'Нельзя подписаться/отписаться на себя',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow_user = Follow.objects.filter(user=user, author=author)
            if follow_user.exists():
                return Response(
                    'Вы уже подписаны', status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowUserSerializer(
                follow, context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            user = request.user
            author = get_object_or_404(CustomUser, id=id)
            if user == author:
                return Response(
                    'Нельзя подписаться/отписаться на себя',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow_user = Follow.objects.filter(user=user, author=author)
            if not follow_user.exists():
                return Response(
                    'Вы не подписаны', status=status.HTTP_400_BAD_REQUEST,
                )
            follow_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
