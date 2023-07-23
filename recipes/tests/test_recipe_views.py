from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views, models
from django.utils.text import slugify
from django.contrib.auth.models import User


class RecipeViewsTest(TestCase):
    """
    The function below creates test objects so that they can be tested
    in other test functions, because there are some rules in the views that
    might cause the tests to return unexpected values when working with empty
    QuerySets.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_login(self.user)

        # Create a Category object test
        self.category = models.Category.objects.create(name='Asiáticas', id=1)

        # Create an Recipe object with the attr is_published=True
        self.recipe = models.Recipe.objects.create(
            title='Bolo de Chocolate',
            description='Um delicioso bolo de chocolate',
            slug=slugify('Bolo de Chocolate'),
            preparation_time=60,
            preparation_time_unit='minutos',
            servings=12,
            servings_unit='porções',
            preparation_steps='Passo 1: Misture os ingredientes ...',
            preparation_steps_is_html=False,
            is_published=True,
            cover='recipes/covers/2023/07/06/user.webp',
            category=self.category,
            author=self.user
        )

    # -------------------- Home Section --------------------

    def test_recipe_home_view_is_correct(self):
        # Getting the view by the URL
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_200_OK(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_returns_status_404_Not_Found(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_view_loads_correct_template(self):
        # Getting the HTTP response object by the URL
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

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
