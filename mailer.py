import os
import smtplib
from email.message import EmailMessage
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')


def send_mail(to_address: str, subject: str, body: str, attachment_path: str) -> None:
    """Send an email with an attachment."""
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_address
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        data = f.read()
        msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=os.path.basename(attachment_path))

    logger.info("Sending email to %s", to_address)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    logger.info("Email sent to %s", to_address)
