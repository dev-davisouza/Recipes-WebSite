from django.shortcuts import render
from .models import Recipe


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
        is_published=True).order_by('updated_at')
    context = {'recipes': recipes,
               'not_recipes': True, }
    if not recipes:
        return render(request, 'recipes/pages/404_error.html', context,
                      status=404)
    return render(request, 'recipes/pages/home.html', context, status=200)


def recipe(request, id):
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
    search_term = request.GET.get("q").strip()
    recipes = Recipe.objects.filter(
        title__icontains=search_term,
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
