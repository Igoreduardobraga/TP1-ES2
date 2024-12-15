from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class PostDeleteViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Log in the user
        self.client.login(username='testuser', password='password')
        # Create a post
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_delete_get_request(self):
        # Test GET request to post_delete view
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_post_delete_post_request(self):
        # Test POST request to post_delete view
        response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        # Check redirection to post list
        self.assertRedirects(response, reverse('post_list'))
        # Check that the post is deleted
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_invalid_post(self):
        # Test trying to delete a non-existent post
        response = self.client.post(reverse('post_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

# NOT WORKING, FIX LATER
#     def test_post_delete_requires_login(self):
#         # Test that login is required to access the view
#         self.client.logout()
#         response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
#         self.assertRedirects(response, f"/accounts/login/?next=/post_delete/{self.post.pk}/")
