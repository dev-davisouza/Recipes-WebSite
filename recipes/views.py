import os
from django.shortcuts import render
from recipes.models import Recipe, Category
from django.db.models import Q
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def category(request, category_name):
    recipes = Recipe.objects.filter(
        category__name=category_name, is_published=True)

    if not recipes:
        response = render(request, 'recipes/pages/404_error.html',
                          context={"title": "Category not found | ",
                                   "category_404": "Category does not exists",
                                   "is_category": True})
        response.status_code = 404
        return response
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    context = {'recipes': page_obj,
               'pagination_range': pagination_range,
               'title': f'{recipes.first().category.name} | ',
               }
    return render(request, 'recipes/pages/category.html', context, status=200)


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-created_at')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    context = {'recipes': page_obj,
               'not_recipes': True,
               'pagination_range': pagination_range, }

    if not recipes:
        return render(request, 'recipes/pages/404_error.html', context,
                      status=404)
    return render(request, 'recipes/pages/home.html', context, status=200)


def recipe(request, slug):
    context = {}
    if Recipe.objects.filter(slug=slug).exists():
        recipe = Recipe.objects.get(slug=slug)
        context = {
            'recipe': recipe,
            'title': f'{recipe.title} | ',
            'is_detail_page': True,
        }
        return render(request, 'recipes/pages/recipe.html', context)
    else:
        response = render(request, 'recipes/pages/404_error.html',
                          context={"title": "Recipe not found | ",
                                   'is_detail_page': True, })
        response.status_code = 404
        return response


def search(request):
    search_term = request.GET.get("q")
    if search_term is not None:
        search_term = search_term.strip()
    else:
        search_term = ""
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    )

    if not search_term or not recipes:
        return render(request, 'recipes/pages/404_error.html', status=404,
                      context={
                          "search_term": search_term,
                          "search_query": True,
                          "title": "Recipes not found | ",
                      })

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'global/pages/search.html', context={
        "title": f"search for '{search_term}' | ",
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
        "search_term": search_term,
    })
