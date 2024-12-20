from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post
from blog.forms import PostForm

class PostNewViewTest(TestCase):
    def setUp(self):
        # Cria usuario e faz login
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_post_new_get_request(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_new_post_valid_data(self):
        valid_data = {
            'title': 'New Post Title',
            'content': 'New Post Content',
        }
        response = self.client.post(reverse('post_new'), data=valid_data)
        # Check redirection to post detail
        new_post = Post.objects.last()
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': new_post.pk}))
        self.assertEqual(new_post.title, 'New Post Title')
        self.assertEqual(new_post.content, 'New Post Content')
        self.assertEqual(new_post.author, self.user)

    def test_post_new_post_invalid_data(self):
        invalid_data = {
            'title': '', 
            'content': 'New Post Content',
        }
        response = self.client.post(reverse('post_new'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_new_requires_login(self):
        # Test that login is required to access the view
        self.client.logout()
        new_url = reverse('post_new')
        login_url = reverse('login')
        expected_url = f"{login_url}?next={new_url}"
        response = self.client.get(new_url)
        self.assertRedirects(response, expected_url)


class PostEditViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # cria um post
        self.post = Post.objects.create(title='Original Title', content='Original Content', author=self.user)

    def test_post_edit_get_request(self):
        response = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertEqual(response.context['post'], self.post)

    def test_post_edit_post_valid_data(self):
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
        }
        response = self.client.post(reverse('post_edit', kwargs={'pk': self.post.pk}), data=updated_data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated Content')

    def test_post_edit_post_invalid_data(self):
        invalid_data = {
            'title': '',  
            'content': 'Updated Content',
        }
        response = self.client.post(reverse('post_edit', kwargs={'pk': self.post.pk}), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertTrue(response.context['form'].errors)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Original Title')

    def test_post_edit_invalid_post(self):
        response = self.client.get(reverse('post_edit', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_post_edit_requires_login(self):
        self.client.logout()
        edit_url = reverse('post_edit', kwargs={'pk': self.post.pk})
        login_url = reverse('login')
        expected_url = f"{login_url}?next={edit_url}"
        response = self.client.get(edit_url)
        self.assertRedirects(response, expected_url)


class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_delete_get_request(self):
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_post_delete_post_request(self):
        response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, reverse('post_list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_invalid_post(self):
        response = self.client.post(reverse('post_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_requires_login(self):
        self.client.logout()
        delete_url = reverse('post_delete', kwargs={'pk': self.post.pk})
        login_url = reverse('login')
        expected_url = f"{login_url}?next={delete_url}"
        response = self.client.get(delete_url)
        self.assertRedirects(response, expected_url)


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post1 = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author=self.user)
        self.post3 = Post.objects.create(title='Post 3', content='Content 3', author=self.user)

    def test_post_list_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_template_used(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_context(self):
        response = self.client.get(reverse('post_list'))
        self.assertIn('posts', response.context)
        self.assertEqual(list(response.context['posts']), list(Post.objects.all().order_by('-created_at')))


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Post Title', content='Post Content', author=self.user)

    def test_post_detail_status_code(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_used(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_context(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertIn('post', response.context)
        self.assertEqual(response.context['post'], self.post)

    def test_post_detail_invalid_post(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


