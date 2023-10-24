from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings


def create_email_confirmation_template(
        email_to: EmailStr,
        verification_url: str
):
    email = EmailMessage()

    email["Subject"] = "Email confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Email confirmation</h1>
        Follow the link to confirm your email {verification_url}
        """,
        subtype="html"
    )

    return email
