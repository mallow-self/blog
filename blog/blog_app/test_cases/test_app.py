from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ..models import Blog
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile


class AuthenticationTest(TestCase):
    def setUp(self):
        # Create required groups
        self.author_group = Group.objects.create(name="Author1")
        self.editor_group = Group.objects.create(name="Editor1")
        self.publisher_group = Group.objects.create(name="Publisher1")

        # Create test users
        self.author_user = User.objects.create_user(
            username="author@test.com",
            email="author@test.com",
            password="testpassword",
            first_name="Author",
            last_name="User",
        )
        self.author_user.groups.add(self.author_group)

        self.editor_user = User.objects.create_user(
            username="editor@test.com",
            email="editor@test.com",
            password="testpassword",
            first_name="Editor",
            last_name="User",
        )
        self.editor_user.groups.add(self.editor_group)

        self.publisher_user = User.objects.create_user(
            username="publisher@test.com",
            email="publisher@test.com",
            password="testpassword",
            first_name="Publisher",
            last_name="User",
        )
        self.publisher_user.groups.add(self.publisher_group)

        # User with multiple roles
        self.multi_role_user = User.objects.create_user(
            username="multi@test.com",
            email="multi@test.com",
            password="testpassword",
            first_name="Multi",
            last_name="Role",
        )
        self.multi_role_user.groups.add(self.author_group, self.editor_group)

        # Create test client
        self.client = Client()

    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(
            reverse("blog:register"),
            {
                "full_name": "New User",
                "email": "newuser@test.com",
                "user_group": self.author_group.id,
                "password1": "complex_password123",
                "password2": "complex_password123",
            },
        )

        # Check redirect to login page
        self.assertRedirects(response, reverse("blog:login"))

        # Check user was created
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())

        # Check user was added to the group
        new_user = User.objects.get(email="newuser@test.com")
        self.assertTrue(new_user.groups.filter(name="Author1").exists())

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(
            reverse("blog:login"),
            {"email": "author@test.com", "password": "testpassword"},
        )

        # Check redirect to blog list page
        self.assertRedirects(response, reverse("blog:blog_list"))

        # Check user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        """Test failed login"""
        response = self.client.post(
            reverse("blog:login"),
            {"email": "author@test.com", "password": "wrongpassword"},
        )

        # Check user remains on login page
        self.assertEqual(response.status_code, 200)

        # Check user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """Test logout functionality"""
        # First login
        self.client.login(username="author@test.com", password="testpassword")

        # Then logout
        response = self.client.get(reverse("blog:logout"))

        # Check redirect to login page
        self.assertRedirects(response, reverse("blog:login"))

        # Check user is not authenticated after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users are redirected to login page"""
        # Try to access protected page without login
        response = self.client.get(reverse("blog:blog_list"))

        # Check redirect to login page with next parameter
        self.assertRedirects(
            response, f"{reverse('blog:login')}?next={reverse('blog:blog_list')}"
        )
