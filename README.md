# Gmail Email Service — Render Deployment

A minimal Python/Flask web service that sends emails via Gmail SMTP.
Deployable for free on [Render](https://render.com).

---

## 📋 Prerequisites

### 1. Generate a Gmail App Password
Google requires an **App Password** instead of your regular password.

1. Go to your Google Account → **Security**
2. Make sure **2-Step Verification** is ON
3. Search for **"App Passwords"** (or visit https://myaccount.google.com/apppasswords)
4. Choose App: **Mail**, Device: **Other** → name it "Render"
5. Copy the 16-character password (e.g. `abcd efgh ijkl mnop`)

---

## 🚀 Deploy to Render

1. Push this folder to a **GitHub repo**
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — confirm settings
5. Under **Environment Variables**, add:
   - `GMAIL_USER` → your Gmail address (e.g. `you@gmail.com`)
   - `GMAIL_APP_PASSWORD` → the 16-char App Password from above
6. Click **Deploy**

---

## 📡 API Usage

### Health check
```
GET /
```

### Send an email
```
POST /send
Content-Type: application/json

{
  "to": "recipient@example.com",
  "subject": "Hello from Render!",
  "body": "This email was sent from my Python service."
}
```

**Success response:**
```json
{ "status": "sent", "to": "recipient@example.com", "subject": "Hello from Render!" }
```

---

## 🧪 Test Locally

```bash
pip install -r requirements.txt

export GMAIL_USER="you@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"

python app.py
```

Then test with curl:
```bash
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"to":"test@example.com","subject":"Test","body":"It works!"}'
```
