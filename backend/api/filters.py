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
            return queryset.filter(recipe_in_cart__buyer=self.request.user)
        return queryset


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ('name',)
