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
        '''
        NOTE: The attr servings_unit generate an error
            if the first character isn't a uppercase letter.
            I don't know why, but it happens!
        '''
        self.recipe = self.make_recipe()

    def make_category(self, name="Category"):
        return models.Category.objects.create(name=name, id=1)

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='12345',
                    email='user@gmail.com'
                    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,
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
                    category=None,
                    author=None):

        if category is None:
            category = self.make_category()

        if author is None:
            author = self.make_author()

        return models.Recipe.objects.create(
            id=id,
            title=title,
            description=description,
            slug=slug,  # Corrigido o uso do slugify
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            is_published=is_published,
            cover=cover,
            category=category,
            author=author,
        )
