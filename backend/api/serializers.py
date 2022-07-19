from django.contrib.auth import get_user_model
from django.db import models
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes,
                            Tags)

User = get_user_model()


def get_obj_of_current_user(serializer, instance, model, method):
    user = serializer.context['request'].user
    if user.is_anonymous:
        return False
    if method == 'exists':
        if model is Follow:
            return model.objects.filter(follower=user,
                                        author=instance).exists()
        elif model is RecipeInCart:
            return model.objects.filter(user=user, recipe=instance).exists()
        elif model is FavoriteRecipe:
            return model.objects.filter(user=user, recipe=instance).exists()
    elif method == 'count':
        if model is Recipes:
            return model.objects.filter(author=instance).count()
    return False


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        return get_obj_of_current_user(self, obj, Follow, 'exists')


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


class TagPrimaryKeyRelatedSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return TagsSerializer(value).data


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagPrimaryKeyRelatedSerializer(queryset=Tags.objects.all(),
                                          many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, source='recipe',
                                               read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'text', 'image',
                  'cooking_time',)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(recipe=recipe,
                                              ingredient_id=ingredient['id'],
                                              amount=ingredient['amount'])

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        ingredients = self.context['request'].data.pop('ingredients')
        recipe = Recipes.objects.create(
            author=author,
            image=image,
            **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def get_is_favorited(self, obj):
        return get_obj_of_current_user(self, obj, FavoriteRecipe, 'exists')

    def get_is_in_shopping_cart(self, obj):
        return get_obj_of_current_user(self, obj, RecipeInCart, 'exists')


class ShortRecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        query = obj.author.recipes.all()
        if recipes_limit:
            query = query[:int(recipes_limit)]
        return ShortRecipesSerializer(instance=query, many=True).data

    def get_is_subscribed(self, obj):
        return get_obj_of_current_user(self, obj.author, Follow, 'exists')

    def get_recipes_count(self, obj):
        return get_obj_of_current_user(self, obj.author, Recipes, 'count')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInCart
        fields = ('user', 'recipe',)
