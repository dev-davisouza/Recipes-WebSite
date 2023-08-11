from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsCategoryTest(RecipeTestBase):
    def test_recipe_category_view_is_correct(self):
        # Getting the view by the URL with args
        view = resolve(
            reverse('recipes:category', args=(1,))
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:category', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_status_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:category', args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_loads_correct_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:category', args=(1,)))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_view_loads_correct_template_if_404_not_found(self):  # noqa
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:category', args=(1000,)))
        self.assertTemplateUsed(response, 'recipes/pages/404_error.html')

    def test_context_if_not_recipes_404_not_found(self):
        expected_context = {"title": "Category not found | ",
                            "category_404": "Category does not exists",
                            "is_category": True}

        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:category', args=(1000,)))
        context = response.context
        self.assertDictContainsSubset(expected_context, context)
