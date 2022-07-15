from rest_framework import serializers

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes, Tags)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsSerializer(serializers.ModelSerializer):
    pass


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    pass


class RecipesSerializer(serializers.ModelSerializer):
    pass
