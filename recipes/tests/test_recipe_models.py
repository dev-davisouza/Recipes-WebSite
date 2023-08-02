from .test_recipe_base import RecipeTestBase, models
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    """
    In the test_recipe_base.py base file I created the setUp method
    that creates a Recipe object that can be used in the all classes that
    inherit of the RecipeTestBase class, but there we have different values
    from the default, for one side it's useful but for another side this can
    be not useful, so below i create here a method that can creates a Recipe
    object with values by default defined in the model.
    """

    def make_recipe_by_defaults(self):
        return models.Recipe.objects.create(
            title="Default Recipe",
            description="It's a default recipe...",
            preparation_time=1,
            preparation_time_unit="seconds",
            servings=1,
            servings_unit="Or infinites tests!",
            preparation_steps="Call me and i'm will be created!",
            category=self.make_category(name="Default test category"),
            author=self.make_author(username="Admin"),
        )
    """
    The next two functions (tests) will test the validation of the `max_length`
    parameter. The first one, just below, manually tests only one attribute,
    while the second one below tests multiple attributes using the external
    library "parameterized." This library takes tuples containing the fields
    and arguments passed to the parameters of each field, consequently
    generating a more automated code instead of repetitive code. Additionally,
    it separates each field as different tests, which will allow me to find
    errors specific to the particular field instead of returning a single
    error where I wouldn't know exactly where the error occurred!
    """

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = "A" * 70
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_preparation_steps_is_html_field_is_false_by_default(self):
        recipe = self.make_recipe_by_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg="This field is not False")

    def test_is_published_field_is_false_by_default(self):
        recipe = self.make_recipe_by_defaults()
        self.assertFalse(recipe.is_published,
                         msg="This field is not False")

    def test_recipe_string_representation(self):
        recipe = self.make_recipe_by_defaults()
        needed = recipe.title
        self.assertEqual(str(recipe), needed,
                         msg=f"Recipe string representation must be '{needed}'")

    def test_category_string_representation(self):
        category = self.make_category(name="Default")
        needed = category.name
        self.assertEqual(str(category), needed,
                         msg=f"Recipe string representation must be '{needed}'")

    def test_slug_is_generated(self):
        recipe = self.make_recipe(title="title slug")
        self.assertIsNotNone(recipe.slug)
        self.assertEqual(recipe.slug, "title-slug")

    def test_unique_slug_generation(self):
        recipe1 = self.make_recipe(title="Like this")
        recipe2 = self.make_recipe(title="Like this")
        self.assertNotEqual(recipe1.slug, recipe2.slug)

    def test_unique_slug_generation_on_save(self):
        # Crie um novo objeto Recipe com o mesmo slug
        recipe2 = self.make_recipe(
            title="Another Recipe", slug="test-recipe")

        # Verifique se a slug é atualizada para um valor único
        recipe2.save()
        # Verifica se o slug foi alterado
        self.assertNotEqual(recipe2.slug, self.recipe.slug)

    def test_slug_generation_when_not_have_slug(self):
        # Crie um objeto Recipe com título "Test Recipe"
        recipe1 = self.make_recipe(slug=None)
        recipe1.save()
        self.assertTrue(recipe1.slug is not None)
