from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def send_otp_email(email, otp):
    subject = _("Your OTP code for Login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }
    print("context", context)

    html_email = render_to_string("emails/otp_email.html", context=context)
    plain_email = strip_tags(html_email)
    composed_email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list) 
    composed_email.attach_alternative(html_email, mimetype="text/html")

    try:
        composed_email.send()
        logger.info(f"OTP email sent successfully to: {email}")
    except Exception as email_error:
        logger.error(f"Failed to send OTP email to {email}: Error: {str(email_error)}")


def send_account_locked_email(user):
    subject = _("Your account has been locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    context = {
        "user": user,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME,
    }

    html_email = render_to_string("emails/account_locked.html", context=context)
    plain_email = strip_tags(html_email)
    composed_email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list) 
    composed_email.attach_alternative(html_email, mimetype="text/html")

    try:
        composed_email.send()
        logger.info(f"account locked email sent to: {user.email}")
    except Exception as email_error:
        logger.error(f"Failed to send account locked email to {user.email}: Error: {str(email_error)}")