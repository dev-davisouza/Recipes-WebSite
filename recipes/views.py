from django.shortcuts import render
from utils.recipes.factory import make_recipe
from .models import Recipe


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id)
    context = {'recipes': recipes, }
    return render(request, 'recipes/pages/home.html', context)


def home(request):
    recipes = Recipe.objects.all().order_by('updated_at')
    context = {'recipes': recipes, }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    context = {'recipe': make_recipe(),
               'is_detail_page': True, }
    return render(request, 'recipes/pages/recipe.html', context)
