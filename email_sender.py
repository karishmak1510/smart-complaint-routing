import smtplib
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

    print("🚀 EMAIL FUNCTION STARTED")

    try:

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        print("📧 Connecting SMTP")

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        print("🔐 Logging in")

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        print("📨 Sending Email")

        server.sendmail(
            SENDER_EMAIL,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:

        print("❌ EMAIL ERROR:")
        print(str(e))