from flask import Flask, render_template, request
from predictor import predict
from email_sender import send_email
from emails import department_emails

app = Flask(__name__)

# Emergency detection
def is_emergency(text):
    keywords = ["accident", "fire", "fight", "urgent", "help"]
    return any(word in text.lower() for word in keywords)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        complaint = request.form["complaint"]

        # Emergency case
        if is_emergency(complaint):
            send_email(department_emails["Police"], complaint, "Police")
            result = "🚨 Emergency! Complaint sent to Police"
        else:
            dept = predict(complaint)
            email = department_emails.get(dept)

            send_email(email, complaint, dept)

            result = f"Complaint sent to {dept} Department 📧"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)