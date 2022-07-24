from django.db import IntegrityError
from django.db.models import F, Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Follow, IngredientInRecipe,
                            RecipeInCart, Recipes,)


def add_delete_obj(request, pk, serializer_obj, model_obj):
    """
    Performs the addition or removal (depending on the method) of an object
    based on the serialized data. Changes output data according to
    ShortRecipesSerializer.
    """
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
    return Response({'errors': 'Method is not allowed.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_obj_of_current_user(serializer, instance, model, method):
    """
    Returns the boolean value of the existence of an instance in the
    database when using the exists method. With the count method, it counts
    the number of instance entity objects.
    """
    user = serializer.context.get('request').user
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
    """
    A .txt file with a shopping list for the user who sent the request is
    sent to the response.
    """
    user = request.user
    name = 'ingredient__name'
    units = 'ingredient__measurement_unit'
    amount = 'amount'
    result_list = []

    ingredients = IngredientInRecipe.objects.filter(
        recipe__recipe_in_cart__user=user).order_by(name)
    ingredient_list = ingredients.values(name, units).annotate(
        name=F(name), units=F(units), amount=Sum(amount)).order_by('-amount')
    for ingredient in ingredient_list:
        result_list.append('{} ({}) - {}'.format(
            ingredient.get(name), ingredient.get(units), ingredient.get(amount)
        ))

    file_name = '{}_shop_list.txt'.format(request.user)
    response = HttpResponse('\n'.join(result_list), status=None)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        file_name)
    return response
