from django.conf import settings
from blog_app.tasks import send_email


def review_mail(object):
    """
    Sends a review notification email to the blog's publisher and editor.

    Notifies the responsible parties that a new blog post has been created
    and is pending review, including key blog details in the message.

    Args:
        object (Blog): The blog instance that has been created.

    Returns:
        None
    """
    publisher = object.publisher
    editor = object.editor
    subject = f"New Blog Post Created: {object.title}"
    message = f"""
                A new blog post has been created and requires your attention:
                
                Title: {object.title}
                Category: {object.category}
                Author: {object.author.get_full_name() or object.author.username}
                Editor: {object.editor.get_full_name() or object.editor.username}
                
                Please review the content at your earliest convenience.
                """
    # sending email from celery to editor and publisher
    send_email.delay(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,publisher_email=[publisher.email,editor.email])

def delete_mail(object):
    """
    Sends a deletion notification email to the blog's editor and author.

    Notifies the relevant parties that a blog post has been deleted,
    including details about the blog and the user who performed the deletion.

    Args:
        object (Blog): The blog instance that was deleted.

    Returns:
        None
    """
    editor = object.editor
    author = object.author
    subject = f"Blog Post Deleted: {object.title}"
    message = f"""
                A blog post has been deleted by {object.publisher.username}:
                
                Title: {object.title}
                Category: {object.category}
                Author: {object.author.get_full_name() or object.author.username}
                Editor: {object.editor.get_full_name() or object.editor.username}
                
                """
    # sending email from celery to editor and publisher
    send_email.delay(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        publisher_email=[editor.email, author.email],
    )

def update_mail(object):
    """
    Sends an update notification email to the blog's publisher and author.

    Alerts relevant users that a blog post has been updated, including blog details
    and a prompt to review the changes.

    Args:
        object (Blog): The blog instance that has been updated.

    Returns:
        None
    """
    publisher = object.publisher
    author = object.author
    subject = f"Blog Post Updated: {object.title}"
    message = f"""
                A blog post has been updated and requires your attention:
                
                Title: {object.title}
                Category: {object.category}
                Author: {object.author.get_full_name() or object.author.username}
                Editor: {object.editor.get_full_name() or object.editor.username}
                
                Please review the content at your earliest convenience.
                """
    # sending email from celery to editor and publisher
    send_email.delay(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        publisher_email=[publisher.email, author.email],
    )
