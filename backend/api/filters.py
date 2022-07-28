from django.db import models
from django_filters import AllValuesMultipleFilter, rest_framework as filters

from recipes.models import Ingredients, Recipes


class RecipesFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipes
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(fav_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(recipe_in_cart__user=self.request.user)
        return queryset


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')

    class Meta:
        model = Ingredients
        fields = ('name',)

    def filter_name(self, queryset, name, value):
        q_exact = queryset.filter(name__iexact=value).annotate(
            q_ord=models.Value(0, models.IntegerField()))
        q_contains = queryset.filter(name__icontains=value).annotate(
            q_ord=models.Value(1, models.IntegerField()))
        return q_exact.union(q_contains).order_by('q_ord')
