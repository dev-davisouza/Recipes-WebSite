from unittest import TestCase
from recipes.views import PER_PAGE


class EnviromentVariablesTest(TestCase):
    def test_constant_PER_PAGE_loads_correct_value(self):
        self.assertIs(PER_PAGE, 6)
