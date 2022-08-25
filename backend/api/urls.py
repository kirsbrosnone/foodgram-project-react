from django.urls import include, path
from rest_framework import routers

from api.views import (
    FollowUserViewSet, IngredientViewSet, RecipeViewSet, TagViewSet,
)

app_name = 'api'


class NoPutRouter(routers.DefaultRouter):
    """Роутер, отключающий PUT запросы."""

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        if 'put' in bound_methods.keys():
            del bound_methods['put']
        return bound_methods


router = NoPutRouter()

router.register('users', FollowUserViewSet, basename='follow')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
