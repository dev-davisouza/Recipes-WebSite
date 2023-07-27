from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # -------------------- Home Section --------------------

    def test_recipe_home_view_is_correct(self):
        # Getting the view by the URL
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    """def test_recipe_home_view_returns_status_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 404)"""

    def test_recipe_home_view_loads_correct_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_loads_content_correctly_on_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        elements = [
            self.recipe.title,
            self.recipe.description,
            self.recipe.preparation_time,
            self.recipe.preparation_time_unit,
            self.recipe.servings,
            self.recipe.servings_unit,
            self.recipe.cover,
            self.recipe.category.name,
            self.recipe.author.first_name,
        ]
        # Check if each element is in the content string
        for element in elements:
            self.assertIn(str(element), content)

    # -------------------- Category Section --------------------

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

    # -------------------- Recipe Section --------------------

    def test_recipe_detail_view_is_correct(self):
        # Getting the view by the URL with kwargs
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_status_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:recipe', args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_loads_correct_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        self.assertTemplateUsed(response, 'recipes/pages/recipe.html')
