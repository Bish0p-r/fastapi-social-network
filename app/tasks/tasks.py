import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_template import create_email_confirmation_template


@celery.task
def send_confirmation_email(email_to: EmailStr, verification_url: str):
    msg_content = create_email_confirmation_template(email_to, verification_url)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp.send_message(msg_content)
