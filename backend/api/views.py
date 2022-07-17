from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import (TagsSerializer, IngredientsSerializer,
                             IngredientInRecipeSerializer, RecipesSerializer)
from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes, Tags)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
