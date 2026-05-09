from flask import Flask, render_template, request, redirect, session
import random
import os

# ML + Email
from predictor import predict
from email_sender import send_email
from emails import department_emails

# Database
from database import conn, cursor

app = Flask(__name__)
app.secret_key = "secret123"

# Demo mode
DEMO_MODE = False

# OTP storage
otp_store = {}
otp_attempts = {}

# 🔐 Generate OTP
def generate_otp(email):

    otp = random.randint(1000, 9999)

    otp_store[email] = otp
    otp_attempts[email] = 0

    print("OTP for", email, "is:", otp)

    # Send OTP Email
    send_email(
        email,
        f"Your OTP is {otp}",
        "OTP Verification"
    )

# 🚨 Emergency detection
def is_emergency(text):

    keywords = [
        "accident",
        "fire",
        "fight",
        "urgent",
        "help"
    ]

    return any(
        word in text.lower()
        for word in keywords
    )

# 🔹 Home Page
@app.route("/")
def home():

    return render_template("login.html")

# 🔹 Login Route
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]

    # Save user in database
    cursor.execute(
        "INSERT OR IGNORE INTO users(email) VALUES(?)",
        (email,)
    )

    conn.commit()

    generate_otp(email)

    return render_template(
        "otp.html",
        email=email
    )

# 🔹 OTP Verify
@app.route("/verify", methods=["POST"])
def verify():

    email = request.form["email"]

    user_otp = int(
        request.form["otp"]
    )

    # Too many attempts
    if otp_attempts.get(email, 0) >= 5:

        otp_attempts[email] = 0

        return redirect("/")

    # Demo mode
    if DEMO_MODE:

        session["user"] = email

        otp_attempts[email] = 0

        return redirect("/main")

    # Real OTP check
    if otp_store.get(email) == user_otp:

        session["user"] = email

        otp_attempts[email] = 0

        return redirect("/main")

    else:

        otp_attempts[email] += 1

        remaining = 5 - otp_attempts[email]

        return render_template(
            "otp.html",
            email=email,
            error=f"❌ Invalid OTP! {remaining} attempts left"
        )

# 🔹 Main Complaint Page
@app.route("/main", methods=["GET", "POST"])
def main():

    # Check login
    if "user" not in session:

        return redirect("/")

    result = ""

    if request.method == "POST":

        complaint = request.form["complaint"]

        # 🚨 Emergency
        if is_emergency(complaint):

            send_email(
                department_emails["Police"],
                complaint,
                "Police Emergency"
            )

            result = "🚨 Emergency! Sent to Police"

        else:

            # Predict department
            dept = predict(complaint)

            # Get department email
            email = department_emails.get(
                dept,
                "yourdefault@gmail.com"
            )

            # Send complaint email
            send_email(
                email,
                complaint,
                dept
            )

            # Save complaint in database
            cursor.execute(
                '''
                INSERT INTO complaints(

                    user_email,
                    complaint,
                    department,
                    status

                )

                VALUES (?, ?, ?, ?)
                ''',

                (
                    session["user"],
                    complaint,
                    dept,
                    "Pending"
                )
            )

            conn.commit()

            result = f"Complaint sent to {dept} Department 📧"

    return render_template(
        "index.html",
        result=result
    )

# 🔹 Complaint History
@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/")

    cursor.execute(
        '''
        SELECT
            complaint,
            department,
            status,
            created_at

        FROM complaints

        WHERE user_email=?
        ''',

        (session["user"],)
    )

    data = cursor.fetchall()

    return render_template(
        "history.html",
        complaints=data
    )

# 🔹 Statistics Page
@app.route("/stats")
def stats():

    if "user" not in session:

        return redirect("/")

    email = session["user"]

    # Total complaints
    cursor.execute(
        '''
        SELECT COUNT(*)

        FROM complaints

        WHERE user_email=?
        ''',

        (email,)
    )

    total = cursor.fetchone()[0]

    # Department wise stats
    cursor.execute(
        '''
        SELECT
            department,
            COUNT(*)

        FROM complaints

        WHERE user_email=?

        GROUP BY department
        ''',

        (email,)
    )

    data = cursor.fetchall()

    return render_template(
        "stats.html",
        total=total,
        data=data
    )

# 🔹 Logout
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

# 🔹 Run App
if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )