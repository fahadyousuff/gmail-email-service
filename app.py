import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Gmail credentials from environment variables
GMAIL_USER = os.environ.get("GMAIL_USER")       # your Gmail address
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")  # Gmail App Password


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email using Gmail SMTP."""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())

    return {"status": "sent", "to": to, "subject": subject}


@app.route("/")
def index():
    return jsonify({"message": "Email service is running ✅"})


@app.route("/send", methods=["POST"])
def send():
    """
    POST /send
    JSON body: { "to": "...", "subject": "...", "body": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    to = data.get("to")
    subject = data.get("subject")
    body = data.get("body")

    if not all([to, subject, body]):
        return jsonify({"error": "Fields 'to', 'subject', and 'body' are required"}), 400

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return jsonify({"error": "Gmail credentials not configured in environment variables"}), 500

    try:
        result = send_email(to, subject, body)
        return jsonify(result), 200
    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "Gmail authentication failed. Check your App Password."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
