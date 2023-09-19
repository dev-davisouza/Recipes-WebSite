from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorsRegisterViews(DjangoTestCase):
    def test_if_the_view_post_method_control_get_responses(self):
        view = reverse('authors:treat')
        response = self.client.get(view)
        self.assertTemplateUsed(response, 'recipes/pages/404_error.html')

    # def test_if_treat_view_creates_a_user_object:
