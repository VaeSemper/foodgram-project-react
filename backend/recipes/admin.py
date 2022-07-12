from django.contrib import admin

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            Ingredients, RecipeInCart, Recipes, Tags)


LINES_PER_PAGE = 20


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    list_per_page = LINES_PER_PAGE


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    list_per_page = LINES_PER_PAGE
    search_fields = ('name',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'get_measurement_unit')
    list_per_page = LINES_PER_PAGE

    @admin.display(description='measurement unit')
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'recipe_description', 'cooking_time')
    list_filter = ('author',)
    list_per_page = LINES_PER_PAGE
    search_fields = ('name',)

    def recipe_description(self, obj):
        return obj.text[:300] + '...'


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
