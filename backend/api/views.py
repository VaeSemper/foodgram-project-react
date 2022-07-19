from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response

from api.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CartSerializer, FavoriteSerializer,
                             FollowSerializer, IngredientsSerializer,
                             RecipesSerializer, TagsSerializer)
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
    serializer_class = RecipesSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter

    def add_delete_obj(self, request, pk, serializer_obj, model_obj):
        recipe = Recipes.objects.get(pk=pk)
        data = {
            'user': request.user.pk,
            'recipe': recipe.pk,
        }
        serializer = serializer_obj(context={'request': request}, data=data)
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            try:
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                raise ValidationError({'errors': 'Recipe already added.'})
        elif request.method == 'DELETE':
            obj_to_delete = model_obj.objects.filter(**data)
            if obj_to_delete.exists():
                obj_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'No such object.'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        return self.add_delete_obj(request, pk, FavoriteSerializer,
                                   FavoriteRecipe)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        return self.add_delete_obj(request, pk, CartSerializer, RecipeInCart)


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
        if follower == author:
            raise ValidationError({'errors': 'You cannot subscribe to '
                                             'yourself.'})
        try:
            serializer.save(follower=follower, author=author)
        except IntegrityError:
            raise ValidationError({'errors': 'You cannot subscribe the same '
                                             'user twice.'})

    def perform_destroy(self, serializer):
        follower = self.request.user
        author = get_object_or_404(User, id=self.kwargs['pk'])
        query = Follow.objects.filter(follower=follower, author=author)
        if not query.exists():
            raise ValidationError({'errors': 'You are not subscribe on this '
                                             'user.'})
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
