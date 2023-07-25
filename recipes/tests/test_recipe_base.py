from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User
from recipes import models


class RecipeTestBase(TestCase):
    """
    The function below creates test objects so that they can be tested
    in other test functions, because there are some rules in the views that
    might cause the tests to return unexpected values when working with empty
    QuerySets.
    """

    def setUp(self):  # This is a fixture
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_login(self.user)

        # Create a Category object test
        self.category = models.Category.objects.create(name='Asiáticas', id=1)

        '''
        NOTE: The attr servings_unit generate an error
            if the first character isn't a uppercase letter.
            I don't know why, but it happens!
        '''
        # Create a Recipe object with the attr is_published=True
        self.recipe = models.Recipe.objects.create(
            id=1,
            title='Bolo de Chocolate',
            description='Um delicioso bolo de chocolate',
            slug=slugify('Bolo de Chocolate'),
            preparation_time=60,
            preparation_time_unit='minutos',
            servings=12,
            servings_unit='Porções',
            preparation_steps='Passo 1: Misture os ingredientes ...',
            is_published=True,
            cover='recipes/covers/2023/07/06/user.webp',
            category=self.category,
            author=self.user
        )
