from django.shortcuts import render
from utils.recipes.factory import make_recipe


def home(request):
    context = {'recipes': [make_recipe() for _ in range(10)], }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    context = {'recipe': make_recipe()}
    return render(request, 'recipes/pages/recipe.html', )
