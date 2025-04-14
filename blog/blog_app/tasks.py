from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Blog

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


