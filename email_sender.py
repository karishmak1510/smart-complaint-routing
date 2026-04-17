import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ENABLED, SENDER_EMAIL, APP_PASSWORD

def send_email(to_email, complaint, department):

    if not EMAIL_ENABLED:
        print("Email disabled")
        return

    subject = f"New Complaint - {department}"
    body = f"""
New Complaint Received

Department: {department}

Complaint:
{complaint}
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    print("✅ Email sent")