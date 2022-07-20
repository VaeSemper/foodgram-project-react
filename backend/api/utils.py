from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.serializers import ShortRecipesSerializer
from recipes.models import Recipes


def add_delete_obj(request, pk, serializer_obj, model_obj):
    recipe = Recipes.objects.get(pk=pk)
    data = {'user': request.user.pk, 'recipe': recipe.pk}
    serializer = serializer_obj(context={'request': request}, data=data)
    serializer.is_valid(raise_exception=True)
    if request.method == 'POST':
        try:
            serializer.save()
            short_query = Recipes.objects.get(pk=recipe.pk)
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
