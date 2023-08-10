from django.shortcuts import render
from recipes.models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True)

    if not recipes:
        response = render(request, 'recipes/pages/404_error.html',
                          context={"title": "Category not found | ",
                                   "category_404": "Category does not exists",
                                   "is_category": True})
        response.status_code = 404
        return response

    context = {'recipes': recipes,
               'title': f'{recipes.first().category.name} | ',
               }
    return render(request, 'recipes/pages/category.html', context, status=200)


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-created_at')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 3)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )
    context = {'recipes': page_obj,
               'not_recipes': True,
               'pagination_range': pagination_range, }

    if not recipes:
        return render(request, 'recipes/pages/404_error.html', context,
                      status=404)
    return render(request, 'recipes/pages/home.html', context, status=200)


def recipe(request, id):
    context = {}
    if Recipe.objects.filter(pk=id).exists():
        recipe = Recipe.objects.get(pk=id)
        context = {'recipe': recipe,
                   'title': f'{recipe.title} | ',
                   'is_detail_page': True, }
        return render(request, 'recipes/pages/recipe.html', context)
    else:
        response = render(request, 'recipes/pages/404_error.html',
                          context.update({"title": "Recipe not found | "}))
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
                          "search_query": True,
                          "title": "Recipes not found | ",
                      })

    return render(request, 'recipes/pages/search.html', context={
        "title": f"search for '{search_term}' | ",
        "recipes": recipes,
    })
