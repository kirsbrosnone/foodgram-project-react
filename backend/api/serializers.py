from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (
    AmountOfIngredient, FavouriteRecipe, Ingredient, Recipe, ShoppingCart, Tag,
)
from users.models import CustomUser, Follow


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов."""

    id = serializers.IntegerField(source='ingredient_recipe.id')
    name = serializers.CharField(
        source='ingredient_recipe.name', read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient_recipe.measurement_unit', read_only=True
    )

    class Meta:
        model = AmountOfIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'password', 'first_name', 'last_name',
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        user_subscribed = Follow.objects.filter(user=user, author=obj.id)
        return user_subscribed.exists()


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        favourite = FavouriteRecipe.objects.filter(user=user, recipe=obj)
        return favourite.exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=obj)
        return shopping_cart.exists()


class RecipeWriteSerializer(RecipeReadSerializer):
    """Сериализатор записи рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def validate(self, data):
        ingredients_data = data.get('ingredients', None)
        for ingredient in ingredients_data:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Минимальное количество ингридиентов 1')
                )
            get_object_or_404(
                Ingredient, pk=ingredient['ingredient']['id'])
            if data['ingredients'].count(ingredient) > 1:
                raise serializers.ValidationError('Ингредиент повторяется')
        if int(data['cooking_time']) <= 0:
            raise serializers.ValidationError('Время готовки в минутах')
        if len(data['tags']) == 0:
            raise serializers.ValidationError('Отсутствует тэг')
        for tag in data['tags']:
            if data['tags'].count(tag) > 1:
                raise serializers.ValidationError(
                    'Один и тот же тег в данном запросе встречается дважды!'
                )
        # data['ingredients'] = ingredients_data
        return data

    @staticmethod
    def create_ingredients(validated_data):
        validated_ingredients = validated_data.get('ingredients')
        ingredients_list = []
        if validated_ingredients:
            for ingredient in validated_ingredients:
                ingr_obj = Ingredient.objects.get(
                    pk=ingredient['ingredient_recipe']['id']
                )
                ingr, created = (
                    AmountOfIngredient.objects.get_or_create(
                        ingredient_recipe=ingr_obj, amount=ingredient['amount']
                    )
                )
                ingredients_list.append(ingr)
        return ingredients_list

    def create(self, validated_data):
        ingredients = self.create_ingredients(validated_data)
        tags = validated_data.pop('tags')
        validated_data.pop('ingredients')
        validated_data.update({'author': self.context['request'].user})
        recipe = Recipe.objects.create(**validated_data)
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = self.create_ingredients(validated_data)
        tags = validated_data.pop('tags')
        validated_data.pop('ingredients')
        validated_data.update({'author': self.context['request'].user})
        instance.tags.set(tags or instance.tags)
        instance.ingredients.set(ingredients or instance.ingredients)
        instance.save()
        updating_data = super(RecipeWriteSerializer, self)
        return updating_data.update(instance, validated_data)


class FavouriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов."""

    id = serializers.CharField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.CharField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = FavouriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка рецептов для покупок."""

    id = serializers.CharField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.CharField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class PreviewRecipeSerializer(serializers.ModelSerializer):
    """Превью рецепта."""

    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowUserSerializer(serializers.ModelSerializer):
    """Cериализатор подписок пользователей."""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        favourite = Follow.objects.filter(user=user, author=obj.author)
        return favourite.exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        preview = PreviewRecipeSerializer(queryset, many=True)
        return preview.data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj.author)
        return recipes.count()
