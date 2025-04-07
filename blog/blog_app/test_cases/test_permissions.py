from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ..models import Blog
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile


class BlogPermissionsTest(TestCase):
    def setUp(self):
        # Create required groups
        self.author_group, _ = Group.objects.get_or_create(name="Author")
        self.editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.publisher_group, _ = Group.objects.get_or_create(name="Publisher")

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

        # Create a test blog post
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"",  # Empty content for testing
            content_type="image/jpeg",
        )

        self.blog = Blog.objects.create(
            title="Test Blog",
            content="Test content",
            image=image,
            category="python",
            author=self.author_user,
            editor=self.editor_user,
            publisher=self.publisher_user,
        )

        # Create test client
        self.client = Client()

    def test_author_permissions(self):
        """Test that authors can create posts but not edit or delete"""
        # Login as author
        self.client.login(username="author@test.com", password="testpassword")

        # Test can view blog list
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)

        # Test can view blog detail
        response = self.client.get(reverse("blog:detail", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

        # Test can access create form
        response = self.client.get(reverse("blog:blog_create"))
        self.assertEqual(response.status_code, 200)

        # Test cannot access edit form
        response = self.client.get(reverse("blog:blog_update", args=[self.blog.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test cannot delete blog
        response = self.client.post(reverse("blog:blog_delete", args=[self.blog.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_editor_permissions(self):
        """Test that editors can create and edit posts but not delete"""
        # Login as editor
        self.client.login(username="editor@test.com", password="testpassword")

        # Test can view blog list
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)

        # Test can view blog detail
        response = self.client.get(reverse("blog:detail", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

        # Test can access create form
        response = self.client.get(reverse("blog:blog_create"))
        self.assertEqual(response.status_code, 200)

        # Test can access edit form
        response = self.client.get(reverse("blog:blog_update", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

        # Test cannot delete blog
        response = self.client.post(reverse("blog:blog_delete", args=[self.blog.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_publisher_permissions(self):
        """Test that publishers can create, edit, and delete posts"""
        # Login as publisher
        self.client.login(username="publisher@test.com", password="testpassword")

        # Test can view blog list
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)

        # Test can view blog detail
        response = self.client.get(reverse("blog:detail", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

        # Test can access create form
        response = self.client.get(reverse("blog:blog_create"))
        self.assertEqual(response.status_code, 200)

        # Test can access edit form
        response = self.client.get(reverse("blog:blog_update", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

        # Test can delete blog
        response = self.client.post(reverse("blog:blog_delete", args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)  # Success response for AJAX

        # Verify blog was deleted
        self.assertEqual(Blog.objects.filter(id=self.blog.id).count(), 0)

    # def test_create_blog_notification(self):
    #     """Test that an email is sent to the publisher when a blog is created"""
    #     # Login as author
    #     self.client.login(username="author@test.com", password="testpassword")

    #     # Create a new blog post
    #     image = SimpleUploadedFile(
    #         name="test_image2.jpg",
    #         content=b"",  # Empty content for testing
    #         content_type="image/jpeg",
    #     )

    #     response = self.client.post(
    #         reverse("blog:blog_create"),
    #         {
    #             "title": "New Test Blog",
    #             "content": "New test content",
    #             "image": image,
    #             "category": "django",
    #             "author": self.author_user.id,
    #             "editor": self.editor_user.id,
    #             "publisher": self.publisher_user.id,
    #         },
    #         HTTP_X_REQUESTED_WITH="XMLHttpRequest",  # Simulate AJAX request
    #     )

    #     # Check email was sent
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].to, [self.publisher_user.email])
    #     self.assertTrue("New Test Blog" in mail.outbox[0].subject)
