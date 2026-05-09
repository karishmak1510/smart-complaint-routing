import smtplib
import socket

from email.mime.text import MIMEText

from config import (
    SENDER_EMAIL,
    APP_PASSWORD
)

def send_email(
    to_email,
    message,
    subject
):

    try:

        socket.setdefaulttimeout(20)

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=20
        )

        server.ehlo()

        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            to_email,
            msg.as_string()
        )

        server.quit()

        print(
            "✅ Email sent successfully"
        )

    except Exception as e:

        print(
            "❌ Email Error:",
            e
        )