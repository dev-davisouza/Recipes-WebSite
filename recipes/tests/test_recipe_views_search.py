from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsSearchTest(RecipeTestBase):
    def test_search_view_is_correct(self):
        # Getting the view by the URL
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_view_loads_correct_template(self):
        """
        The function search from recipe app does what it's name says,
        it's a search funcionality. In our case we just have one
        recipe available to use in our querys, this recipe recived
        the title "Bolo de chocolate", that means chocolate cake in
        portuguese. Yes, we can make more recipes, we have functions
        that creates a Recipe object, but in this case it's not
        necessary, because for the test pass or not, we just need
        pass an argument that exists or not. For more info, see
        the view search in views.py file.
        """
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:search') + "?q=Bolo")
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_search_view_loads_correct_template_if_404_not_found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:search') + "?q=Temaki")
        self.assertTemplateUsed(response, 'recipes/pages/404_error.html')

    def test_search_view_loads_correct_title_on_template_if_404_not_found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:search') + "?q=Temaki")
        expected_title = "Recipes not found | "
        content = response.content.decode("utf-8")
        self.assertIn(expected_title, content)

    def test_search_view_returns_status_404_Not_Found(self):
        # Getting the URL
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_view_returns_status_200_OK(self):
        # Getting the URL with QueryString
        response = self.client.get(reverse('recipes:search') + "?q=Bolo")
        self.assertEqual(response.status_code, 200)

    def test_if_search_can_find_recipes(self):
        response = self.client.get(reverse('recipes:search') + "?q=Bo")
        content = response.content.decode("utf-8")
        self.assertIn("Bolo", content)
