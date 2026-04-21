from flask import Flask, render_template, request, redirect, session
import random

# ML + Email
from predictor import predict
from email_sender import send_email
from emails import department_emails

app = Flask(__name__)
app.secret_key = "secret123"
DEMO_MODE = True   # 🔥 change later
# OTP storage
otp_store = {}
otp_attempts = {}

# 🔐 Generate OTP
def generate_otp(phone):
    otp = random.randint(1000, 9999)
    otp_store[phone] = otp
    otp_attempts[phone] = 0
    print("OTP for", phone, "is:", otp)

# 🚨 Emergency detection
def is_emergency(text):
    keywords = ["accident", "fire", "fight", "urgent", "help"]
    return any(word in text.lower() for word in keywords)

# 🔹 Home (Login page)
@app.route("/")
def home():
    return render_template("login.html")

# 🔹 Login → Generate OTP
@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    phone = request.form["phone"]

    generate_otp(phone)

    return render_template("otp.html", phone=phone)

# 🔹 OTP Verify
@app.route("/verify", methods=["POST"])
def verify():
    phone = request.form["phone"]
    user_otp = int(request.form["otp"])

    # limit check
    if otp_attempts.get(phone, 0) >= 5:
        otp_attempts[phone] = 0
        return render_template("login.html", error="❌ Too many attempts! Try again.")




# 🔥 DEMO MODE
if DEMO_MODE:
    session["user"] = phone
    otp_attempts[phone] = 0
    return redirect("/main")












    if otp_store.get(phone) == user_otp:
        session["user"] = phone
        otp_attempts[phone] = 0
        return redirect("/main")
    else:
        otp_attempts[phone] += 1
        remaining = 5 - otp_attempts[phone]

        return render_template(
            "otp.html",
            phone=phone,
            error=f"❌ Invalid OTP! {remaining} attempts left"
        )
# 🔹 Main page
@app.route("/main", methods=["GET", "POST"])
def main():
    if "user" not in session:
        return redirect("/")

    result = ""

    if request.method == "POST":
        complaint = request.form["complaint"]

        if is_emergency(complaint):
            send_email(department_emails["Police"], complaint, "Police")
            result = "🚨 Emergency! Sent to Police"
        else:
            dept = predict(complaint)
            email = department_emails.get(dept)

            send_email(email, complaint, dept)

            result = f"Complaint sent to {dept} Department 📧"

    return render_template("index.html", result=result)

# 🔹 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)