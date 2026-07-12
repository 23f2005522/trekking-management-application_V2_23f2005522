from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from config.config import Config


def send_email(to_address, subject, body, content_type="plain"):
    """
    sends email via MailHog (localhost:1025).
    content_type: "plain" or "html"
    """
    msg = MIMEMultipart()
    msg["From"] = Config.SENDER_EMAIL
    msg["To"] = to_address
    msg["Subject"] = subject

    if content_type == "html":
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
        server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
        server.send_message(msg)

    return True
