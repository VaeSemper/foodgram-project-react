from rest_framework import viewsets

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
