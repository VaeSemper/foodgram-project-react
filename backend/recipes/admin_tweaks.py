from django import forms
from django.contrib import admin

from recipes.models import Recipes


class RequiredInlineFormSet(forms.BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class IngredientsInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1
    formset = RequiredInlineFormSet
