from django.test import TestCase
from django.contrib.auth.models import User
from recipes import models


class RecipeTestBase(TestCase):
    """
    The function below creates a Recipe test object that can be used in all
    classes that inherit from this class, the reason is, i want to simulate
    the situation where we have recipes to see, if we don't have available
    recipes, the tests will fail, because the views was created to give
    a response, a recipe or more! So, it's necessary have recipes.
    """

    def setUp(self):  # This is a fixture
        self.author = self.make_author()
        self.category = self.make_category()
        self.recipe = self.make_recipe(
            author=self.author, category=self.category)
        return super().setUp()

    def make_category(self, name="Category"):
        return models.Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='12345',
                    email='user@gmail.com',
                    id=1,
                    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            id=id
        )

    '''
    NOTE: The attr servings_unit generate an error
        if the first character isn't a uppercase letter.
        I don't know why, but it happens!
    '''

    def make_recipe(self,
                    title='Bolo de Chocolate',
                    description='Um delicioso bolo de chocolate',
                    slug="test-recipe",
                    preparation_time=60,
                    preparation_time_unit='minutos',
                    servings=12,
                    servings_unit='Porções',
                    preparation_steps='Passo 1: Misture os ingredientes ...',
                    is_published=True,
                    cover='recipes/covers/2023/07/06/user.webp',
                    category=None,
                    author=None,
                    preparation_steps_is_html=True,):

        if category is None:
            category = self.make_category()

        if author is None:
            author = self.make_author()

        return models.Recipe.objects.create(
            title=title,
            description=description,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            slug=slug,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            is_published=is_published,
            cover=cover,
            category=category,
            author=author,
            preparation_steps_is_html=preparation_steps_is_html
        )
