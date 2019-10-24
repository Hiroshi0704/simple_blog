from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Comment

User = get_user_model()


class BaseTestPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            user = User.objects.create(
                username=f'user{i}',
                email=f'user{i}@exmaple.com',
            )
            user.set_password('pass12345')
            user.save()


        for i in range(5):
            Post.objects.create(
                title=f'post{i}',
                body=f'body{i}',
                author=User.objects.get(pk=i+1)
            )


class TestPostListView(BaseTestPostView):

    def test_get_success(self):
        response = self.client.get('/blog/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_url_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')


class TestPostDetailView(BaseTestPostView):

    def test_get_success(self):
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_url_name(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_none_comment(self):
        response = self.client.get('/blog/1/')
        self.assertFalse(response.context['comment_list'])


class TestPostCreateView(BaseTestPostView):

    def setUp(self):
        self.user = User.objects.get(username='user1')

    def test_login(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)


    def test_get_page_without_login(self):
        response = self.client.get('/blog/create/')
        self.assertRedirects(response, '/users/login/?next=/blog/create/')

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_success(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        response = self.client.post('/blog/create/', {
            'title': 'testtitle',
            'body': 'testbody',
        })
        self.assertRedirects(response, '/blog/6/')
        post = Post.objects.get(pk=6)
        self.assertTrue(post)
        self.assertEqual(post.title, 'testtitle')
        self.assertEqual(post.body, 'testbody')
        self.assertEqual(post.author, self.user)

    def test_post_without_title(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        response = self.client.post(reverse('post_create'), {
            'title': '',
            'body': 'testbody',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'title', 'This field is required.')


    def test_post_without_body(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        self.assertFalse(Post.objects.filter(id=6).exists())

        response = self.client.post(reverse('post_create'), {
            'title': 'testtitle',
            'body': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'body', 'This field is required.')



class TestPostDeleteView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@example.com')
        user.set_password('pass12345')
        user.save()

        Post.objects.create(
            title='testtitle',
            body='testbody',
            author=user
        )
        



    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.post = Post.objects.get(author=self.user)

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('post_delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/blog/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_get_without_login(self):
        response = self.client.get('/blog/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/1/delete/')

    def test_get_by_other_user(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        response = self.client.get('blog/2/delete')
        self.assertEqual(response.status_code, 404)

    def test_post_success(self):
        logged_in = self.client.login(username=self.user.username, password='pass12345')
        self.assertTrue(logged_in)
        response = self.client.post(f'/blog/{self.post.id}/delete/')
        self.assertRedirects(response, '/blog/list/')
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
