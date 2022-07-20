from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CartSerializer, FavoriteSerializer,
                             FollowSerializer, IngredientsSerializer,
                             RecipeCreateSerializer, RecipesSerializer,
                             TagsSerializer)
from api.utils import add_delete_obj, download_shopping_cart
from recipes.models import (FavoriteRecipe, Follow, Ingredients, RecipeInCart,
                            Recipes, Tags)

User = get_user_model()


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


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update',):
            permission_classes = (IsAdminOrAuthorOrReadOnly,)
        else:
            permission_classes = (IsAuthenticatedOrReadOnly,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipesSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        return add_delete_obj(request, pk, FavoriteSerializer, FavoriteRecipe)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        return add_delete_obj(request, pk, CartSerializer, RecipeInCart)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        return download_shopping_cart(request)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Follow.objects.all()

    def get_object(self):
        follower = self.request.user
        author = get_object_or_404(User, id=self.kwargs['pk'])
        return get_object_or_404(Follow, follower=follower, author=author)

    def perform_create(self, serializer):
        follower = self.request.user
        author = get_object_or_404(User, id=self.kwargs['pk'])
        serializer.save(follower=follower, author=author)

    def perform_destroy(self, serializer):
        follower = self.request.user
        author = get_object_or_404(User, id=self.kwargs['pk'])
        query = Follow.objects.filter(follower=follower, author=author)
        if not query.exists():
            raise ValidationError({'errors': 'You are not subscribe on this '
                                             'user.'})
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
