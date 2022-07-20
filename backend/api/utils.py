from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            RecipeInCart, Recipes)


def add_delete_obj(request, pk, serializer_obj, model_obj):
    recipe = Recipes.objects.get(pk=pk)
    data = {'user': request.user.pk, 'recipe': recipe.pk}
    serializer = serializer_obj(context={'request': request}, data=data)
    serializer.is_valid(raise_exception=True)
    if request.method == 'POST':
        try:
            serializer.save()
            short_query = Recipes.objects.get(pk=recipe.pk)
            from api.serializers import ShortRecipesSerializer
            returned_data = ShortRecipesSerializer(instance=short_query)
            return Response(returned_data.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError({'errors': 'Recipe already added.'})
    elif request.method == 'DELETE':
        obj_to_delete = model_obj.objects.filter(**data)
        if obj_to_delete.exists():
            obj_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'No such object.'},
                        status=status.HTTP_400_BAD_REQUEST)


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


def download_shopping_cart(request):
    query_set = RecipeInCart.objects.filter(user=request.user)
    if not query_set.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)
    from api.serializers import CartSerializer
    cart_serializer_data = CartSerializer(query_set, many=True).data
    shopping_cart = {}
    for recipe in cart_serializer_data:
        recipe_id = recipe.get('recipe')
        ingredients_query = IngredientInRecipe.objects.filter(
            recipe_id=recipe_id)
        from api.serializers import IngredientInRecipeSerializer
        ingredients_data = IngredientInRecipeSerializer(ingredients_query,
                                                        many=True).data
        for ingredient in ingredients_data:
            name = ingredient.get('name')
            measurement_unit = ingredient.get('measurement_unit')
            amount = ingredient.get('amount')
            if name not in shopping_cart:
                shopping_cart[name] = [measurement_unit, amount]
            else:
                shopping_cart[name][1] += amount
    result_list = []
    for item in shopping_cart.items():
        result_list.append('{0} ({1}) - {2}\n'.format(item[0], item[1][0],
                                                      item[1][1]))
    file_name = '{}_shop_list.txt'.format(request.user)
    response = HttpResponse(result_list, status=None)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        file_name)
    return response
