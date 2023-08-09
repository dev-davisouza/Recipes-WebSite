from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsHomeTest(RecipeTestBase):
    def test_recipe_home_view_is_correct(self):
        # Getting the view by the URL
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_returns_status_404_Not_Found(self):
        self.recipe.delete()  # Delete the recipe
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_view_loads_correct_template_if_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_loads_correct_template_if_status_404_not_found(self):
        self.recipe.delete()  # Delete the recipe
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            response, 'recipes/pages/404_error.html')

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

    def test_home_template_do_not_loads_not_published_recipes(self):
        # Creating alternative User to avoid the IntegrityError
        alternative_user = self.make_author(id=2, username="Vlad")
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        recipe_2 = self.make_recipe(title="Bolo de peroba",
                                    is_published=False,
                                    author=alternative_user)
        self.assertNotIn(recipe_2.title, content)
