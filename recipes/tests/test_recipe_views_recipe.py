from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_detail_view_is_correct(self):
        # Getting the view by the URL with kwargs
        view = resolve(
            reverse('recipes:recipe', kwargs={'slug': "Temaki"})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'slug': "test-recipe"}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_status_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(
            reverse('recipes:recipe', args=("louco-e-sonhador",)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_template_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(
            reverse('recipes:recipe', args=("louco-e-sonhador",)))
        self.assertTemplateUsed(response, 'recipes/pages/404_error.html')

    def test_recipe_detail_view_loads_correct_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'slug': "test-recipe"}))
        self.assertTemplateUsed(response, 'recipes/pages/recipe.html')
