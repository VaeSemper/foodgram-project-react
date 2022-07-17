from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipesViewSet, TagsViewSet, IngredientsViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
