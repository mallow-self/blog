from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Blog
from django.utils import timezone
from .custom_exceptions import EmailSendingError


@shared_task
def send_email(subject,message,from_email,publisher_email):
    """
    Sends an email notification to the specified publisher using Django's send_mail function.

    Args:
        subject (str): Subject line of the email.
        message (str): Body content of the email.
        from_email (str): Sender's email address.
        publisher_email (str): Recipient publisher's email address.

    Returns:
        int: The number of successfully delivered messages (1 if successful, 0 otherwise).
    """
    print(f"Sending notification to {publisher_email}")
    try:
        return send_mail(
            subject,
            message,
            from_email,
            publisher_email,  # should be a list
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email to {publisher_email}: {e}")
        raise EmailSendingError(str(e), publisher_email)


@shared_task 
def daily_mail_users():
    """
    Sends a daily email to all registered users containing the three most recent blog titles.

    This task retrieves all user email addresses and the latest three blog posts,
    formats them into an email message, and sends it using Django's send_mail function.
    Intended to be triggered by a daily cron job.

    Returns:
        int: The number of successfully delivered messages.
    """
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
    """
    Publishes blogs that are scheduled to go live.

    This task checks for blogs that are not yet published but have a `publish_at` timestamp
    less than or equal to the current time. It marks them as published and sends a
    notification email for each published blog.

    Returns:
        None
    """
    now = timezone.now()
    blogs = Blog.objects.filter(is_published=False, publish_at__lte=now)
    for blog in blogs:
        blog.is_published = True
        blog.save()
        publish_mail(blog)


def publish_mail(object):
    """
    Sends a publication notification email to the blog's author and editor.

    Constructs an email message with blog details such as title, category, author, and editor,
    and sends it asynchronously using the `send_email` task.

    Args:
        object (Blog): The blog instance that has been published.

    Returns:
        None
    """
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
