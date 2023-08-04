from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        # Getting the URL
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        # Getting the URL with args
        url = reverse('recipes:category', args=(1,))
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_url_is_correct(self):
        # Getting the URL with kwargs
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_search_url_is_correct(self):
        # Getting the URL
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
