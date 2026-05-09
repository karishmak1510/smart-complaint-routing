import smtplib
from email.mime.text import MIMEText
from config import SENDER_EMAIL, APP_PASSWORD

def send_email(to_email, message, subject):

    msg = MIMEText(message)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)

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