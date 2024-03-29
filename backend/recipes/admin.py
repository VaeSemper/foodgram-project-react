from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from recipes.admin_tweaks import IngredientsInline
from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes, Tags,)

LINES_PER_PAGE = 20
TEXT_LINE_LIMIT = 100

User = get_user_model()

UserAdmin.list_filter = ('username', 'email',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    list_per_page = LINES_PER_PAGE


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit',)
    list_per_page = LINES_PER_PAGE
    search_fields = ('name',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', 'get_measurement_unit')
    list_per_page = LINES_PER_PAGE

    @admin.display(description='measurement unit')
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'recipe_description', 'cooking_time',
                    'pub_date', 'get_number_in_favorites',)
    list_filter = ('name', 'author', 'tags',)
    list_per_page = LINES_PER_PAGE
    search_fields = ('name',)
    inlines = (IngredientsInline,)

    @staticmethod
    def recipe_description(obj):
        return obj.text[:TEXT_LINE_LIMIT] + '...'

    @admin.display(description='number of recipe in favorites')
    def get_number_in_favorites(self, obj):
        return obj.fav_recipe.filter(recipe=obj).count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'author',)
    list_per_page = LINES_PER_PAGE
    search_fields = ('author',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_per_page = LINES_PER_PAGE


@admin.register(RecipeInCart)
class RecipeInCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_per_page = LINES_PER_PAGE
