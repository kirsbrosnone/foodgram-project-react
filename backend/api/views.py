from api.permissions import AdminOrReadOnly
from api.serializers import TagSerializer
from recipes.models import Tag
from rest_framework import viewsets


class TagViewSet(viewsets.ModelViewSet):
    """Модель представления Тэгов."""

    permission_classes = (AdminOrReadOnly, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    pass
