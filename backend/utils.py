from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from .constants import SMTP_SERVER, SMTP_PORT, SMTP_USER, TO_EMAIL, USER_DB_PATH
import os


def _send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    pw = os.getenv("SMTP_PW")

    msg.attach(MIMEText(body, "plain"))
    # Connect and send
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Upgrade the connection to secure
    server.login(SMTP_USER, pw)
    server.send_message(msg)
    server.quit()
