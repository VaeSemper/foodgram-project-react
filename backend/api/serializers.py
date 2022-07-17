from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes,
                            Tags)

User = get_user_model()


def get_obj_of_current_user(serializer, obj, model):
    user = serializer.context['request'].user
    if user.is_anonymous:
        return False
    elif model is Follow:
        return model.objects.filter(follower=user, author=obj).exists()
    elif model is RecipeInCart:
        return model.objects.filter(user=user, recipe=obj).exists()
    return False


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        return get_obj_of_current_user(self, obj, Follow)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',)
        read_only_fields = ('id',)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientInRecipeSerializer(many=True,
                                               source='recipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'text', 'image',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        return get_obj_of_current_user(self, obj, RecipeInCart)

    def get_is_in_shopping_cart(self, obj):
        return get_obj_of_current_user(self, obj, RecipeInCart)
