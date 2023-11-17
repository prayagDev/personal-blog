from django.core.mail import send_mail
import os

def send_email(to_email, subject, message):
    """
    Sends an email using the configured email settings.
    """
    email_host_user = os.getenv('EMAIL_HOST_USER')

    send_mail(
        subject,
        message,
        email_host_user,
        [to_email],
        fail_silently=False,
    )
