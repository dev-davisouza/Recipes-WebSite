from django.urls import reverse
from .test_authors_base import AuthorsTestBase, User


class AuthorsRegisterViews(AuthorsTestBase):
    def test_if_the_view_post_method_control_get_responses(self):
        view = reverse('authors:treat')
        response = self.client.get(view)
        self.assertTemplateUsed(response, 'recipes/pages/404_error.html')

    def test_traet_view_redirects_correctly(self):
        url_add_user = reverse('authors:add_user')

        url_treat_post = reverse('authors:treat')

        response = self.client.post(
            url_treat_post, data=self.form_data, follow=True)

        # Verify if the redirection was happened with success
        self.assertRedirects(response, url_add_user)

    def test_traet_view_creates_a_user_correctly(self):

        # Verify the number of users before call the view function
        initial_user_count = User.objects.count()

        # Geting the treat_post view by url
        url_treat_post = reverse('authors:treat')

        # Posting the data
        self.client.post(url_treat_post, data=self.form_data, follow=True)

        # Verify the number of user after call the view function
        final_user_count = User.objects.count()

        # Assertion
        self.assertEqual(final_user_count, initial_user_count + 1)
