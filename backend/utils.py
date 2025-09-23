import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import redirect, request, session, url_for

from .constants import SMTP_PORT, SMTP_SERVER, SMTP_USER, TO_EMAIL


def require_admin(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if session.get("is_admin") is True:
            return view_function(*args, **kwargs)
        session["is_admin"] = False
        return redirect(url_for("admin_login", next=request.path))

    return wrapper


def _send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    pw = os.getenv("SMTP_PW")
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Upgrade the connection to secure
    server.login(SMTP_USER, pw)
    server.send_message(msg)
    server.quit()
