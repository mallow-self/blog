from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Blog
from django.utils import timezone


@shared_task
def send_email(subject,message,from_email,publisher_email):
    print(f"Sending notification to {publisher_email}")
    return send_mail(
        subject,
        message,
        from_email,
        publisher_email,
        fail_silently=False,
    )


@shared_task 
def daily_mail_users():
    print("email starting...")
    users = User.objects.all().values_list('email',flat=True)
    recent_blogs = Blog.objects.order_by("-created_at")[:3]
    blog_titles = "\n".join([f"👉 {blog.title}" for blog in recent_blogs])
    subject = f"Exciting new blogs"
    message = f"""
                Hi Users,

                We’re thrilled to share that some exciting new blog posts are now live on our website! Whether you're looking for insights, tips, or a dose of inspiration, there's something for everyone.

                Check out the latest content and stay up to date with what's new:
                {blog_titles}

                We’d love to hear your thoughts—feel free to leave a comment or share with others who might find them helpful.

                Happy reading!
                Blog App
                """
    from_email = (settings.DEFAULT_FROM_EMAIL,)
    recipient_list = list(users)

    # sending email to users using cronjob daily
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def publish_scheduled_blogs():
    now = timezone.now()
    blogs = Blog.objects.filter(is_published=False, publish_at__lte=now)
    for blog in blogs:
        blog.is_published = True
        blog.save()
        publish_mail(blog)


def publish_mail(object):
    author = object.author
    editor = object.editor
    subject = f"Blog Post Published: {object.title}"
    message = f"""
                Your Blog post has been published!
                
                Title: {object.title}
                Category: {object.category}
                Author: {object.author.get_full_name() or object.author.username}
                Editor: {object.editor.get_full_name() or object.editor.username}
                
                """
    # sending email from celery to editor and author
    send_email.delay(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        publisher_email=[author.email, editor.email],
    )
