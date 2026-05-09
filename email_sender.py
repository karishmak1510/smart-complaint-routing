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

    print("🚀 send_email function started")

    try:

        socket.setdefaulttimeout(20)

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        print("📧 Connecting to Gmail SMTP")

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.ehlo()

        server.starttls()

        print("🔐 Logging in")

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        print("📨 Sending email")

        server.sendmail(
            SENDER_EMAIL,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:

        print("❌ EMAIL ERROR:")
        print(str(e))